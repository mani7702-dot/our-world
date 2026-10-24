#!/usr/bin/env python3
"""Direct urllib fallback: download NASA Orion image from Wikimedia Commons (confirmed PD)."""
import urllib.request, urllib.parse, os

BASE = "/home/ubuntu/our-world"
DEST_MD = os.path.join(BASE, "content/news/2026-10-24-nasa-artemis-3-moon-lander-test.md")
DEST_IMG_DIR = os.path.join(BASE, "assets/images")
os.makedirs(DEST_IMG_DIR, exist_ok=True)
UA = "OurWorldSite/1.0 (contact: andugulamani722@gmail.com)"

# Confirmed public-domain NASA image
IMG_URL = "https://upload.wikimedia.org/wikipedia/commons/6/6c/NASA%E2%80%99s_Orion_spacecraft_approaching_the_robotic_asteroid_capture_vehicle.jpg"
IMG_NAME = "2026-10-24-nasa-artemis-3-moon-lander-test.jpg"
CAPTION = "NASA\u2019s Orion spacecraft in a concept artwork (public domain, PD-USGov, via Wikimedia Commons)"
CREDIT_URL = "https://commons.wikimedia.org/wiki/File:NASA%E2%80%99s_Orion_spacecraft_approaching_the_robotic_asteroid_capture_vehicle.jpg"

dest = os.path.join(DEST_IMG_DIR, IMG_NAME)
print(f"Downloading -> {dest}")
req = urllib.request.Request(IMG_URL, headers={"User-Agent": UA})
with urllib.request.urlopen(req, timeout=30) as resp:
    data = resp.read()
with open(dest, 'wb') as f:
    f.write(data)
print(f"Saved {dest} ({len(data)} bytes)")

# Verify file is a real image (not an error page)
if os.path.getsize(dest) < 1000:
    print("WARNING: file too small, likely HTML error")
    raise SystemExit(1)

# Update markdown frontmatter + add source credit
with open(DEST_MD, 'r') as f:
    md = f.read()

md = md.replace('image: ""', f'image: assets/images/{IMG_NAME}')
md = md.replace('image_caption: ""', f'image_caption: {CAPTION}')

# add image credit to Sources block
if CREDIT_URL not in md:
    md = md.replace(
        "- NASA Artemis — https://www.nasa.gov/specials/artemis-iii/",
        f"- NASA Artemis — https://www.nasa.gov/specials/artemis-iii/\n- Wikimedia Commons (public domain, PD-USGov) — {CAPTION} — {CREDIT_URL}"
    )
with open(DEST_MD, 'w') as f:
    f.write(md)
print("Frontmatter + sources updated.")
