#!/usr/bin/env python3
"""Fetch Colletes halophilus and saltmarsh Wikipedia articles."""
import urllib.request, json, re
from urllib.parse import quote

def fetch_wiki_api(title):
    encoded_title = quote(title)
    url = f'https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext&titles={encoded_title}&format=json'
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    raw = urllib.request.urlopen(req, timeout=25).read().decode('utf-8', errors='ignore')
    data = json.loads(raw)
    pages = data.get('query', {}).get('pages', {})
    for page_id, page in pages.items():
        if 'extract' in page:
            return page['extract'][:3000]
    return None

for title in ['Colletes halophilus', 'Saltmarsh', 'Salt_meadow', 'Sea aster']:
    result = fetch_wiki_api(title)
    if result:
        print(f"=== {title} ===")
        print(result[:2000])
        print()
    else:
        print(f"=== {title} === (no extract found)")
        print()
