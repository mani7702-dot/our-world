#!/usr/bin/env python3
"""Check what the FieldMuseum.jpg Commons page describes."""
import urllib.request, urllib.parse, json

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
API = "https://commons.wikimedia.org/w/api.php"

# First, find pages containing "narwhal" and "FieldMuseum" or look at the file page directly
params = {
    'action': 'query',
    'format': 'json',
    'titles': 'File:FieldMuseum.jpg',
    'prop': 'imageinfo',
    'iiprop': 'extmetadata',
    'iiurlwidth': '1200',
}
url = API + "?" + urllib.parse.urlencode(params)
req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
with urllib.request.urlopen(req, timeout=30) as resp:
    data = json.loads(resp.read().decode("utf-8", "replace"))

pages = data.get("query", {}).get("pages", {})
for pid, pg in pages.items():
    meta = pg.get("extmetadata", {}) or {}
    desc = meta.get("Description", {}).get("value", "")
    artist = meta.get("Artist", {}).get("value", "")
    print("Description (HTML):", desc[:500])
    print("Artist:", artist[:300])

# Also fetch the actual Commons page HTML to see what the image depicts
print("\n--- Fetching Commons file page ---")
params2 = {
    'action': 'parse',
    'format': 'json',
    'page': 'File:FieldMuseum.jpg',
    'prop': 'wikitext',
    'section': 0,
}
url2 = API + "?" + urllib.parse.urlencode(params2)
req2 = urllib.request.Request(url2, headers={"User-Agent": UA})
try:
    with urllib.request.urlopen(req2, timeout=30) as resp:
        data2 = json.loads(resp.read().decode("utf-8", "replace"))
    wikitext = data2.get("parse", {}).get("wikitext", {}).get("*", "")
    print("Wikitext (first 1000 chars):")
    print(wikitext[:1000])
except Exception as e:
    print(f"Parse error: {e}")
