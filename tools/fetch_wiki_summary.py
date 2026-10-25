#!/usr/bin/env python3
"""Fetch Wikipedia summaries for cross-checking."""
import urllib.request, json, sys

def fetch_wiki_summary(title):
    url = f'https://en.wikipedia.org/api/rest_v1/page/summary/{title}'
    req = urllib.request.Request(url, headers={'User-Agent': 'OurWorldBot/1.0'})
    resp = urllib.request.urlopen(req, timeout=15)
    data = json.loads(resp.read().decode())
    return data.get('extract', 'N/A')

if __name__ == "__main__":
    for title in sys.argv[1:]:
        print(f"=== {title} ===")
        try:
            print(fetch_wiki_summary(title))
        except Exception as e:
            print(f"Error: {e}")
        print()
