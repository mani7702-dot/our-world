#!/usr/bin/env python3
"""Extract APOD explanation text from NASA Science page."""
import re
from html import unescape

html = open('/tmp/apod-rainbow.html').read()

# Try to find the image explanation - look for text between specific patterns
# APOD pages have the explanation in the main content area

# Find all text content
text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', ' ', text)
text = unescape(text)
text = re.sub(r'\s+', ' ', text).strip()

# Find the section about anticrepuscular rainbow
# Look for the explanation portion
idx = text.lower().find('anticrepuscular')
if idx >= 0:
    print(text[max(0,idx-200):idx+1200])
print('---')
# Also look for rainbow fan
idx2 = text.lower().find('rainbow fan')
if idx2 >= 0:
    print(text[max(0,idx2-200):idx2+800])
