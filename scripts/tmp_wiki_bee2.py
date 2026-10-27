#!/usr/bin/env python3
"""Search Wikipedia for the specific sea aster mining bee species."""
import urllib.request, json, re

def search_wiki(query):
    url = f'https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={query}&srlimit=5&format=json'
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    raw = urllib.request.urlopen(req, timeout=25).read().decode('utf-8', errors='ignore')
    data = json.loads(raw)
    results = data.get('query', {}).get('search', [])
    for r in results:
        print(f"  {r['title']}: {r['snippet'][:200]}")
    return results

# Search for the bee
print("=== Search: sea aster mining bee ===")
search_wiki('sea aster mining bee')

print("\n=== Search: Andrena gravidus ===")
search_wiki('Andrena gravidus')

print("\n=== Search: coastal saltmarsh ===")
search_wiki('coastal saltmarsh')

# Also fetch the Andrena page for more info
def fetch_wiki_full(title):
    url = f'https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext&titles={title}&format=json'
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

print("\n=== Andrena (mining bees) ===")
result = fetch_wiki_full('Andrena')
if result:
    print(result[:2000])
