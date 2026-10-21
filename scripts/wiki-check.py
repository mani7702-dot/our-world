#!/usr/bin/env python3
"""Cross-check skin biology story with Wikipedia as 2nd source."""
import urllib.request, json

# Wikipedia API for skin stem cells article
url = "https://en.wikipedia.org/api/rest_v1/page/summary/Embryonic_stem_cell"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'OurWorld-picker/1.0 (contact andugulamani722@gmail.com)'})
    resp = urllib.request.urlopen(req, timeout=25)
    data = json.loads(resp.read())
    print("=== Wikipedia: Embryonic stem cell ===")
    print(data.get('extract', '')[:500])
except Exception as e:
    print(f"Wikipedia fetch error: {e}")

# Also try skin renewal article
url2 = "https://en.wikipedia.org/api/rest_v1/page/summary/Epidermis"
try:
    req = urllib.request.Request(url2, headers={'User-Agent': 'OurWorld-picker/1.0 (contact andugulamani722@gmail.com)'})
    resp = urllib.request.urlopen(req, timeout=25)
    data = json.loads(resp.read())
    print("\n=== Wikipedia: Epidermis ===")
    print(data.get('extract', '')[:800])
except Exception as e:
    print(f"Wikipedia fetch error: {e}")
