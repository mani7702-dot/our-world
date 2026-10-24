#!/usr/bin/env python3
"""Final manual Commons fallback: find + download a PD/CC-BY solar image."""
import io, os, re, ssl, json, urllib.parse, urllib.request
from PIL import Image

API = "https://commons.wikimedia.org/w/api.php"
UA = "OurWorldSite/1.0 (contact: andugulamani722@gmail.com)"
BAD_EXT = (".svg", ".tif", ".tiff", ".gif", ".gz", ".webm", ".ogg", ".pdf")

def sslctx():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def api_json(params):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30, context=sslctx()) as r:
        return json.loads(r.read().decode("utf-8", "ignore"))

def ok_license(l):
    l = l.lower()
    return any(k in l for k in ("public domain", "cc0", "cc by")) and "nc" not in l and "nd" not in l

def find(urls):
    for q in urls:
        data = api_json({"action": "query", "format": "json", "generator": "search",
                         "gsrsearch": q, "gsrnamespace": "6", "gsrlimit": "50",
                         "prop": "imageinfo", "iiprop": "url|mime|extmetadata",
                         "iiurlwidth": "1600"})
        pages = (data.get("query", {}) or {}).get("pages", {}) or {}
        for pid, pg in pages.items():
            ii = (pg.get("imageinfo") or [{}])[0]
            mime = ii.get("mime", "")
            url = ii.get("thumburl") or ii.get("url", "")
            meta = ii.get("extmetadata", {}) or {}
            lic = (meta.get("LicenseShortName", {}) or {}).get("value", "")
            title = pg.get("title", "")
            if mime in ("image/jpeg", "image/png") and url and ok_license(lic) and title:
                return (title, url, mime, lic, meta)
    return None

cand = find(["solar corona magnetic field lines NASA SDO",
             "Sun magnetic field lines corona AIA 171",
             "solar prominence SDO NASA public domain"])
if not cand:
    print("NO usable image found on Commons")
    raise SystemExit(1)
title, url, mime, lic, meta = cand
print("CHOSEN:", title, "mime=", mime, "lic=", lic)
slug = "2026-10-24-suns-hidden-magnetic-web"
ext = "jpg" if mime.endswith("jpeg") else "png"
out = os.path.join("assets/images", slug + "." + ext)

req = urllib.request.Request(url, headers={"User-Agent": UA,
                                           "Referer": "https://commons.wikimedia.org/"})
with urllib.request.urlopen(req, timeout=60, context=sslctx()) as r:
    img_bytes = r.read()
if len(img_bytes) > 2 * 1024 * 1024:
    im = Image.open(io.BytesIO(img_bytes))
    w, h = im.size
    nw = 1600
    nh = int(h * nw / w)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=82, optimize=True)
    img_bytes = buf.getvalue()
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "wb") as f:
    f.write(img_bytes)
print("OK downloaded:", out, len(img_bytes), "bytes")

# build caption credit
artist = (meta.get("Artist", {}) or {}).get("value", "")
artist_clean = re.sub(r"<[^>]+>", "", artist).strip()[:120] if artist else ""
cap = "Photo: " + (artist_clean if artist_clean else "Wikimedia Commons")
cap += " / %s via Wikimedia Commons" % lic
print("CAPTION:", cap)
print("OUT:", out)
