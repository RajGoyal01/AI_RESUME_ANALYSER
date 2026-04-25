"""
Flask Backend - AI Resume Analyser API
"""
import os
import sys
import traceback
from flask import Flask, request, jsonify, send_from_directory, make_response
from flask_cors import CORS
from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, MAX_CONTENT_LENGTH, COURSES, BRANCHES, DOMAIN_SKILLS
from resume_parser import parse_resume
from analyser import analyze_resume

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH  # 50MB
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ─── Ensure CORS + JSON headers on EVERY response (especially errors) ───
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    # Ensure API routes always return JSON content type
    if request.path.startswith('/api/'):
        response.headers['Content-Type'] = 'application/json'
    return response


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def json_error(message, status_code=400):
    """Helper to always return a proper JSON error response with CORS headers."""
    resp = make_response(jsonify({"error": message}), status_code)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_from_directory(app.static_folder, path)
    except Exception:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/config', methods=['GET'])
def get_config():
    return jsonify({
        "courses": COURSES,
        "branches": BRANCHES,
        "domains": list(DOMAIN_SKILLS.keys()),
        "allowed_extensions": list(ALLOWED_EXTENSIONS),
        "max_file_size_mb": MAX_CONTENT_LENGTH // (1024 * 1024),
    })


# Handle preflight OPTIONS requests explicitly
@app.route('/api/analyze', methods=['OPTIONS'])
def analyze_options():
    resp = make_response('', 200)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return resp


@app.route('/api/analyze', methods=['POST'])
def analyze():
    filepath = None
    try:
        # Check content length before processing (catches large files early)
        content_length = request.content_length
        if content_length and content_length > MAX_CONTENT_LENGTH:
            max_mb = MAX_CONTENT_LENGTH // (1024 * 1024)
            return json_error(f"File too large. Maximum size is {max_mb}MB.", 413)

        # Validate file presence
        if 'resume' not in request.files:
            return json_error("No file uploaded. Please select a resume file.")

        file = request.files['resume']
        if file.filename == '' or file.filename is None:
            return json_error("No file selected. Please choose a file.")

        if not allowed_file(file.filename):
            allowed_list = ', '.join(sorted(ALLOWED_EXTENSIONS)).upper()
            return json_error(f"Invalid file type. Allowed formats: {allowed_list}")

        domain = request.form.get('domain', 'Computer Science')
        course = request.form.get('course', 'B.Tech')
        branch = request.form.get('branch', 'Computer Science')

        # Secure the filename and save
        original_name = file.filename
        filename = secure_filename(file.filename)
        if not filename:
            filename = 'resume_upload'
        # Preserve original extension
        ext = os.path.splitext(original_name)[1].lower()
        if ext and not filename.endswith(ext):
            filename = filename + ext

        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        try:
            file.save(filepath)
        except Exception as save_err:
            print(f"[ERROR] Failed to save file: {save_err}")
            return json_error("Failed to save uploaded file. Please try again.")

        file_size = os.path.getsize(filepath)
        print(f"[INFO] File saved: {filepath} ({file_size} bytes)")

        if file_size == 0:
            return json_error("Uploaded file is empty. Please select a valid resume file.")

        # Parse the resume
        print(f"[INFO] Parsing resume: {filename}")
        try:
            parsed = parse_resume(filepath)
        except Exception as parse_err:
            print(f"[ERROR] Parse exception: {parse_err}")
            traceback.print_exc()
            return json_error(f"Failed to parse resume: {str(parse_err)}")

        if parsed is None:
            return json_error("Resume parser returned no data. Please try a different file format.")

        if "error" in parsed:
            print(f"[WARN] Parse error: {parsed['error']}")
            return json_error(parsed['error'])

        print(f"[INFO] Parse success: {parsed.get('word_count', 0)} words extracted")

        # Analyse the resume
        try:
            results = analyze_resume(parsed, domain, course, branch)
        except Exception as analyze_err:
            print(f"[ERROR] Analysis exception: {analyze_err}")
            traceback.print_exc()
            return json_error(f"Analysis failed: {str(analyze_err)}")

        if results is None:
            return json_error("Analysis returned no results. Please try again.")

        # Attach parsed info for frontend display
        results["parsed_info"] = {
            "name": parsed.get("name"),
            "email": parsed.get("email"),
            "phone": parsed.get("phone"),
            "links": parsed.get("links"),
            "word_count": parsed.get("word_count"),
            "section_names": parsed.get("section_names"),
            "education": parsed.get("education"),
            "project_count": parsed.get("project_count"),
        }
        results["input"] = {"domain": domain, "course": course, "branch": branch}
        print(f"[INFO] Analysis complete: score={results.get('overall_score', 0)}, grade={results.get('grade', '?')}")
        
        response = jsonify(results)
        return response

    except RequestEntityTooLarge:
        max_mb = MAX_CONTENT_LENGTH // (1024 * 1024)
        return json_error(f"File too large. Maximum size is {max_mb}MB.", 413)
    except Exception as e:
        traceback.print_exc()
        print(f"[ERROR] Analysis failed: {str(e)}")
        return json_error(f"Analysis failed: {str(e)}", 500)
    finally:
        # Clean up uploaded file
        if filepath:
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
            except Exception:
                pass


# Import the exception class for 413 handling
from werkzeug.exceptions import RequestEntityTooLarge


# Catch ALL errors and return valid JSON with CORS headers
@app.errorhandler(413)
def too_large(e):
    max_mb = MAX_CONTENT_LENGTH // (1024 * 1024)
    return json_error(f"File too large. Maximum size is {max_mb}MB.", 413)


@app.errorhandler(500)
def internal_error(e):
    return json_error("Internal server error. Please try again.", 500)


@app.errorhandler(400)
def bad_request(e):
    return json_error("Bad request. Please check your upload and try again.", 400)


@app.errorhandler(404)
def not_found(e):
    return json_error("Resource not found.", 404)


# Health check endpoint for debugging
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "Server is running"})


if __name__ == '__main__':
    print("=" * 50)
    print("  AI Resume Analyser - Server Starting")
    print("  Open http://localhost:5000 in your browser")
    print("=" * 50)
    app.run(debug=True, port=5000, host='0.0.0.0', use_reloader=False)
