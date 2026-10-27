#!/usr/bin/env python3
"""Fetch BBC articles for cross-check: zebra bee and student badge astronaut."""
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
ld_match = re.search(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', raw, re.S)
if ld_match:
    ld = json.loads(ld_match.group(1))
    print(f"Headline: {ld.get('headline', '')}")
    print(f"Description: {ld.get('description', '')}")
    print(f"Date: {ld.get('datePublished', '')}")
    if 'articleBody' in ld:
        print(f"Body: {ld['articleBody'][:2000]}")

# Fetch paragraph text
body_matches = re.findall(r'<[pP][^>]*>(.*?)</[pP]>', raw, re.S)
for p in body_matches:
    text = re.sub(r'<[^>]+>', '', p).strip()
    if len(text) > 50 and 'bee' in text.lower() and ('zebra' in text.lower() or 'stripe' in text.lower()):
        print(f"\nParagraph: {text[:500]}")

# Student badge
print("\n\n=== Student badge article ===")
raw2 = fetch_bbc('https://www.bbc.co.uk/news/articles/cq78pzl85nglo')
ld_match2 = re.search(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', raw2, re.S)
if ld_match2:
    ld2 = json.loads(ld_match2.group(1))
    print(f"Headline: {ld2.get('headline', '')}")
    print(f"Description: {ld2.get('description', '')}")
    print(f"Date: {ld2.get('datePublished', '')}")
    if 'articleBody' in ld2:
        print(f"Body: {ld2['articleBody'][:2000]}")
