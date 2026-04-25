"""
Resume Parser Module - Extracts text and structured info from resume files.
Supports: PDF, DOCX, TXT, JPG, JPEG, PNG, BMP, TIFF, WEBP (via OCR)
"""
import re, os
from typing import Dict, List, Optional
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None
try:
    import pdfplumber
except ImportError:
    pdfplumber = None
try:
    from docx import Document as DocxDocument
except ImportError:
    DocxDocument = None
try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# Try easyocr first (no system dependency needed)
try:
    import easyocr
    HAS_EASYOCR = True
    _easyocr_reader = None  # Lazy init to avoid slow startup
except ImportError:
    HAS_EASYOCR = False

# Fallback to pytesseract (needs Tesseract installed)
try:
    import pytesseract
    HAS_TESSERACT = True
    # Verify tesseract is actually installed
    try:
        pytesseract.get_tesseract_version()
    except Exception:
        HAS_TESSERACT = False
except ImportError:
    HAS_TESSERACT = False

from config import SECTION_KEYWORDS

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}

def _get_easyocr_reader():
    """Lazy-initialize easyocr reader (downloads model on first use)."""
    global _easyocr_reader
    if _easyocr_reader is None:
        _easyocr_reader = easyocr.Reader(['en'], gpu=False, verbose=False)
    return _easyocr_reader

def extract_text_from_pdf(filepath):
    text = ""
    if pdfplumber:
        try:
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    pt = page.extract_text()
                    if pt: text += pt + "\n"
            if text.strip(): return text
        except Exception: pass
    if PyPDF2:
        try:
            with open(filepath, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    pt = page.extract_text()
                    if pt: text += pt + "\n"
        except Exception: pass
    return text

def extract_text_from_image(filepath):
    """Extract text from image using easyocr (primary) or pytesseract (fallback)."""
    # Method 1: easyocr (no system dependency needed)
    if HAS_EASYOCR:
        try:
            reader = _get_easyocr_reader()
            results = reader.readtext(filepath, detail=0, paragraph=True)
            text = '\n'.join(results)
            if text.strip():
                print(f"OCR Success (easyocr): extracted {len(text)} chars")
                return text
        except Exception as e:
            print(f"easyocr Error: {e}")

    # Method 2: pytesseract (needs Tesseract installed)
    if HAS_TESSERACT and HAS_PIL:
        try:
            img = Image.open(filepath)
            if img.mode not in ('L', 'RGB'):
                img = img.convert('RGB')
            text = pytesseract.image_to_string(img, lang='eng')
            if text.strip():
                print(f"OCR Success (tesseract): extracted {len(text)} chars")
                return text
        except Exception as e:
            print(f"Tesseract Error: {e}")

    print("OCR: No working OCR engine available")
    return ""

def extract_text(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".pdf": return extract_text_from_pdf(filepath)
    elif ext in (".docx", ".doc"):
        if not DocxDocument: return ""
        try:
            doc = DocxDocument(filepath)
            return "\n".join([p.text for p in doc.paragraphs])
        except: return ""
    elif ext == ".txt":
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f: return f.read()
        except: return ""
    elif ext in IMAGE_EXTENSIONS:
        return extract_text_from_image(filepath)
    return ""

def extract_email(text):
    m = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    return m.group(0) if m else None

def extract_phone(text):
    for p in [r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', r'(?:\+?\d{1,3}[-.\s]?)?\d{10}', r'(?:\+?\d{1,3}[-.\s]?)?\d{5}[-.\s]?\d{5}']:
        m = re.search(p, text)
        if m: return m.group(0).strip()
    return None

def extract_name(text):
    for line in text.strip().split('\n'):
        line = line.strip()
        if line and len(line) < 60 and not re.search(r'[@\d]', line):
            words = line.split()
            if 1 <= len(words) <= 5: return line
    return None

def extract_links(text):
    links = {"linkedin": None, "github": None, "portfolio": None}
    m = re.search(r'(?:https?://)?(?:www\.)?linkedin\.com/in/[\w-]+', text, re.IGNORECASE)
    if m: links["linkedin"] = m.group(0)
    m = re.search(r'(?:https?://)?(?:www\.)?github\.com/[\w-]+', text, re.IGNORECASE)
    if m: links["github"] = m.group(0)
    for url in re.findall(r'https?://[^\s<>\"\']+', text):
        if "linkedin" not in url.lower() and "github" not in url.lower():
            links["portfolio"] = url; break
    return links

def detect_sections(text):
    lines = text.split('\n')
    sections = {}
    current_section = "header"
    current_content = []
    for line in lines:
        ll = line.strip().lower()
        found = None
        for sn, kws in SECTION_KEYWORDS.items():
            for kw in kws:
                if ll == kw or ll.startswith(kw + ":") or ll.startswith(kw + " ") or (len(ll) < 40 and kw in ll and ll.replace(kw, "").strip() in ("", ":", "-")):
                    found = sn; break
            if found: break
        if found:
            if current_content: sections[current_section] = '\n'.join(current_content)
            current_section = found; current_content = []
        else: current_content.append(line)
    if current_content: sections[current_section] = '\n'.join(current_content)
    return sections

def count_projects(text):
    sections = detect_sections(text)
    ps = sections.get("projects", "")
    if not ps: return 0
    count = 0
    for line in ps.split('\n'):
        line = line.strip()
        if line and len(line) > 5: count += 1
    return max(count // 2, 1) if count > 0 else 0

def extract_education(text):
    education = []
    sections = detect_sections(text)
    edu_text = sections.get("education", text)
    for line in edu_text.split('\n'):
        ll = line.lower().strip()
        if re.search(r'(?:b\.?tech|m\.?tech|b\.?e\.?|m\.?e\.?|b\.?sc|m\.?sc|bca|mca|mba|bba|ph\.?d|diploma|bachelor|master)', ll):
            entry = {"text": line.strip()}
            gm = re.search(r'(?:gpa|cgpa|percentage|score)\s*:?\s*([\d.]+)', ll)
            if gm: entry["gpa"] = gm.group(1)
            education.append(entry)
    return education

def parse_resume(filepath):
    text = extract_text(filepath)
    if not text or len(text.strip()) < 20:
        ext = os.path.splitext(filepath)[1].lower()
        if ext in IMAGE_EXTENSIONS:
            return {"error": "Could not extract text from the image. Please ensure the image is clear and contains readable text, or try uploading a PDF/DOCX version."}
        return {"error": "Could not extract sufficient text from the resume. Please try a different file format."}
    sections = detect_sections(text)
    return {
        "raw_text": text, "text_length": len(text), "word_count": len(text.split()),
        "name": extract_name(text), "email": extract_email(text), "phone": extract_phone(text),
        "links": extract_links(text), "sections": sections, "section_names": list(sections.keys()),
        "education": extract_education(text), "project_count": count_projects(text),
    }
