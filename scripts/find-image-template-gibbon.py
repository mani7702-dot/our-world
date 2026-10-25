#!/usr/bin/env python3
"""
find-image-template-gibbon.py — Gibbon image fetch with progressive keyword broadening.
Uses browser UA, progressive queries, time.sleep(1.5) between calls,
accepts "no restrictions" license, downloads with browser UA to avoid 403.
"""
import urllib.request, urllib.parse, json, time, re, os, html

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
API = "https://commons.wikimedia.org/w/api.php"

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
        if not ok_license(lic):
            continue
        artist = (meta.get("Artist", {}) or {}).get("value", "")
        artist = html.unescape(re.sub(r'<[^>]+>', '', str(artist)))[:200] if artist else ""
        return {"url": url, "mime": mime, "license": lic, "title": pg.get("title", ""), "artist": artist}
    return None

def main():
    slug = "2026-10-25-international-gibbon-day-saves-tiny-primates"
    outpath = f"assets/images/{slug}.jpg"
    os.makedirs("assets/images", exist_ok=True)

    keyword_sets = [
        ["gibbon", "Hylobates", "swing", "tree", "Borneo"],
        ["gibbon", "swing", "tree", "forest"],
        ["gibbon", "ape", "sitting", "branch"],
        ["gibbon", "animal", "ape"],
        ["gibbon", "swing", "forest"],
    ]

    for i, kw in enumerate(keyword_sets):
        print(f"Query {i+1}: {kw}")
        result = search_and_pick(kw)
        time.sleep(1.5)
        if result:
            print(f"  Found: {result['title']}")
            print(f"  License: {result['license']}")
            print(f"  Artist: {result.get('artist', '')}")
            print(f"  URL: {result['url']}")
            size = download(result["url"], outpath)
            if size > 0:
                print(f"  Downloaded: {size} bytes to {outpath}")
                artist = result.get("artist", "")
                artist_clean = artist or "Wikimedia Commons contributor"
                if artist_clean and (not artist_clean.lower().startswith("wikimedia")):
                    print(f"  Image file: {slug}.jpg")
                    print(f"  Caption: {artist_clean} / {result['license']} / Wikimedia Commons")
                else:
                    print(f"  Image file: {slug}.jpg")
                    print(f"  Caption: Photo by {artist_clean} / {result['license']} / Wikimedia Commons")
                print(f"  IMAGE_PATH: assets/images/{slug}.jpg")
                return 0
            else:
                print("  Download failed, trying next query...")
        else:
            print("  No suitable image found for this query.")

    print("NO usable image found across all queries.")
    return 1

if __name__ == "__main__":
    exit(main())
