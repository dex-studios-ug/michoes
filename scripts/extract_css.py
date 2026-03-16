import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent
html_files = ['index.html','about.html','appointment.html','services.html','facilities.html','specialists.html']

for fname in html_files:
    p = root / fname
    text = p.read_text(encoding='utf-8')

    # Remove any <style>...</style> blocks (handles attributes too)
    new_text = re.sub(r'<style[^>]*>.*?</style>\s*', '', text, flags=re.S)
    # Remove any leftover closing style tags (in case partial edits left them)
    new_text = new_text.replace('</style>', '')

    # Add shared stylesheet if missing
    if 'href="css/michoes.css"' not in new_text:
        head_end = new_text.find('</head>')
        if head_end == -1:
            print(f"WARN: no </head> in {fname}")
            continue
        head = new_text[:head_end]
        rest = new_text[head_end:]
        insertion = '  <link rel="stylesheet" href="css/michoes.css">\n'
        if 'bootstrap-icons' in head:
            head = re.sub(r'(\<link[^>]*bootstrap-icons[^>]*>\s*)', r'\1' + insertion, head, count=1)
        else:
            head = head + insertion
        new_text = head + rest

    p.write_text(new_text, encoding='utf-8')
    print(f"Updated {fname}")
