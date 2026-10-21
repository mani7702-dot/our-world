#!/usr/bin/env python3
"""Search Wikimedia Commons directly for skin stem cell images with commercial-safe license."""
import urllib.request, json, urllib.parse

API = "https://commons.wikimedia.org/w/api.php"
UA = "OurWorldSite/1.0 (contact: andugulamani722@gmail.com)"

queries = [
    "human skin microscope",
    "skin stem cell",
    "epidermis microscopy",
    "skin cell renewal",
    "connective tissue skin cross-section",
]

for q in queries:
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": "file:" + q,
        "gsrnamespace": "6",
        "gsrlimit": "15",
        "prop": "imageinfo",
        "iiprop": "url|mime|extmetadata|metadata",
        "iiurlwidth": "1200",
    }
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        resp = urllib.request.urlopen(req, timeout=25)
        raw = resp.read().decode("utf-8", errors="replace")
        data = json.loads(raw)
    except Exception as e:
        print(f"QUERY '{q}' -> ERROR: {e}")
        continue
    
    pages = (data.get("query", {}) or {}).get("pages", {}) or {}
    print(f"\nQUERY '{q}' -> {len(pages)} pages found")
    count = 0
    for pid, pg in pages.items():
        ii = (pg.get("imageinfo") or [{}])[0]
        mime = ii.get("mime", "")
        url_val = ii.get("thumburl") or ii.get("url", "")
        meta = ii.get("extmetadata", {}) or {}
        lic = (meta.get("LicenseShortName", {}) or {}).get("value", "")
        lic_url = (meta.get("LicenseURL", {}) or {}).get("value", "")
        title = pg.get("title", "")
        
        if mime not in ("image/jpeg", "image/png", "image/webp"):
            continue
        if not lic or "public domain" not in lic.lower() and "cc0" not in lic.lower() and "cc by" not in lic.lower():
            continue
        if "nc" in lic.lower() or "nd" in lic.lower():
            continue
        if not url_val:
            continue
        print(f"  OK: {title}")
        print(f"    mime: {mime}, license: {lic}, url: {url_val[:120]}")
        count += 1
    if count == 0:
        print("  NO usable images")
