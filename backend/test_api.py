"""Test the API endpoint with the actual JPG resume via HTTP."""
import requests

files = {'resume': ('veronica_resume.jpg', open('test_resumes/veronica_rivers_resume.jpg', 'rb'), 'image/jpeg')}
data = {'course': 'B.Tech', 'branch': 'Computer Science', 'domain': 'Computer Science'}

print("Sending JPG resume to API...")
r = requests.post('http://localhost:5000/api/analyze', files=files, data=data, timeout=120)
print("Status:", r.status_code)

if r.status_code == 200:
    d = r.json()
    print("Score:", d.get('overall_score'))
    print("Grade:", d.get('grade'))
    print()
    print("Categories:")
    for c in d.get('categories', []):
        print("  ", c['name'], ":", c['score'])
    print()
    print("Top MNC matches:")
    mncs = d.get('mnc_readiness', [])
    for m in sorted(mncs, key=lambda x: x.get('score', 0), reverse=True)[:5]:
        print("  ", m['name'], ":", m.get('score', 0), "%")
    print()
    pi = d.get('parsed_info', {})
    print("Parsed Name:", pi.get('name'))
    print("Parsed Email:", pi.get('email'))
    print("Parsed Phone:", pi.get('phone'))
    print("Word Count:", pi.get('word_count'))
    print()
    print("SUCCESS!")
else:
    print("ERROR:", r.text)
