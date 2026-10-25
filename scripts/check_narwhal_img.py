#!/usr/bin/env python3
"""Check the metadata/description of the FieldMuseum narwhal image on Commons."""
import urllib.request, urllib.parse, json, time

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
API = "https://commons.wikimedia.org/w/api.php"

# Get imageinfo for FieldMuseum.jpg - we need the full filename
# The thumb url was: thumb.wikimedia.org/wikipedia/commons/thumb/6/66/FieldMuseum.jpg/1920px-
# So the file is File:FieldMuseum.jpg

params = {
    'action': 'query',
    'format': 'json',
    'titles': 'File:FieldMuseum.jpg',
    'prop': 'imageinfo',
    'iiprop': 'url|mime|extmetadata|metadata',
    'iiurlwidth': '1200',
}
url = API + "?" + urllib.parse.urlencode(params)
req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
with urllib.request.urlopen(req, timeout=30) as resp:
    data = json.loads(resp.read().decode("utf-8", "replace"))

pages = data.get("query", {}).get("pages", {})
for pid, pg in pages.items():
    ii = (pg.get("imageinfo") or [{}])[0]
    print("Title:", pg.get("title"))
    print("Mime:", ii.get("mime"))
    meta = ii.get("extmetadata", {})
    print("Description:", (meta.get("Description", {}).get("value", "") or "")[:200])
    print("Artist:", (meta.get("Artist", {}).get("value", "") or "")[:200])
    print("License:", (meta.get("LicenseShortName", {}).get("value", "") or ""))
    # Get the full URL
    print("Full URL:", ii.get("url", ""))
    print("Thumb URL:", ii.get("thumburl", ii.get("url", "")))
    # Print raw dimensions
    raw = ii.get("metadata", {})
    print("Width:", raw.get("width", "N/A") if isinstance(raw, dict) else "N/A")
    print("Height:", raw.get("height", "N/A") if isinstance(raw, dict) else "N/A")
