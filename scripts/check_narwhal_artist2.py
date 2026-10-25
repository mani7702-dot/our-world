#!/usr/bin/env python3
"""Get author from the Commons file page via API prop=info + description."""
import urllib.request, urllib.parse, json, re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
API = "https://commons.wikimedia.org/w/api.php"

# Try the parse API to get the actual file page wikitext
params = {
    "action": "parse",
    "format": "json",
    "page": "File:Germany Narwhal Unicorn.jpg",
    "prop": "wikitext",
}
url = API + "?" + urllib.parse.urlencode(params)
req = urllib.request.Request(url, headers={"User-Agent": UA})
with urllib.request.urlopen(req, timeout=30) as resp:
    data = json.loads(resp.read().decode("utf-8", "replace"))

wikitext = data.get("parse", {}).get("wikitext", {}).get("*", "")
print("=== WIKITEXT (first 1500 chars) ===")
print(wikitext[:1500])
