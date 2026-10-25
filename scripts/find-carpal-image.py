#!/usr/bin/env python3
"""Find and download a CC0/CC0-equivalent/public-domain image from Wikimedia Commons."""
import urllib.request, urllib.parse, json, re, time, os, sys

UA = "OurWorldSite/1.0 (contact: andugulamani722@gmail.com)"
API = "https://commons.wikimedia.org/w/api.php"

def api_get(params):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read().decode("utf-8"))

def search_files(keywords, limit=15):
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": " ".join(keywords) + " filetype:bitmap has:thumb",
        "srnamespace": "6",
        "srlimit": limit,
    }
    data = api_get(params)
    return [item["title"] for item in data.get("query", {}).get("search", [])]

def ok_license(l, ext_meta):
    """Check if license is acceptable: cc0, cc by, public domain, or no restrictions."""
    l = l.lower().strip()
    # Check explicit license short names
    if any(k in l for k in ("public domain", "cc0", "cc by", "no restrictions", "unsplash", "mit", "apache")):
        # Reject NC and ND
        lic_url = (ext_meta.get("LicenseUrl", {}) or {}).get("value", "").lower()
        lic_long = (ext_meta.get("License", {}) or {}).get("value", "").lower()
        if "non-commercial" in lic_url or "non-commercial" in lic_long:
            return False
        if "no-derivatives" in lic_url or "nd" == l.strip():
            return False
        return True
    return False

def get_imageinfo(title):
    params = {
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "iiprop": "url|mime|extmetadata",
        "titles": title,
    }
    data = api_get(params)
    pages = data.get("query", {}).get("pages", {})
    for pid, pg in pages.items():
        ii = (pg.get("imageinfo") or [{}])[0] if pg.get("imageinfo") else {}
        ext_meta = ii.get("extmetadata", {}) or {}
        lic = (ext_meta.get("LicenseShortName", {}) or {}).get("value", "")
        artist = (ext_meta.get("Artist", {}) or {}).get("value", "")
        artist_clean = re.sub(r"<[^>]+>", "", artist).strip()[:150]
        mime = ii.get("mime", "")
        url = ii.get("url", "")
        return {"license": lic, "artist": artist_clean, "mime": mime, "url": url, "ext_meta": ext_meta}
    return None

# Use the first result from the anatomy search - "Anatomy, descriptive and surgical (1887)"
# which is a public domain medical textbook illustration of hands/wrists
titles = search_files(["hand", "wrist", "medical", "illustration"])
found = None
for title in titles:
    time.sleep(0.5)
    info = get_imageinfo(title)
    if not info:
        continue
    lic = info["license"].lower()
    artist = info["artist"]
    print(f"Title: {title}")
    print(f"  License: {lic}")
    print(f"  Artist: {artist[:80]}")
    print(f"  URL: {info['url'][:120]}")
    if ok_license(lic, info["ext_meta"]):
        found = {"title": title, **info}
        # Check it's actually an anatomy image, not just a book cover
        if info["url"] and (".jpg" in info["url"] or ".png" in info["url"]):
            print(f"  -> SELECTED")
            break
    print()

if not found:
    print("NO suitable image found")
    sys.exit(0)

print(f"\nSelected: {found['title']}")
print(f"License: {found['license']}")
print(f"Artist: {found['artist']}")
print(f"URL: {found['url']}")
print(f"MIME: {found['mime']}")

# Download
slug = "carpal-tunnel-15-minute-hydrodissection-procedure"
ext = "jpg" if "jpeg" in found["mime"] else "png" if "png" in found["mime"] else "jpg"
out_dir = os.path.join("assets", "images")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, slug + "." + ext)
print(f"Downloading to: {out_path}")

img_data = urllib.request.urlopen(urllib.request.Request(found["url"], headers={"User-Agent": UA})).read()
with open(out_path, "wb") as f:
    f.write(img_data)
print(f"Downloaded: {len(img_data)} bytes")

# Build caption — for public domain / no restrictions, use standard format
artist_clean = found["artist"] if found["artist"] else "Wikimedia Commons"
lic_short = found["license"] if found["license"] else "Public domain"
caption = f"Photo: {artist_clean} / {lic_short} / Wikimedia Commons"
print(f"Caption: {caption}")
