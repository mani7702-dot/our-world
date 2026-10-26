#!/usr/bin/env python3
"""Verify Commons image metadata for the wildflower meadow image."""
import json, urllib.parse, subprocess

API = "https://commons.wikimedia.org/w/api.php"
UA = "OurWorldSite/1.0 (contact: andugulamani722@gmail.com)"
params = {
    "action": "query",
    "format": "json",
    "titles": "File:Allesley Village Jubilee Nature Reserve - geograph.org.uk - 761967.jpg",
    "prop": "imageinfo",
    "iiprop": "url|mime|extmetadata",
    "iiurlwidth": "1200",
}
url = API + "?" + urllib.parse.urlencode(params)
p = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, url], capture_output=True, text=True)
d = json.loads(p.stdout)
pages = d.get("query", {}).get("pages", {})
for pid, pg in pages.items():
    ii = pg.get("imageinfo", [{}])[0]
    meta = ii.get("extmetadata", {})
    lic = meta.get("LicenseShortName", {}).get("value", "")
    desc = meta.get("ImageDescription", {}).get("value", "")
    artist = meta.get("Artist", {}).get("value", "")
    credit = meta.get("Credit", {}).get("value", "")
    mime = ii.get("mime", "")
    print("License:", lic)
    print("MIME:", mime)
    print("Description:", desc[:300])
    print("Artist:", artist[:200])
    print("Credit:", credit[:200])
    print("Thumb URL:", ii.get("thumburl", "")[:150])
