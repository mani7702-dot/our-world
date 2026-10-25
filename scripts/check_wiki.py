#!/usr/bin/env python3
"""Get more detail from Wikipedia about Nakumatt and Tuskys."""
import urllib.request
import json

def fetch_wikipedia_api(title):
    api_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=false&explaintext=true&titles={title}&format=json"
    req = urllib.request.Request(api_url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })
    resp = urllib.request.urlopen(req, timeout=30)
    data = json.loads(resp.read().decode('utf-8'))
    pages = data.get('query', {}).get('pages', {})
    for page_id, page in pages.items():
        return page.get('extract', '')[:5000]
    return "Not found"

print("=== Nakumatt Wikipedia extract ===")
print(fetch_wikipedia_api("Nakumatt"))

print("\n=== Tuskys Wikipedia extract ===")
print(fetch_wikipedia_api("Tuskys"))
