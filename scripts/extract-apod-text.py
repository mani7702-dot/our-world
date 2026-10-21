#!/usr/bin/env python3
import re
from html import unescape

html = open('/tmp/apod261020.html').read()
text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', '\n', text)
text = unescape(text)
lines = [l.strip() for l in text.split('\n') if l.strip()]

for i, line in enumerate(lines):
    if 'Anticrepuscular Rainbow Fan' in line or 'APOD: 2026 October 20' in line:
        for j in range(i, min(i+80, len(lines))):
            if len(lines[j]) > 25:
                print(lines[j][:300])
        break
