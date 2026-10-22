#!/usr/bin/env python3
"""Extract full article text from NC State page - try multiple selectors."""
import re

with open("/tmp/ncsu_plantarmor.html", errors="replace") as f:
    html = f.read()

# Try to find article body content
# Look for common article content wrappers
for selector in ['entry-content', 'article-body', 'post-content', 'content-area', 'main-content', 'ncst-article-body']:
    matches = re.findall(rf'class="[^"]*{selector}[^"]*"[^>]*>(.*?)</div>', html, re.I | re.S)
    for m in matches:
        text = re.sub(r'<script.*?</script>', '', m, flags=re.I|re.S)
        text = re.sub(r'<style.*?</style>', '', text, flags=re.I|re.S)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) > 200:
            print(f"=== {selector} ({len(text)} chars) ===")
            print(text[:5000])
            print()

# Also try finding all <p> tags after the title
paras = re.findall(r'<p[^>]*>(.*?)</p>', html, re.I | re.S)
print(f"\n=== ALL P TAGS ({len(paras)} total) ===")
for i, p in enumerate(paras):
    text = re.sub(r'<[^>]+>', '', p).strip()
    text = re.sub(r'\s+', ' ', text)
    if len(text) > 50:
        print(f"[{i}] ({len(text)} chars): {text[:300]}")
        print()
