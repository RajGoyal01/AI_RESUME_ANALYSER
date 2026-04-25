"""Test OCR on the user's actual JPG resume image."""
import sys, json
sys.path.insert(0, '.')
from resume_parser import parse_resume
from analyser import analyze_resume

filepath = 'test_resumes/veronica_rivers_resume.jpg'
print('Parsing JPG resume image...')
parsed = parse_resume(filepath)
if 'error' in parsed:
    print('ERROR:', parsed['error'])
else:
    print('Name:', parsed.get('name'))
    print('Email:', parsed.get('email'))
    print('Phone:', parsed.get('phone'))
    print('Words:', parsed.get('word_count'))
    print('Projects:', parsed.get('project_count'))
    print('Sections:', parsed.get('section_names'))
    print('Education:', parsed.get('education'))
    print()
    print('--- Text Preview (first 500 chars) ---')
    print(parsed['raw_text'][:500])
    print('--- End Preview ---')
    print()
    results = analyze_resume(parsed, 'Computer Science', 'B.Tech', 'Computer Science')
    print('Overall Score:', results['overall_score'], '/100')
    print('Grade:', results['grade'])
    print()
    print('Category Breakdown:')
    for cat in results.get('categories', []):
        print('  ', cat['name'], ':', cat['score'])
    print()
    print('MNC Readiness (top 5):')
    mnc = results.get('mnc_readiness', [])
    for item in sorted(mnc, key=lambda x: x.get('score', 0), reverse=True)[:5]:
        print('  ', item['name'], ':', item.get('score', 0), '%')
    print()
    print('SUCCESS - Analysis completed!')
