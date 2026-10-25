#!/usr/bin/env python3
"""Custom Wikimedia Commons image search with progressive broadening (no filetype/has:thumb restriction).
Designed for our-world-site trendling lane article image fetch.
"""
import urllib.request, urllib.parse, json, time, os, re, sys

API = "https://commons.wikimedia.org/w/api.php"
UA = "OurWorldSite/1.0 (contact: andugulamani722@gmail.com) Mozilla/5.0"

OK_LICENSE = ("public domain", "cc0", "cc by", "no restrictions")
BAD_EXT = (".svg", ".tif", ".tiff", ".gif", ".gz", ".webm", ".ogg", ".ogv", ".pdf")

def api(params):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read().decode("utf-8"))

def search_files(keywords, limit=15):
    search_term = keywords
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": search_term,
        "srnamespace": "6",
        "srlimit": limit,
    }
    try:
        data = api(params)
    except Exception as e:
        print(f"  search error: {e}")
        return []
    return [item["title"] for item in data.get("query", {}).get("search", [])]

def get_imageinfo(title):
    params = {
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "iiprop": "url|mime|extmetadata",
        "titles": title,
        "iiurlwidth": "1200",
    }
    try:
        data = api(params)
    except Exception as e:
        print(f"  info error for {title}: {e}")
        return None
    pages = data.get("query", {}).get("pages", {})
    for pid, pg in pages.items():
        ii = (pg.get("imageinfo") or [{}])[0] if pg.get("imageinfo") else {}
        thumb_url = ii.get("thumburl", "")
        full_url = ii.get("url", "")
        url = thumb_url or full_url
        mime = ii.get("mime", "")
        meta = ii.get("extmetadata", {}) or {}
        lic = (meta.get("LicenseShortName", {}) or {}).get("value", "")
        artist = (meta.get("Artist", {}) or {}).get("value", "")
        artist_clean = re.sub(r"<[^>]+>", "", artist).strip()
        # Extract creator name from cleaned artist
        if not artist_clean:
            artist_clean = "Wikimedia Commons"
        license_url = (meta.get("LicenseUrl", {}) or {}).get("value", "")
        return {"title": title, "url": url, "mime": mime, "license": lic,
                "artist": artist_clean, "license_url": license_url}
    return None

def ok_license(lic):
    l = lic.lower()
    return any(k in l for k in OK_LICENSE) and "nc" not in l and "nd" not in l

def download(url, path):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        resp = urllib.request.urlopen(req, timeout=60)
        data = resp.read()
        if len(data) < 1000:
            return None
        with open(path, "wb") as f:
            f.write(data)
        return len(data)
    except Exception as e:
        print(f"  download error {url}: {e}")
        return None

def main():
    slug = sys.argv[1] if len(sys.argv) > 1 else "test"
    # Progressive broadening queries
    keyword_sets = [
        "Spinosaurus dinosaur swimming underwater paleoart",
        "Spinosaurus swimming river",
        "Spinosaurus dinosaur",
    ]
    found = []
    for ks in keyword_sets:
        print(f"Searching: {ks}")
        titles = search_files(ks, 10)
        time.sleep(2)
        for t in titles:
            ii = get_imageinfo(t)
            time.sleep(1)
            if ii and ii["mime"] not in ("image/jpeg", "image/png", "image/webp"):
                continue
            if any(t.lower().endswith(b) for b in BAD_EXT):
                continue
            if not ok_license(ii["license"]):
                continue
            found.append(ii)
        if found:
            break
        time.sleep(2)

    if not found:
        print("NO usable images found across all queries")
        return

    best = found[0]
    print(f"\nBest match: {best['title']}")
    print(f"  License: {best['license']}")
    print(f"  Artist: {best['artist'][:120]}")
    print(f"  URL: {best['url']}")

    ext = "jpg" if best["mime"].endswith("jpeg") else "png" if best["mime"].endswith("png") else "webp"
    outpath = os.path.join("assets/images", slug + "." + ext)
    size = download(best["url"], outpath)
    if size:
        print(f"Downloaded: {outpath} ({size} bytes)")
        print(f"CAPTION: {best['artist']} / {best['license']} / Wikimedia Commons")
    else:
        print("Download failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
