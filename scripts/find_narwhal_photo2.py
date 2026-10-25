#!/usr/bin/env python3
"""Find actual modern narwhal photos. Use search to look for JPEG photos."""
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

# Use the search with more specific filters for photos
# Commons search syntax: we can use "narwhal" and look for recent photos
# Let's try searching with "intitle:narwhal" to get files actually named narwhal
keyword_sets = [
    "narwhal intitle:narwhal",
    "narwhal",
    "Monodon monoceros",
]

for i, kw in enumerate(keyword_sets):
    print(f"Query {i+1}: {kw}")
    params = {
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": kw, "gsrnamespace": "6", "gsrlimit": "30",
        "prop": "imageinfo", "iiprop": "url|mime|extmetadata|metadata",
        "iiurlwidth": "1600",
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
        if not url:
            continue
        if mime not in ("image/jpeg", "image/png"):
            continue
        meta = ii.get("extmetadata", {}) or {}
        lic = (meta.get("LicenseShortName", {}) or {}).get("value", "")
        title = pg.get("title", "").replace("File:", "").strip()
        if not ok_license(lic):
            continue
        # Skip historical/illustration files by title keywords
        skip_terms = ["coenen", "visboek", "folio", "etching", "drawing", "illustration", 
                      "engraving", "lithograph", "sketch", "chart", "codex", "manuscript",
                      "specimen", "taxidermy", "museum", "17th", "19th century", "vintage",
                      "wellcome", "plate", "atlas"]
        if any(term in title.lower() for term in skip_terms):
            print(f"  SKIP: {title}")
            continue
        # Also check description
        desc_raw = (meta.get("Description", {}) or {}).get("value", "")
        desc = re.sub(r"<[^>]+>", " ", desc_raw).strip().lower()
        if any(term in desc for term in ["illustration", "etching", "drawing", "17th century", "19th century", 
                                          "historical", "manuscript", "codex", "wellcome"]):
            print(f"  SKIP (desc): {title}")
            continue
        artist = re.sub(r"<[^>]+>", "", (meta.get("Artist", {}) or {}).get("value", "")).strip()
        print(f"  CANDIDATE: {title}")
        print(f"    License: {lic} | Artist: {artist[:60]}")
        size = download(url, f"assets/images/_test_narwhal.jpg")
        time.sleep(1.0)
        if size > 100000:
            from PIL import Image
            img = Image.open("assets/images/_test_narwhal.jpg")
            print(f"    Size: {size} bytes | Dimensions: {img.size}")
            if img.size[0] >= 800 and img.size[1] >= 800:
                os.rename("assets/images/_test_narwhal.jpg", f"assets/images/2026-10-25-narwhal-tusk-double-helix.jpg")
                print(f"    KEPT!")
                found = True
                break
            else:
                print(f"    Too small dimensions")
                os.remove("assets/images/_test_narwhal.jpg")
        else:
            if os.path.exists("assets/images/_test_narwhal.jpg"):
                os.remove("assets/images/_test_narwhal.jpg")
    if found:
        break
    print("  No suitable photo found for this query.")
else:
    print("\nNO modern photo found. Will use etching/fallback.")
