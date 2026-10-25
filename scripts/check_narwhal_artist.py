#!/usr/bin/env python3
"""Get the proper artist/attribution for the Germany Narwhal Unicorn image."""
import urllib.request, urllib.parse, json, re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
API = "https://commons.wikimedia.org/w/api.php"

params = {
    "action": "query",
    "format": "json",
    "titles": "File:Germany Narwhal Unicorn.jpg",
    "prop": "imageinfo",
    "iiprop": "extmetadata",
}
url = API + "?" + urllib.parse.urlencode(params)
req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
with urllib.request.urlopen(req, timeout=30) as resp:
    data = json.loads(resp.read().decode("utf-8", "replace"))

pages = data.get("query", {}).get("pages", {})
for pid, pg in pages.items():
    meta = pg.get("extmetadata", {}) or {}
    lic = (meta.get("LicenseShortName", {}) or {}).get("value", "")
    artist_raw = (meta.get("Artist", {}) or {}).get("value", "")
    artist = re.sub(r"<[^>]+>", "", artist_raw).strip()
    desc = re.sub(r"<[^>]+>", " ", (meta.get("Description", {}) or {}).get("value", "")).strip()
    print(f"Artist: {artist}")
    print(f"License: {lic}")
    print(f"Description: {desc[:300]}")
    print(f"\nCaption: Photo: {artist} / {lic} / Wikimedia Commons")
