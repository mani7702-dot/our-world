#!/usr/bin/env python3
"""
find_golden_coral_image_v2.py — Better targeted image search.
Try: coral reef, deep sea coral, brittle star, ROV, Schmidt Ocean Institute, etc.
"""
import urllib.request
import urllib.parse
import json
import time
import re
import os
import html

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
API = "https://commons.wikimedia.org/w/api.php"

SLUG = "2026-10-26-golden-tree-coral-costa-rica"
OUTDIR = "assets/images"
os.makedirs(OUTDIR, exist_ok=True)

def api_call(params):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode('utf-8', 'replace'))
    except Exception as e:
        print(f"  API error: {e}")
        return None

def ok_license(lic):
    l = lic.lower()
    if "nc" in l or "nd" in l:
        return False
    return any(k in l for k in ("public domain", "cc0", "cc by", "no restrictions"))

def clean_caption(artist_value):
    if not artist_value:
        return ""
    text = re.sub(r'<[^>]+>', '', artist_value)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def download(url, outpath):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://commons.wikimedia.org/"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            with open(outpath, "wb") as f:
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
        "gsrlimit": "20",
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
        if not ok_license(lic):
            continue
        artist = (meta.get("Artist", {}) or {}).get("value", "")
        artist_clean = clean_caption(artist)
        return {
            "url": url,
            "mime": mime,
            "license": lic,
            "title": pg.get("title", ""),
            "artist": artist_clean,
        }
    return None

# More targeted keyword sets for coral / deep sea / marine biology
keyword_sets = [
    # Deep sea coral specifically
    ["deep sea coral", "yellow"],
    ["deep water coral", "Lophelia"],
    ["deep-sea coral", "gorgonian"],
    ["octocoral", "deep"],
    ["sea fan", "deep water"],
    [" coral", "deep ocean", "ROV"],
    ["brittle star", "deep sea"],
    [" seamount", "deep sea", "coral"],
    ["deep sea", "coral", "Costa Rica"],
]

outpath = f"{OUTDIR}/{SLUG}.jpg"

for i, kw in enumerate(keyword_sets):
    print(f"Query {i+1}: {kw}")
    result = search_and_pick(kw)
    time.sleep(1.5)
    if result:
        print(f"  Found: {result['title']}")
        print(f"  License: {result['license']}")
        print(f"  Artist/credit: {result['artist'][:100]}")
        size = download(result["url"], outpath)
        if size > 0:
            print(f"  Downloaded: {size} bytes to {outpath}")
            if result["url"].endswith(".png"):
                newpath = outpath.replace(".jpg", ".png")
                os.rename(outpath, newpath)
                outpath = newpath
                print(f"  Renamed to {outpath}")
            artist_clean = result["artist"] if result["artist"] else "Wikimedia Commons"
            lic = result["license"]
            with open(f"{SLUG}.imginfo", "w") as f:
                f.write(f"url={result['url']}\n")
                f.write(f"artist={artist_clean}\n")
                f.write(f"license={lic}\n")
                f.write(f"title={result['title']}\n")
                f.write(f"outpath={outpath}\n")
            exit(0)
        else:
            print("  Download failed, trying next query...")
    else:
        print("  No suitable image found for this query.")

print("\nNO usable image found across all queries.")
exit(1)
