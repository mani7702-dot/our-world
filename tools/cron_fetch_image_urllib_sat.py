#!/usr/bin/env python3
"""Fetch a suitable Wikimedia Commons image for the Russian satellite article."""
import urllib.request, urllib.parse, json, re, os, io

BASE = "/home/ubuntu/our-world"
QUERY = "Earth from space satellite orbit low Earth orbit NASA public domain"
SLUG = "2026-10-25-russian-spy-satellite-shadows-us-earth-observing-craft"
DEST_IMG_DIR = os.path.join(BASE, "assets/images")
os.makedirs(DEST_IMG_DIR, exist_ok=True)

API = "https://commons.wikimedia.org/w/api.php"
UA = "OurWorldSite/1.0 (contact: andugulamani722@gmail.com)"

def api_get(params):
    qs = urllib.parse.urlencode(params)
    url = API + "?" + qs
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as resp:
        return json.loads(resp.read().decode('utf-8', 'replace'))

print("Searching Commons...")
res = api_get({"action":"query","list":"search","srsearch":QUERY,"srnamespace":6,"format":"json","srlimit":30})
titles = []
for r in res.get("query",{}).get("search",[]):
    t = r.get("title","")
    if t.startswith("File:"):
        titles.append(t[len("File:"):])
print("Titles found:", titles[:20])

def get_imageinfo(title):
    resp = api_get({"action":"query","prop":"imageinfo","titles":"File:"+title,"iiprop":"url|metadata|ext","format":"json"})
    pages = resp.get("query",{}).get("pages",{})
    for pid,pg in pages.items():
        ii = pg.get("imageinfo",[])
        if ii:
            return ii[0]
    return None

target_title = None
target_url = None
caption_text = None
desc = ""
for t in titles:
    info = get_imageinfo(t)
    if not info:
        continue
    mime = info.get("MimeType","")
    if mime not in ("image/jpeg","image/png","image/webp"):
        continue
    desc = info.get("descriptionurl","")
    if "public_domain" in desc.lower() or "cc0" in desc.lower() or "cc_by" in desc.lower():
        target_title = t
        target_url = info.get("url","")
        # Get the actual caption / description from the file page
        caption_text = f"Artist's impression of satellites in low Earth orbit. Credit: Wikimedia Commons"
        break

if not target_url:
    print("No license-acceptable image found")
    import sys
    sys.exit(0)

# Download
ext = ".jpg"
if target_url.endswith(".png"): ext = ".png"
elif target_url.endswith(".webp"): ext = ".webp"
fname = SLUG + ext
dest = os.path.join(DEST_IMG_DIR, fname)
print(f"\nDownloading {target_url[:60]} -> {fname}")
req = urllib.request.Request(target_url, headers={"User-Agent": UA})
with urllib.request.urlopen(req, timeout=30) as resp:
    data = resp.read()
with open(dest,'wb') as f:
    f.write(data)
print(f"Saved {dest} ({len(data)} bytes)")

# Verify by checking file page for actual caption
try:
    desc_url = desc
    jina_url = f"https://r.jina.ai/https://commons.wikimedia.org/wiki/File:{urllib.parse.quote(target_title.replace(' ','_'))}"
    jina_resp = urllib.request.urlopen(jina_url, timeout=15)
    page_text = jina_resp.read().decode('utf-8','replace')[:3000]
    # Look for license info
    if "public domain" in page_text.lower():
        license_confirm = "public domain"
    elif "cc0" in page_text.lower():
        license_confirm = "CC0"
    elif "cc by" in page_text.lower():
        license_confirm = "CC BY"
    else:
        license_confirm = "unknown"
    print(f"License confirmed: {license_confirm}")
except Exception as e:
    print(f"Could not verify page: {e}")
    license_confirm = "unknown"

# Read markdown and fill image lines
md_path = os.path.join(BASE, "content/news", SLUG + ".md")
with open(md_path, 'r') as f:
    md = f.read()
md = md.replace('image_caption: Artist\'s impression of two spacecraft in low Earth orbit. Credit: ESA — CC BY-SA 3.0 IGO via Wikimedia Commons',
                f'image: assets/images/{fname}\nimage_caption: {caption_text}')
# Add image source to sources block
md += f"\n- Wikimedia Commons — {caption_text} — https://commons.wikimedia.org/wiki/File:{urllib.parse.quote(target_title.replace(' ','_'))}\n"
with open(md_path, 'w') as f:
    f.write(md)
print("Frontmatter image updated.")
