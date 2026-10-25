#!/usr/bin/env python3
"""
Find a CC-licensed image of a narwhal for the 2026-10-25 narwhal tusk article.
Uses browser UA, progressive keyword broadening, time.sleep(1.5) between
Commons API calls to avoid 429, accepts "no restrictions" license, downloads
with browser UA + referer to avoid 403 from the image CDN.
"""
import urllib.request
import urllib.parse
import json
import time
import os

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
API = "https://commons.wikimedia.org/w/api.php"
slug = "2026-10-25-narwhal-tusk-double-helix"
outpath = f"assets/images/{slug}.jpg"
os.makedirs("assets/images", exist_ok=True)


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


def search_and_pick(query_keywords):
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": " ".join(query_keywords),
        "gsrnamespace": "6",
        "gsrlimit": "15",
        "prop": "imageinfo",
        "iiprop": "url|mime|extmetadata",
        "iiurlwidth": "1200",
    }
    data = api_call(params)
    if not data:
        return None
    pages = (data.get("query", {}) or {}).get("pages", {}) or {}
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
        artist = (meta.get("Artist", {}) or {}).get("value", "")
        if not ok_license(lic):
            continue
        return {"url": url, "mime": mime, "license": lic, "title": pg.get("title", ""), "artist": artist}
    return None


# Progressive keyword broadening: specific -> broad
keyword_sets = [
    ["narwhal", "tusk", "Arctic", "whale"],
    ["narwhal", "tusk", "Arctic"],
    ["narwhal", "tusk"],
    ["narwhal"],
    ["Monodon monoceros"],
]

for i, kw in enumerate(keyword_sets):
    print(f"Query {i+1}: {kw}")
    result = search_and_pick(kw)
    time.sleep(1.5)
    if result:
        print(f"  Found: {result['title']}")
        print(f"  License: {result['license']}")
        print(f"  URL: {result['url']}")
        size = download(result["url"], outpath)
        if size > 0:
            print(f"  Downloaded: {size} bytes to {outpath}")
            print(f"  Image file: {slug}.jpg")
            # Strip HTML from artist for caption
            artist = result.get("artist", "")
            artist_clean = artist.replace("File:", "").replace("_", " ")
            # Extract plain text name from any HTML
            import re
            artist_name = re.sub(r'<[^>]+>', '', artist_clean).strip()
            lic_clean = result["license"]
            print(f"  Caption suggestion: Photo: {artist_name} / {lic_clean} / Wikimedia Commons")
            break
        else:
            print("  Download failed, trying next query...")
    else:
        print("  No suitable image found for this query.")
else:
    print("NO usable image found across all queries.")
    exit(1)
