#!/usr/bin/env python3
"""
Find a high-res actual photo of a narwhal (not a building) for the article.
Uses browser UA, progressive keyword broadening, time.sleep between calls.
"""
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

# Get the file page description via props to verify it's a narwhal
def get_description(filename):
    params = {
        "action": "query",
        "format": "json",
        "titles": f"File:{filename}",
        "prop": "imageinfo",
        "iiprop": "extmetadata",
    }
    data = api_call(params)
    pages = (data.get("query", {}) or {}).get("pages", {}) or {}
    for pid, pg in pages.items():
        meta = pg.get("extmetadata", {}) or {}
        desc = (meta.get("Description", {}) or {}).get("value", "")
        # Strip HTML tags
        desc_text = re.sub(r"<[^>]+>", " ", desc).strip()
        return desc_text.lower()
    return ""

slug = "2026-10-25-narwhal-tusk-double-helix"
outpath = f"assets/images/{slug}.jpg"

# Search specifically for narwhal photos
keyword_sets = [
    ["narwhal" + " \"Monodon monoceros\"" + " photo"],
    ["narwhal" + " photo" + " " + "tusk"],
    ["narwhal" + " Arctic" + " " + "whale" + " " + "photo"],
]

for i, kw in enumerate(keyword_sets):
    print(f"Query {i+1}: {kw}")
    params = {
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": " ".join(kw), "gsrnamespace": "6", "gsrlimit": "25",
        "prop": "imageinfo", "iiprop": "url|mime|extmetadata",
        "iiurlwidth": "1600",
    }
    data = api_call(params)
    time.sleep(1.5)
    if not data:
        continue
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
        title = pg.get("title", "").replace("File:", "").strip()
        if not ok_license(lic):
            continue
        # Check description for narwhal
        desc = get_description(title)
        time.sleep(0.5)
        # Skip if it's clearly about a building/museum
        if "museum" in title.lower() or "museum" in desc or "building" in desc:
            continue
        # Must mention narwhal in title or description
        if "narwhal" in title.lower() or "narwhal" in desc:
            artist_raw = (meta.get("Artist", {}) or {}).get("value", "")
            artist = re.sub(r"<[^>]+>", "", artist_raw).strip()
            print(f"  Found: {title}")
            print(f"  License: {lic}")
            print(f"  Artist: {artist[:80]}")
            print(f"  Desc: {desc[:150]}")
            print(f"  URL: {url[:100]}")
            size = download(url, outpath)
            if size > 50000:
                print(f"  Downloaded: {size} bytes to {outpath}")
                # Verify file
                from PIL import Image
                img = Image.open(outpath)
                print(f"  Dimensions: {img.size}")
                print(f"  Image file: {slug}.jpg")
                print(f"  Caption: Photo: {artist or 'Wikimedia Commons'} / {lic} / Wikimedia Commons")
                # Update frontmatter caption
                break
            else:
                print(f"  Downloaded too small: {size} bytes, trying next")
                if size > 0:
                    os.remove(outpath)
    else:
        print("  No suitable image found for this query.")
        continue
    break
else:
    print("NO usable image found across all queries.")
    exit(1)
