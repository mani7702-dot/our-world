#!/usr/bin/env python3
"""Download a Wikimedia Commons image and save to assets/images/."""
import urllib.request, re, html, sys

url = 'https://upload.wikimedia.org/wikipedia/commons/2/22/Pacific_Walrus_-_Bull_%288247646168%29.jpg'
slug = '2026-10-25-walrus-calf-annautaq-rescue'
out_path = f'assets/images/{slug}.jpg'

req = urllib.request.Request(url, headers={'User-Agent': 'OurWorldSite/1.0 (contact: andugulamani722@gmail.com)'})
resp = urllib.request.urlopen(req, timeout=30)
img_data = resp.read()

import os
os.makedirs('assets/images', exist_ok=True)
with open(out_path, 'wb') as f:
    f.write(img_data)

print(f"Downloaded {len(img_data)} bytes to {out_path}")
print(f"MIME: {resp.headers.get('Content-Type')}")
