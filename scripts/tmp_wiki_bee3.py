#!/usr/bin/env python3
"""Search Wikipedia for sea aster mining bee info."""
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

def search_wiki(query):
    encoded_query = quote(query)
    url = f'https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={encoded_query}&srlimit=5&format=json'
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    raw = urllib.request.urlopen(req, timeout=25).read().decode('utf-8', errors='ignore')
    data = json.loads(raw)
    results = data.get('query', {}).get('search', [])
    for r in results:
        print(f"  {r['title']}: {r.get('snippet', '')[:200]}")
    return results

print("=== Search: sea aster mining bee ===")
search_wiki('sea aster mining bee')

print("\n=== Search: Andrena gravidus ===")
search_wiki('Andrena gravidus')

print("\n=== Andrena (mining bees) ===")
result = fetch_wiki_api('Andrena')
if result:
    print(result[:2000])
