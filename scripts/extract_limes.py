#!/usr/bin/env python3
"""Extract relevant sentences from Wikipedia HTML about Limes."""
import re, html, sys

with open(sys.argv[1], encoding="utf-8", errors="replace") as f:
    content = f.read()

text = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.S)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.S)
text = re.sub(r'<[^>]+>', ' ', text)
text = html.unescape(text)

for sentence in re.split(r'[.!?]+', text):
    s = sentence.strip()
    if len(s) > 20 and any(k in s.lower() for k in ['limes', 'world heritage', 'unesco', 'rhine', 'danube', 'fortress', 'frontier']):
        print(s[:300])
        print("---")
