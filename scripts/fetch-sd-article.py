#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch-sd-article.py — Fetch a ScienceDaily article page and extract readable text.
ScienceDaily 403s via Jina Reader, so we grab raw HTML and extract the article body.
"""
import urllib.request, re, sys

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

url = sys.argv[1] if len(sys.argv) > 1 else "https://www.sciencedaily.com/releases/2026/10/261020085020.htm"
req = urllib.request.Request(url, headers={"User-Agent": UA})
html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")

# ScienceDaily article body — try the main content area
# Often wrapped in <div id="text"> or similar
# Extract paragraphs from article
paras = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL | re.IGNORECASE)
text_parts = []
for p in paras:
    clean = re.sub(r'<[^>]+>', '', p).strip()
    clean = re.sub(r'\s+', ' ', clean)
    if len(clean) > 40:
        text_parts.append(clean)

# Also grab the title
title_m = re.search(r'<title>(.*?)</title>', html, re.DOTALL | re.IGNORECASE)
if title_m:
    print("TITLE:", title_m.group(1).strip())
print(f"\n{'='*60}")
print(f"Extracted {len(text_parts)} paragraphs (len>40)\n")
for i, p in enumerate(text_parts[:80]):
    print(f"[{i}] {p[:300]}")
    print()
