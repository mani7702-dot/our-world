#!/usr/bin/env python3
"""Fetch full ScienceDaily article + cross-check Wikipedia gravitational lensing."""
import urllib.request, gzip, re, json

# 1. Get full ScienceDaily article
url = "https://www.sciencedaily.com/releases/2026/10/261012185021.htm"
req = urllib.request.Request(url, headers={
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
})
raw = urllib.request.urlopen(req, timeout=30).read()
if raw[:2] == b'\x1f\x8b':
    raw = gzip.decompress(raw)
html = raw.decode('utf-8', errors='replace')

article_m = re.search(r'<div id="text">(.*?)</div>\s*<div id="sources"', html, re.DOTALL)
if not article_m:
    article_m = re.search(r'<div id="text">(.*?)</div>\s*</div>', html, re.DOTALL)
if article_m:
    text = re.sub(r'<[^>]+>', ' ', article_m.group(1))
    text = re.sub(r'\s+', ' ', text)
    print("=== SCIENCEDAILY ARTICLE (continued) ===")
    print(text[3000:])
else:
    print("[Could not extract article body]")

# 2. Cross-check: Wikipedia gravitational lensing page via MediaWiki API
print("\n\n=== WIKIPEDIA API: GRAVITATIONAL LENSING ===")
wiki_url = "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro&explaintext&titles=Gravitational_lens&format=json&exchars=3000"
req2 = urllib.request.Request(wiki_url, headers={"User-Agent": "HermesBot/1.0 (educational; contact@example.com)"})
try:
    raw2 = urllib.request.urlopen(req2, timeout=30).read()
    data = json.loads(raw2.decode())
    pages = data['query']['pages']
    for pid, page in pages.items():
        if 'extract' in page:
            print(page['extract'][:2500])
        else:
            print("[No extract found]")
except Exception as e:
    print(f"Wikipedia API error: {e}")

# 3. Cross-check: JWST telescope page
print("\n\n=== WIKIPEDIA API: JWST ===")
wiki_url2 = "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro&explaintext&titles=James_Webb_Space_Telescope&format=json&exchars=2500"
req3 = urllib.request.Request(wiki_url2, headers={"User-Agent": "HermesBot/1.0 (educational; contact@example.com)"})
try:
    raw3 = urllib.request.urlopen(req3, timeout=30).read()
    data3 = json.loads(raw3.decode())
    pages3 = data3['query']['pages']
    for pid, page in pages3.items():
        if 'extract' in page:
            print(page['extract'][:2500])
        else:
            print("[No extract found]")
except Exception as e:
    print(f"Wikipedia API error: {e}")

# 4. Cross-check: Dark matter
print("\n\n=== WIKIPEDIA API: DARK MATTER ===")
wiki_url3 = "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro&explaintext&titles=Dark_matter&format=json&exchars=2500"
req4 = urllib.request.Request(wiki_url3, headers={"User-Agent": "HermesBot/1.0 (educational; contact@example.com)"})
try:
    raw4 = urllib.request.urlopen(req4, timeout=30).read()
    data4 = json.loads(raw4.decode())
    pages4 = data4['query']['pages']
    for pid, page in pages4.items():
        if 'extract' in page:
            print(page['extract'][:2500])
        else:
            print("[No extract found]")
except Exception as e:
    print(f"Wikipedia API error: {e}")
