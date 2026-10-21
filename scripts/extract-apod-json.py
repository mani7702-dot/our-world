#!/usr/bin/env python3
"""Extract APOD explanation from NASA page meta tags."""
import re
from html import unescape

html = open('/tmp/apod-rainbow2.html').read()

# Find meta description
desc_match = re.search(r'"description"\s*:\s*"([^"]{100,800})"', html)
if desc_match:
    desc = unescape(desc_match.group(1))
    print("DESCRIPTION:")
    print(desc[:600])
    print()

# Find the actual APOD image credit/description  
# Look for text mentioning anticrepuscular and rainbow fan in paragraphs
text = re.sub(r'<script[^>]*>.*?</script>', ' ', html, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', ' ', text, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', '\n', text)
text = unescape(text)
lines = [l.strip() for l in text.split('\n') if l.strip() and len(l.strip()) > 40]

# Find lines with relevant keywords
for line in lines:
    low = line.lower()
    if any(w in low for w in ['anticrepuscular', 'rainbow fan', 'sun ', 'backscatter', 'antisolar', 'perspective', 'optical phenomenon', 'crepuscular ray', 'water droplet', 'refraction']):
        if 'script' not in low and 'function' not in low and 'var ' not in low:
            print(line[:300])
            print('---')
