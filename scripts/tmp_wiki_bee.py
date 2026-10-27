#!/usr/bin/env python3
"""Fetch Wikipedia articles for sea aster mining bee and saltmarsh restoration."""
import urllib.request, json, re

def fetch_wiki_api(title):
    url = f'https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro&explaintext&titles={title}&format=json'
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    raw = urllib.request.urlopen(req, timeout=25).read().decode('utf-8', errors='ignore')
    data = json.loads(raw)
    pages = data.get('query', {}).get('pages', {})
    for page_id, page in pages.items():
        if 'extract' in page:
            return page['extract'][:2000]
    return None

# Try different Wikipedia titles
titles = [
    'Andrena_crassa',  # One of the sea aster mining bees
    'Sea_aster',
    'Salt_meadow',
    'Steart_Marshes',
    'Mining_bee',
    'Andrena',
    'Coastal_saltmarsh',
    'Halictidae',
]

for title in titles:
    result = fetch_wiki_api(title)
    if result:
        print(f"=== {title} ===")
        print(result[:1000])
        print()
