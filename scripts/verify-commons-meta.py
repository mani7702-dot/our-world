#!/usr/bin/env python3
"""Verify Commons metadata for the radio telescope image."""
import urllib.request, json, urllib.parse

BASE = "https://commons.wikimedia.org/w/api.php"
HEADERS = {"User-Agent": "OurWorldSite/1.0 (contact: andugulamani722@gmail.com)"}

def api_call(params):
    url = BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=25) as resp:
        return json.loads(resp.read().decode('utf-8', 'ignore'))

# Get pageid via search, then query extmetadata
title = "File:A dipole of UTR-2 radio telescope antenna array and sunset with light pillar.jpg"
data = api_call({
    "action": "query", "format": "json",
    "titles": title, "prop": "imageinfo",
    "iiprop": "url|metadata|extmetadata|mimetype",
    "iiurlwidth": "1200",
})
pages = data.get("query", {}).get("pages", {})
for pid, pg in pages.items():
    ii = (pg.get("imageinfo") or [{}])[0]
    meta = ii.get("extmetadata", {}) or {}
    for key in ("Credit", "Artist", "LicenseShortName", "License", "ImageDescription", "DateTime"):
        v = (meta.get(key, {}) or {}).get("value", "")
        print(f"  {key}: {v[:300]}")
    print(f"  mime: {ii.get('mime','')}")
    print(f"  thumburl: {ii.get('thumburl','')[:200]}")
    print(f"  url: {ii.get('url','')[:200]}")
