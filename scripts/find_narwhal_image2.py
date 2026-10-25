#!/usr/bin/env python3
"""Scan Commons for actual narwhal photos and list results."""
import urllib.request, urllib.parse, json, time, re, os

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
API = "https://commons.wikimedia.org/w/api.php"

def api_call(params):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8", "replace"))
    except Exception as e:
        print(f"  API error: {e}")
        return None

def ok_license(lic):
    l = lic.lower()
    if "nc" in l or "nd" in l:
        return False
    return any(k in l for k in ("public domain", "cc0", "cc by", "no restrictions"))

def download(url, path):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://commons.wikimedia.org/"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            with open(path, "wb") as f:
                f.write(data)
            return len(data)
    except Exception as e:
        print(f"  Download error: {e}")
        return 0

slug = "2026-10-25-narwhal-tusk-double-helix"
outpath = f"assets/images/{slug}.jpg"

keyword_sets = [
    ["narwhal", "Monodon monoceros", "Arctic"],
    ["narwhal", "tusk", "Arctic"],
    ["narwhal"],
    ["Monodon monoceros"],
]

for i, kw in enumerate(keyword_sets):
    print(f"Query {i+1}: {kw}")
    params = {
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": " ".join(kw), "gsrnamespace": "6", "gsrlimit": "15",
        "prop": "imageinfo", "iiprop": "url|mime|extmetadata",
        "iiurlwidth": "1200",
    }
    data = api_call(params)
    time.sleep(1.5)
    if not data:
        continue
    pages = (data.get("query", {}) or {}).get("pages", {}) or {}
    found = False
    for pid, pg in pages.items():
        ii = (pg.get("imageinfo") or [{}])[0]
        mime = ii.get("mime", "")
        url = ii.get("thumburl") or ii.get("url", "")
        if mime not in ("image/jpeg", "image/png", "image/webp"):
            continue
        if any(url.lower().endswith(ext) for ext in (".svg", ".tif", ".tiff", ".gif", ".pdf")):
            continue
        meta = ii.get("extmetadata", {}) or {}
        lic = (meta.get("LicenseShortName", {}) or {}).get("value", "")
        artist_raw = (meta.get("Artist", {}) or {}).get("value", "")
        artist = re.sub(r"<[^>]+>", "", artist_raw).strip()
        title = pg.get("title", "").replace("File:", "").replace("_", " ")
        if not ok_license(lic):
            continue
        print(f"  Found: {title[:80]}")
        print(f"  License: {lic}")
        print(f"  Artist: {artist[:80]}")
        print(f"  URL: {url}")
        size = download(url, outpath)
        if size > 0:
            print(f"  Downloaded: {size} bytes to {outpath}")
            found = True
            break
        else:
            print("  Download failed, trying next image...")
    if found:
        break
    print("  No suitable image found for this query.")
else:
    print("NO usable image found across all queries.")
