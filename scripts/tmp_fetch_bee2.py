#!/usr/bin/env python3
"""Fetch BBC article body text from the JSON-LD / article content."""
import urllib.request, re, json

url = 'https://www.bbc.co.uk/news/articles/c3dxwjx7xpj0o'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})
raw = urllib.request.urlopen(req, timeout=25).read().decode('utf-8', errors='ignore')

# Find JSON-LD
ld_match = re.search(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', raw, re.S)
if ld_match:
    ld = json.loads(ld_match.group(1))
    # Print all string values
    def extract_strings(obj, depth=0):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in ('headline', 'description', 'articleBody', 'date'):
                    print(f'{k}: {v[:500]}' if isinstance(v, str) else f'{k}: {v}')
                extract_strings(v, depth+1)
        elif isinstance(obj, list):
            for item in obj:
                extract_strings(item, depth+1)
    extract_strings(ld)

# Also try to find article body in the HTML
body_matches = re.findall(r'<p[^>]*class="[^"]*paragraph[^"]*"[^>]*>(.*?)</p>', raw, re.S)
if body_matches:
    print("\n=== Article paragraphs ===")
    for p in body_matches[:10]:
        text = re.sub(r'<[^>]+>', '', p).strip()
        if text:
            print(text[:300])
            print()
