#!/usr/bin/env python3
"""Custom multi-query Wikimedia Commons search for Chandrayaan-1 images.
Progressive broadening to avoid the restrictive modifiers in commons-fallback-query.py.
"""
import urllib.request, urllib.parse, json, re, time, io, os

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
API = "https://commons.wikimedia.org/w/api.php"
SLUG = "2026-10-25-on-this-day-india-launches-chandrayaan-1-first-moon-mission"
OK_LICENSE = ("public domain", "cc0", "cc by", "no restrictions")
BAD_EXT = (".svg", ".tif", ".tiff", ".gif", ".gz", ".webm", ".ogg", ".ogv", ".pdf")
OK_MIME = ("image/jpeg", "image/png", "image/webp")

def ok_license(l):
    l = l.lower()
    return any(k in l for k in OK_LICENSE) and "nc" not in l and "nd" not in l

def search(keywords, limit=10):
    """Search Commons WITHOUT restrictive modifiers."""
    params = urllib.parse.urlencode({
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": " ".join(keywords),
        "srnamespace": "6",
        "srlimit": str(limit),
    })
    req = urllib.request.Request(API + "?" + params, headers={"User-Agent": UA})
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"  search error: {e}")
        return []
    time.sleep(1.5)  # rate limit
    
    results = []
    for item in data.get("query", {}).get("search", []):
        title = item["title"]
        # Get image info
        info_params = urllib.parse.urlencode({
            "action": "query",
            "format": "json",
            "prop": "imageinfo",
            "iiprop": "url|mime|extmetadata",
            "titles": title,
        })
        info_req = urllib.request.Request(API + "?" + info_params, headers={"User-Agent": UA})
        try:
            info_resp = urllib.request.urlopen(info_req, timeout=30)
            info_data = json.loads(info_resp.read().decode())
        except Exception as e:
            continue
        time.sleep(1.5)  # rate limit
        
        pages = info_data.get("query", {}).get("pages", {})
        for pid, pg in pages.items():
            ii = pg.get("imageinfo", [{}])[0] if pg.get("imageinfo") else {}
            mime = ii.get("mime", "")
            url = ii.get("thumburl") or ii.get("url", "")
            meta = ii.get("extmetadata", {}) or {}
            lic = meta.get("LicenseShortName", {}).get("value", "")
            artist = meta.get("Artist", {}).get("value", "")
            artist_clean = re.sub(r"<[^>]+>", "", artist).strip()
            if mime in OK_MIME and not any(url.lower().endswith(b) for b in BAD_EXT):
                results.append({
                    "title": title,
                    "url": url,
                    "mime": mime,
                    "license": lic,
                    "artist": artist_clean,
                })
    return results

# Progressive broadening queries
queries = [
    ["Chandrayaan-1", "PSLV", "launch", "ISRO", "moon mission"],
    ["Chandrayaan-1", "ISRO", "moon spacecraft"],
    ["Chandrayaan", "moon", "ISRO"],
]

all_results = []
for q in queries:
    print(f"Query: {' '.join(q)}")
    results = search(q, limit=15)
    for r in results:
        lic_ok = ok_license(r["license"])
        print(f"  {r['title']} | mime={r['mime']} | license={r['license']} | ok={lic_ok} | url={r['url'][:80]}")
        if lic_ok:
            all_results.append(r)
    time.sleep(2)

if not all_results:
    print("\nNo acceptable licensed images found across all queries.")
    print("Will publish without image.")
else:
    print(f"\nFound {len(all_results)} acceptable images.")
    # Pick the first acceptable one
    best = all_results[0]
    ext = "jpg" if "jpeg" in best["mime"] else "png" if "png" in best["mime"] else "webp"
    out_path = os.path.join("assets/images", SLUG + "." + ext)
    print(f"\nDownloading best: {best['title']}")
    req = urllib.request.Request(best["url"], headers={"User-Agent": UA})
    img = urllib.request.urlopen(req, timeout=60).read()
    if img:
        io.open(out_path, "wb").write(img)
        # Clean caption
        caption = f"Photo: {best['artist']} / {best['license']} / Wikimedia Commons"
        caption = re.sub(r"\s+", " ", caption).strip()
        print(f"Saved to: {out_path}")
        print(f"Caption: {caption}")
    else:
        print("Download failed!")
