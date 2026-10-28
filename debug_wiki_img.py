#!/usr/bin/env python3
"""Debug the Wikimedia API search for Portia fimbriata images."""
import urllib.parse, json, subprocess

QUERY = "Portia fimbriata jumping spider sleep REM stage eye movement twitch arachnid spider dreaming research University of Bonn PNAS"
API = "https://commons.wikimedia.org/w/api.php"
UA = "OurWorldSite/1.0 (contact: andugulamani722@gmail.com)"

params = {
    "action": "query",
    "format": "json",
    "generator": "search",
    "gsrsearch": QUERY,
    "gsrnamespace": "6",
    "gsrlimit": "15",
    "prop": "imageinfo",
    "iiprop": "url|mime|extmetadata",
    "iiurlwidth": "1200"
}

url = API + "?" + urllib.parse.urlencode(params)
print(f"URL: {url[:200]}...")

result = subprocess.run(
    ["curl", "-s", "--max-time", "30", "-A", UA, url],
    capture_output=True, text=True
)
print(f"curl exit: {result.returncode}")
print(f"Response length: {len(result.stdout)}")

data = json.loads(result.stdout)
pages = (data.get("query", {}) or {}).get("pages", {}) or {}
print(f"\nFound {len(pages)} pages")

OK_MIME = ("image/jpeg", "image/png", "image/webp")
BAD_EXT = (".svg", ".tif", ".tiff", ".gif", ".gz", ".webm", ".ogg", ".ogv", ".pdf")

for pid, pg in pages.items():
    ii = (pg.get("imageinfo") or [{}])[0]
    mime = ii.get("mime", "")
    url = ii.get("thumburl") or ii.get("url", "")
    meta = ii.get("extmetadata", {}) or {}
    lic = (meta.get("LicenseShortName", {}) or {}).get("value", "")
    title = pg.get("title", "")

    # Replicate ok_license logic
    lic_lower = lic.lower()
    ok_lic = any(k in lic_lower for k in ("public domain", "cc0", "cc by")) and "nc" not in lic_lower and "nd" not in lic_lower
    ok_mime = mime in OK_MIME
    bad_ext = any(url.lower().endswith(b) for b in BAD_EXT)

    passes = ok_mime and ok_lic and not bad_ext
    print(f"\n  Title: {title}")
    print(f"  MIME: {mime}, License: {lic}")
    print(f"    ok_mime={ok_mime}, ok_lic={ok_lic}, bad_ext={bad_ext}")
    print(f"    PASSES: {passes}")
    print(f"    URL: {url[:120]}")
