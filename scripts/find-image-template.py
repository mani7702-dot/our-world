#!/usr/bin/env python3
"""Custom multi-query Wikimedia Commons search with progressive broadening.
Template: copy and modify for any topic where commons-fallback-query.py returns empty.

Key differences from commons-fallback-query.py:
  1. Runs 2-3 progressive broadening queries (not just one)
  2. Does NOT use restrictive search modifiers (no 'filetype:bitmap has:thumb')
  3. Adds time.sleep(1-2) between API calls to avoid HTTP 429
  4. Sets browser User-Agent on BOTH API calls AND image downloads (avoids 403)
  5. Accepts 'no restrictions' as a license (in addition to public domain, cc0, cc by)

Usage: python3 scripts/find-image-template.py <SLUG> <keyword1 keyword2 ...>
"""
import urllib.request, urllib.parse, json, re, time, io, os, sys

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
API = "https://commons.wikimedia.org/w/api.php"
OK_LICENSE = ("public domain", "cc0", "cc by", "no restrictions")
BAD_EXT = (".svg", ".tif", ".tiff", ".gif", ".gz", ".webm", ".ogg", ".ogv", ".pdf")
OK_MIME = ("image/jpeg", "image/png", "image/webp")

def ok_license(l):
    l = l.lower()
    return any(k in l for k in OK_LICENSE) and "nc" not in l and "nd" not in l

def search_and_info(keywords, limit=10):
    """Search Commons without restrictive modifiers, then fetch imageinfo for each."""
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
    time.sleep(1.5)

    results = []
    for item in data.get("query", {}).get("search", []):
        title = item["title"]
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
        except Exception:
            continue
        time.sleep(1.5)

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

def download_image(url, out_path):
    """Download image with browser UA to avoid Wikimedia 403."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    img = urllib.request.urlopen(req, timeout=60).read()
    io.open(out_path, "wb").write(img)
    return len(img)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 find-image-template.py <SLUG> <keyword1 keyword2 ...>")
        sys.exit(1)
    slug = sys.argv[1]
    keywords = sys.argv[2:]

    # Progressive broadening: specific -> broad
    queries = [
        keywords,                          # e.g. ["Chandrayaan-1", "PSLV", "launch"]
        keywords[:3] if len(keywords) >= 3 else keywords,
        keywords[:2] if len(keywords) >= 2 else keywords,
    ]

    all_results = []
    for q in queries:
        print(f"Query: {' '.join(q)}")
        results = search_and_info(q, limit=15)
        for r in results:
            lic_ok = ok_license(r["license"])
            print(f"  {r['title']} | mime={r['mime']} | license={r['license']} | ok={lic_ok}")
            if lic_ok:
                all_results.append(r)
        time.sleep(2)

    if not all_results:
        print("\nNo acceptable licensed images found. Will publish without image.")
    else:
        print(f"\nFound {len(all_results)} acceptable images.")
        best = all_results[0]
        ext = "jpg" if "jpeg" in best["mime"] else "png" if "png" in best["mime"] else "webp"
        out_path = os.path.join("assets/images", slug + "." + ext)
        print(f"Downloading best: {best['title']}")
        try:
            size = download_image(best["url"], out_path)
            caption = f"Photo: {best['artist']} / {best['license']} / Wikimedia Commons"
            caption = re.sub(r"\s+", " ", caption).strip()
            print(f"Saved to: {out_path} ({size} bytes)")
            print(f"Caption: {caption}")
        except Exception as e:
            print(f"Download failed: {e} -- trying curl fallback")
            os.system(f'curl -s -o "{out_path}" -H "User-Agent: {UA}" "{best["url"]}"')
            print(f"Saved via curl to: {out_path}")
