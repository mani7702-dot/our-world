#!/usr/bin/env python3
"""Extract full article text from NC State page."""
import re

with open("/tmp/ncsu_plantarmor.html", errors="replace") as f:
    html = f.read()

# Try to find the article content - look for <article> tag
art_match = re.search(r'<article[^>]*>(.*?)</article>', html, re.I | re.S)
if art_match:
    art_html = art_match.group(1)
    # Remove scripts and styles
    art_html = re.sub(r'<script.*?</script>', '', art_html, flags=re.I|re.S)
    art_html = re.sub(r'<style.*?</style>', '', art_html, flags=re.I|re.S)
    # Remove tags
    text = re.sub(r'<[^>]+>', ' ', art_html)
    text = re.sub(r'\s+', ' ', text).strip()
    print(f"ARTICLE LENGTH: {len(text)} chars")
    print(text[:3000])
else:
    # Try finding content by class names
    for pattern in [r'class="entry-content[^"]*"', r'class="article-body[^"]*"', r'class="content[^"]*"']:
        m = re.search(pattern, html, re.I)
        if m:
            start = m.start()
            chunk = html[start:start+8000]
            text = re.sub(r'<[^>]+>', ' ', chunk)
            text = re.sub(r'\s+', ' ', text).strip()
            print(f"Found content via {pattern}:")
            print(text[:2000])
            print()
