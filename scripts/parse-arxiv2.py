#!/usr/bin/env python3
"""Fetch and parse arXiv search results properly."""
import re, subprocess
html = open('/tmp/arxiv.html', encoding='utf-8').read()
# Find all links to abs pages and their text
pattern = r'<a[^>]*href="(/abs/[0-9.]+)"[^>]*>(.*?)</a>'
matches = re.findall(pattern, html, re.S|re.I)
for link, text in matches:
    clean = re.sub(r'<[^>]+>', '', text)
    clean = clean.strip()
    if len(clean) > 10:
        print(f'{clean}')
        print(f'  https://arxiv.org{link}')
