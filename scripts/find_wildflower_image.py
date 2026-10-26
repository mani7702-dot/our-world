#!/usr/bin/env python3
"""Find a CC-BY/CC0 image on Wikimedia Commons for a given slug/topic."""
import sys, os, json, time, urllib.parse, subprocess, urllib.request

API = "https://commons.wikimedia.org/w/api.php"
UA = "OurWorldSite/1.0 (contact: andugulamani722@gmail.com)"
BAD_EXT = (".svg", ".tif", ".tiff", ".gif", ".gz", ".webm", ".ogg", ".ogv", ".pdf")
OK_MIME = ("image/jpeg", "image/png")
OK_LICENSE = ("public domain", "cc0", "cc by")

def curl_json(params):
    url = API + "?" + urllib.parse.urlencode(params)
    for _ in range(3):
        p = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, url],
                           capture_output=True, text=True)
        out = p.stdout.strip()
        if not out:
            time.sleep(8)
            continue
        try:
            d = json.loads(out)
            if "error" in d:
                time.sleep(15)
                continue
            return d
        except Exception:
            time.sleep(8)
    return None

def ok_license(l):
    l = l.lower()
    return any(k in l for k in OK_LICENSE) and "nc" not in l and "nd" not in l

def extract_metadata(data, slug, out_path):
    pages = (data.get("query", {}) or {}).get("pages", {}) or {}
    for pid, pg in pages.items():
        ii = (pg.get("imageinfo") or [{}])[0]
        mime = ii.get("mime", "")
        url = ii.get("thumburl") or ii.get("url", "")
        meta = ii.get("extmetadata", {}) or {}
        lic = (meta.get("LicenseShortName", {}) or {}).get("value", "")
        desc = (meta.get("ImageDescription", {}) or {}).get("value", "")
        artist = (meta.get("Artist", {}) or {}).get("value", "")
        credit = (meta.get("Credit", {}) or {}).get("value", "")
        if mime not in OK_MIME:
            continue
        if any(url.lower().endswith(b) for b in BAD_EXT):
            continue
        if not ok_license(lic):
            continue
        # Download
        print(f"  Candidate: {url}")
        print(f"  License: {lic}, MIME: {mime}")
        print(f"  Description: {desc[:200]}")
        print(f"  Artist: {artist[:200]}")
        print(f"  Credit: {credit[:200]}")
        return url, lic, mime, desc, artist, credit
    return None

# Search for wildflower meadow images
queries = [
    "wildflower meadow England native pollinator",
    "wildflower meadow UK native plants bee butterfly",
    "meadow wildflowers bees butterflies England",
]

for q in queries:
    print(f"\nSearching: {q}")
    data = curl_json({
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": q,
        "gsrnamespace": "6",
        "gsrlimit": "20",
        "prop": "imageinfo",
        "iiprop": "url|mime|extmetadata",
        "iiurlwidth": "1200",
    })
    time.sleep(6)
    if not data:
        print("  No data")
        continue
    result = extract_metadata(data, "wildflower", "assets/images/2026-10-26-kings-lynn-wildflower-meadow-buzzing-with-life.jpg")
    if result:
        url, lic, mime, desc, artist, credit = result
        ext = "jpg"
        out = f"assets/images/2026-10-26-kings-lynn-wildflower-meadow-buzzing-with-life.{ext}"
        os.makedirs("assets/images", exist_ok=True)
        # Download
        p = subprocess.run(["curl", "-s", "--max-time", "60", "-A", UA, url],
                            capture_output=True)
        img = p.stdout
        if img and len(img) > 5000:
            with open(out, "wb") as f:
                f.write(img)
            print(f"\n  DOWNLOADED: {out} ({len(img)} bytes)")
            # Build caption
            caption_parts = []
            if desc:
                caption_parts.append(desc[:200])
            if artist:
                caption_parts.append(f"Photo: {artist[:150]}")
            else:
                caption_parts.append("Photo: Wikimedia Commons")
            caption_parts.append(lic)
            full_caption = " / ".join(caption_parts) + " / Wikimedia Commons"
            print(f"  Caption: {full_caption}")
            sys.exit(0)
        else:
            print(f"  Download too small ({len(img)} bytes)")
    else:
        print("  No suitable image found in this query")

print("\nFAILED to find a suitable image")
