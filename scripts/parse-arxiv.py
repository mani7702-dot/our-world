#!/usr/bin/env python3
"""Extract arXiv search result titles/links from a saved HTML file."""
import re, sys
html = open(sys.argv[1], encoding='utf-8').read()
# arXiv search results: each result has an <a href="/abs/...">title</a>
links = re.findall(r'href=\"(/abs/[0-9.]+)\"', html)
for l in links[:15]:
    print(f'https://arxiv.org{l}')
# Also try the result entries
titles = re.findall(r'class="title"[^>]*>(.*?)</a>', html, re.S)
ids = re.findall(r'/abs/([0-9.]+)', html)
if ids:
    print(f'\nFound {len(ids)} article IDs')
