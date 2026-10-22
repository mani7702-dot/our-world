#!/usr/bin/env python3
import json, subprocess, urllib.parse, time

API = "https://commons.wikimedia.org/w/api.php"
UA = "OurWorldSite/1.0 (contact: andugulamani722@gmail.com)"

# Try several query terms for the extratropical cyclone
queries = [
    "extratropical cyclone Iceland",
    "extratropical cyclone satellite",
    "NOAA-21 VIIRS",
    "comma cloud satellite",
    "storm clouds comma",
    "cyclone cloud pattern",
    "North Atlantic storm satellite",
]

for q in queries:
    params = urllib.parse.urlencode({
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": "file:" + q, "gsrnamespace": "6", "gsrlimit": "15",
        "prop": "imageinfo", "iiprop": "url|mime|extmetadata", "iiurlwidth": "1200"
    })
    url = API + "?" + params
    result = subprocess.run(["curl", "-s", "--compressed", "--max-time", "20", "-A", UA, url],
                          capture_output=True, text=True)
    try:
        d = json.loads(result.stdout)
        pages = (d.get("query", {}) or {}).get("pages", {}) or {}
        print(f"\n=== Query: '{q}' — {len(pages)} pages ===")
        for pid, pg in pages.items():
            ii = (pg.get("imageinfo") or [{}])[0]
            mime = ii.get("mime", "")
            img_url = ii.get("thumburl") or ii.get("url", "")
            meta = ii.get("extmetadata", {}) or {}
            lic = (meta.get("LicenseShortName", {}) or {}).get("value", "")
            title = pg.get("title", "")
            print(f"  title={title[:60]}, mime={mime}, lic={lic}")
            print(f"  url={img_url[:100]}")
            if "public domain" in lic.lower() or "cc0" in lic.lower() or ("cc by" in lic.lower() and "nc" not in lic.lower() and "nd" not in lic.lower()):
                if "image/jpeg" in mime or "image/png" in mime or "image/webp" in mime:
                    print(f"  *** USABLE ***")
                    break
    except Exception as e:
        print(f"Query '{q}' error: {e}")
    time.sleep(3)
