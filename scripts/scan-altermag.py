"""Scan a file for mentions of altermagnetism."""
import re
with open('/tmp/physicsworld.html', 'r', errors='replace') as f:
    h = f.read()
text = re.sub(r'<script[^>]*>.*?</script>', ' ', h, flags=re.DOTALL | re.IGNORECASE)
text = re.sub(r'<[^>]+>', ' ', text)
text = ' '.join(text.split())
for m in re.finditer(r'[Aa]ltermagnet', text):
    s = max(0, m.start() - 100)
    e = min(len(text), m.end() + 200)
    print(text[s:e])
    print('---')
