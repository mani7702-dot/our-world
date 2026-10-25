#!/usr/bin/env python3
"""Download image with browser UA to assets/images/."""
import urllib.request
import sys

BROWSER_UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

slug = "2026-10-25-bona-trust-teamwork-kenya-business"
url = "https://upload.wikimedia.org/wikipedia/commons/4/47/Business_Bay_Square_%28BBS_Mall%29.jpg"

# Download to assets/images/<slug>.jpg
dest = f"/home/ubuntu/our-world/assets/images/{slug}.jpg"
req = urllib.request.Request(url, headers={"User-Agent": BROWSER_UA, "Referer": "https://commons.wikimedia.org/"})
resp = urllib.request.urlopen(req, timeout=30)
data = resp.read()
with open(dest, 'wb') as f:
    f.write(data)
print(f"Downloaded {len(data)} bytes to {dest}")
