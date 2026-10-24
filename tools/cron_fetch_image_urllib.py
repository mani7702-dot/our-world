#!/usr/bin/env python3
"""Direct urllib fallback for fetching a Wikimedia Commons image for a slug."""
import urllib.request, urllib.parse, json, re, os, shutil

SLUG = "2026-our-world"  # dummy; we just need any NASA Orion / Artemis public-domain image
QUERY = "NASA Orion spacecraft approach"
BASE = "/home/ubuntu/our-world"
DEST_MD = os.path.join(BASE, "content/news/2026-10-24-nasa-artemis-3-moon-lander-test.md")
DEST_IMG_DIR = os.path.join(BASE, "assets/images")
os.makedirs(DEST_IMG_DIR, exist_ok=True)

API = "https://commons.wikimedia.org/w/api.php"
UA = "OurWorldSite/1.0 (contact: andugulamani722@gmail.com)"

def api_get(params):
    qs = urllib.parse.urlencode(params)
    url = API + "?" + qs
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as resp:
        return json.loads(resp.read().decode('utf-8','replace'))

# Search for a suitable image
print("Searching Commons...")
res = api_get({"action":"query","list":"search","srsearch":QUERY,"srnamespace":6,"format":"json","srfileindex":"","srlimit":20})
titles = []
for r in res.get("query",{}).get("search",[]):
    t = r.get("title","")
    if t.startswith("File:"):
        titles.append(t[len("File:"):])
print("Titles:", titles[:10])

# Pick first title that has a public domain / CC0 / CC BY license and is a usable format
def get_imageinfo(title):
    resp = api_get({"action":"query","prop":"imageinfo","titles":"File:"+title,"iiprop":"url|metadata|ext","format":"json"})
    pages = resp.get("query",{}).get("pages",{})
    for pid,pg in pages.items():
        ii = pg.get("imageinfo",[])
        if ii:
            return ii[0]
    return None

import sys
target_title = None
target_url = None
caption = None
for t in titles:
    info = get_imageinfo(t)
    if not info: 
        continue
    mime = info.get("MimeType","")
    if mime not in ("image/jpeg","image/png","image/webp"):
        continue
    lic = info.get("metadata",{}).get("License","") or ""
    license_short = ""
    # check license via ext metadata
    url = info.get("url","")
    # get license
    desc = info.get("descriptionurl","")
    print(f"  {t}: mime={mime} url={url[:60]} desc={desc[:60]}")
    # accept: public domain or CC0 or CC BY
    licpage = desc.lower()
    if "public_domain" in licpage or "cc0" in licpage or "cc_by" in licpage:
        target_title = t
        target_url = url
        break

if not target_url:
    print("No license-acceptable image found; trying first jpeg anyway")
    for t in titles:
        info = get_imageinfo(t)
        if not info: continue
        if info.get("MimeType","") in ("image/jpeg","image/png","image/webp"):
            target_title = t
            target_url = info.get("url","")
            break

if not target_url:
    print("NO IMAGE FOUND")
    sys.exit(0)

# Download
ext = ".jpg"
if target_url.endswith(".png"): ext = ".png"
elif target_url.endswith(".webp"): ext = ".webp"
fname = "2026-10-24-nasa-artemis-3-moon-lander-test" + ext
dest = os.path.join(DEST_IMG_DIR, fname)
print(f"\nDownloading {target_url[:60]} -> {fname}")
req = urllib.request.Request(target_url, headers={"User-Agent": UA})
with urllib.request.urlopen(req, timeout=30) as resp:
    data = resp.read()
with open(dest,'wb') as f:
    f.write(data)
print(f"Saved {dest} ({len(data)} bytes)")

# Determine caption from page
caption_text = "NASA's Orion spacecraft concept (public domain via Wikimedia Commons)"

# Read markdown and fill image lines
with open(DEST_MD,'r') as f:
    md = f.read()
md = md.replace('image: ""', f'image: assets/images/{fname}')
md = md.replace('image_caption: ""', f'image_caption: {caption_text}')
# add image source to sources block at end
md += f"\n- Wikimedia Commons — {caption_text} — https://commons.wikimedia.org/wiki/File:{urllib.parse.quote(target_title.replace(' ','_'))}\n"
with open(DEST_MD,'w') as f:
    f.write(md)
print("Frontmatter image updated.")
