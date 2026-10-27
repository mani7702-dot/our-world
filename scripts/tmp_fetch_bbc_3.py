#!/usr/bin/env python3
"""Fetch full BBC article content for zebra bee and student badge."""
import urllib.request, re, json

def fetch_bbc(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    raw = urllib.request.urlopen(req, timeout=25).read().decode('utf-8', errors='ignore')
    return raw

# Zebra bee
print("=== Zebra bee article ===")
raw = fetch_bbc('https://www.bbc.co.uk/news/articles/c3dxwjx7xpj0o')

# Find all paragraphs in the article body
# BBC uses specific data attributes
paragraphs = re.findall(r'<[pP][^>]*data-block-tracking-id="paragraph"[^>]*>(.*?)</[pP]>', raw, re.S)
if not paragraphs:
    # Try general paragraph extraction
    paragraphs = re.findall(r'<[pP][^>]*>(.*?)</[pP]>', raw, re.S)

for p in paragraphs:
    text = re.sub(r'<[^>]+>', '', p).strip()
    if len(text) > 30 and 'skip' not in text.lower() and 'menu' not in text.lower():
        print(text[:500])
        print()

# Also try JSON-LD full body
ld_match = re.search(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', raw, re.S)
if ld_match:
    ld = json.loads(ld_match.group(1))
    if isinstance(ld, dict):
        for k, v in ld.items():
            if k == 'articleBody' and isinstance(v, str):
                print(f"\n=== JSON-LD Body ===")
                print(v[:3000])
