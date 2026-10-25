#!/usr/bin/env python3
"""Download the full-res image to assets and verify it's a narwhal."""
import urllib.request, os
from PIL import Image

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
url = "https://upload.wikimedia.org/wikipedia/commons/6/66/FieldMuseum.jpg"
outpath = "assets/images/_check_narwhal_full.jpg"
req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://commons.wikimedia.org/"})
with urllib.request.urlopen(req, timeout=30) as resp:
    data = resp.read()
    with open(outpath, "wb") as f:
        f.write(data)
    print(f"Downloaded {len(data)} bytes to {outpath}")

img = Image.open(outpath)
print(f"Dimensions: {img.size}, Mode: {img.mode}")
os.remove(outpath)
print("Cleaned up check file.")
