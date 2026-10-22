#!/usr/bin/env python3
"""Extract more content from the NC State article."""
import re

with open("/tmp/ncsu_straw2.html", errors="replace") as f:
    html = f.read()

# Remove scripts and styles
html2 = re.sub(r'<script.*?</script>', '', html, flags=re.I|re.S)
html2 = re.sub(r'<style.*?</style>', '', html2, flags=re.I|re.S)

# Find all paragraphs with substantial content
paras = re.findall(r'<p[^>]*>(.*?)</p>', html2, re.I | re.S)
for i, p in enumerate(paras):
    text = re.sub(r'<[^>]+>', '', p).strip()
    text = re.sub(r'\s+', ' ', text)
    if len(text) > 80:
        print(f"[{i}] ({len(text)} chars): {text[:400]}")
        print()

# Also look for h2, h3 headings
headings = re.findall(r'<h[23][^>]*>(.*?)</h[23]>', html2, re.I | re.S)
for h in headings:
    text = re.sub(r'<[^>]+>', '', h).strip()
    if len(text) > 5:
        print(f"HEADING: {text}")
