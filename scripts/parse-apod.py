#!/usr/bin/env python3
"""Extract APOD article content from saved HTML."""
import re, sys
from html import unescape

html = open('/tmp/apod-rainbow.html').read()

# Find the main content - APOD typically has image description in a specific div
# Look for the image credit/description text
img_match = re.search(r'(The image|Image credits|Image:|Explanation:)(.*?)(\n\n|\Z)', html, re.DOTALL | re.IGNORECASE)

# Find the main APOD text block
text_blocks = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
for block in text_blocks:
    clean = re.sub(r'<[^>]+>', '', block).strip()
    clean = unescape(clean)
    if len(clean) > 80 and ('rainbow' in clean.lower() or 'anticrepuscular' in clean.lower() or 'sun' in clean.lower()):
        print(clean)
        print('---')
