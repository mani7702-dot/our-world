#!/usr/bin/env python3
"""Targeted single-slug image fetcher for cron budget.
Searches Wikimedia Commons for a single article, downloads a CC0/PD/CC-BY image,
and inserts image: + image_caption: lines into the markdown frontmatter.
"""
import sys, io, os, re, json, time, urllib.parse, urllib.request

API = "https://commons.wikimedia.org/w/api.php"
UA = "OurWorldSite/1.0 (contact: andugulamani722@gmail.com)"
BAD_EXT = (".svg", ".tif", ".tiff", ".gif", ".gz", ".webm", ".ogg", ".ogv", ".pdf")
OK_MIME = ("image/jpeg", "image/png", "image/webp")
OK_LICENSE = ("public domain", "cc0", "cc by")

def ok_license(l):
    l = l.lower()
    return any(k in l for k in OK_LICENSE) and "nc" not in l and "nd" not in l

def curl_json(params):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for _ in range(3):
        try:
            raw = urllib.request.urlopen(req, timeout=30).read()
            d = json.loads(raw)
            if "error" in d and "429" in str(d.get("error", {})):
                time.sleep(25)
                continue
            return d
        except Exception:
            time.sleep(8)
    return None

def down(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=45).read()

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 scripts/fetch-single-image.py <slug> \"<query>\"")
        sys.exit(1)
    slug = sys.argv[1]
    query = sys.argv[2]

    # Find the article file
    fp = None
    for dirpath, _, files in os.walk("content"):
        for fn in files:
            if fn[:-3] == slug:
                fp = os.path.join(dirpath, fn)
                break
        if fp:
            break

    if not fp:
        print(f"Article not found for slug: {slug}")
        sys.exit(1)

    t = io.open(fp, encoding="utf-8").read()

    # Check if image already exists
    if re.search(r"^image:", t, re.M):
        print(f"  Already has image: {slug}")
        return

    print(f"QUERY {query}")
    data = curl_json({
        "action": "query", "format": "json",
        "generator": "search",
        "gsrsearch": "file:" + query,
        "gsrnamespace": "6", "gsrlimit": "15",
        "prop": "imageinfo", "iiprop": "url|mime|extmetadata", "iiurlwidth": "1200",
    })
    time.sleep(6)

    if not data:
        print(f"  GIVE UP {slug}")
        return

    pages = (data.get("query", {}) or {}).get("pages", {}) or {}
    chosen = None
    for pid, pg in pages.items():
        ii = (pg.get("imageinfo") or [{}])[0]
        mime = ii.get("mime", "")
        url = ii.get("thumburl") or ii.get("url", "")
        meta = ii.get("extmetadata", {}) or {}
        lic = (meta.get("LicenseShortName", {}) or {}).get("value", "")
        if mime not in OK_MIME:
            continue
        if any(url.lower().endswith(b) for b in BAD_EXT):
            continue
        if not ok_license(lic):
            continue
        chosen = (url, mime, lic)
        break

    if not chosen:
        print(f"  NO usable image for {slug}")
        return

    url, mime, lic = chosen
    ext = "jpg" if mime.endswith("jpeg") else "png" if mime.endswith("png") else "webp"
    out = os.path.join("assets/images", slug + "." + ext)

    # Ensure assets/images exists
    os.makedirs("assets/images", exist_ok=True)

    img = down(url)
    if not img:
        print(f"  ERR download {slug}")
        return

    io.open(out, "wb").write(img)
    t2 = re.sub(
        r'^(time:\s*\S+)$',
        r'\1\nimage: ' + out.replace("\\", "/") + '\nimage_caption: Photo: Wikimedia Commons',
        t, count=1, flags=re.M,
    )
    io.open(fp, "w", encoding="utf-8", newline="").write(t2)
    print(f"  OK {out} {len(img)} {lic}")

if __name__ == "__main__":
    main()
