#!/usr/bin/env python3
"""Search for secondary sources via DuckDuckGo Lite."""
import urllib.request
import re

def search_ddg(query):
    url = f"https://lite.duckduckgo.com/lite/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    })
    resp = urllib.request.urlopen(req, timeout=15)
    html = resp.read().decode('utf-8', errors='replace')
    # Extract result links/text
    results = re.findall(r'<a[^>]+class="result-link"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', html, re.DOTALL)
    if not results:
        results = re.findall(r'<a[^>]+href="(https?://[^"]+)"[^>]*>(.*?)</a>', html, re.DOTALL)
    for link, text in results[:10]:
        clean_text = re.sub(r'<[^>]+>', '', text).strip()
        if clean_text:
            print(f"  {clean_text}")
            print(f"  URL: {link}")
            print()

import urllib.parse
print("Searching: PwC economic crime East Africa 2022 survey")
search_ddg("PwC economic crime survey East Africa 2022")
print("\n---\n")
print("Searching: Nakumatt stock theft closure 2020")
search_ddg("Nakumatt Kenya closure employee theft 2020")
print("\n---\n")
print("Searching: Tuskys employee theft loss 100m shillings")
search_ddg("Tuskys Kenya employee theft 100m shillings Hipora")
