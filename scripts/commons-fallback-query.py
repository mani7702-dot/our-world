# -*- coding: utf-8 -*-
"""
Manual Wikimedia Commons image fallback for slugs missing an image (per skill pitfall).
Usage: python3 scripts/commons-fallback-query.py <SLUG> <QUERY_KEYWORDS>

- Uses Commons API directly (curl -> file -> parse JSON). NO python3 -c pipes.
- generator=search pops file titles; follow-up get_imageinfo call validates mime/license.
- Accepts CC0 / Public domain / CC BY (incl. CC BY-SA). Rejects cc-by-nc, cc-by-nd, non-images.
- Downloads from upload.wikimedia.org with Referer header. Strips ?utm_source= params.
- Resizes >2MB with PIL.
- Patches frontmatter image: + image_caption with creator + license credit.
"""
import sys, os, json, re, subprocess, io, urllib.parse

API = "https://commons.wikimedia.org/w/api.php"
UA = "OurWorldSite/1.0 (contact: andugulamani722@gmail.com)"
REFERER = "https://commons.wikimedia.org/"
BAD_EXT = (".svg", ".tif", ".tiff", ".gif", ".ogg", ".ogv", ".pdf", ".djvu", ".webm")
OK_MIME = ("image/jpeg", "image/png", "image/webp")
# Accept public domain, cc0, cc by (including cc by-sa). Reject nc/nd variants.
REJECT_LICENSE_SUB = ("nc", "nd", "copyright")


def curl(url):
    p = subprocess.run(["curl", "-s", "-L", "--max-time", "30", "-A", UA, url],
                       capture_output=True)
    return p.stdout


def ok_license(lic):
    l = lic.lower()
    if any(s in l for s in REJECT_LICENSE_SUB):
        return False
    return any(k in l for k in ("public domain", "cc0", "cc by"))


def get_imageinfo(titles):
    """Follow-up get_imageinfo to validate mime + license for a list of titles."""
    params = {
        "action": "query", "format": "json", "prop": "imageinfo",
        "titles": "|".join(titles),
        "iiprop": "url|mime|extmetadata", "iiurlwidth": "1200",
    }
    url = API + "?" + urllib.parse.urlencode(params)
    raw = curl(url)
    if not raw:
        return []
    try:
        d = json.loads(raw)
    except Exception:
        return []
    out = []
    pages = (d.get("query", {}) or {}).get("pages", {}) or {}
    for pid, pg in pages.items():
        ii = (pg.get("imageinfo") or [{}])[0]
        mime = ii.get("mime", "")
        thumb = ii.get("thumburl")
        url2 = ii.get("url", "")
        full_url = thumb or url2
        meta = ii.get("extmetadata", {}) or {}
        lic = (meta.get("LicenseShortName", {}) or {}).get("value", "")
        creator = (meta.get("Artist", {}) or {}).get("value", "")
        if mime not in OK_MIME:
            continue
        if any(str(full_url).lower().endswith(b) for b in BAD_EXT):
            continue
        if not ok_license(lic):
            continue
        out.append({"url": full_url, "mime": mime, "license": lic, "creator": creator,
                    "title": pg.get("title", "")})
    return out


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 scripts/commons-fallback-query.py <SLUG> <QUERY_KEYWORDS>")
        sys.exit(1)
    slug = sys.argv[1]
    query = " ".join(sys.argv[2:])

    # Step 1: generator=search to get candidate file titles
    params = {
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": query, "gsrnamespace": "6", "gsrlimit": "20",
        "prop": "imageinfo", "iiprop": "url|mime|extmetadata", "iiurlwidth": "1200",
    }
    url = API + "?" + urllib.parse.urlencode(params)
    raw = curl(url)
    if not raw:
        print("NO response from Commons search for", query)
        sys.exit(2)
    try:
        d = json.loads(raw)
    except Exception as e:
        print("Parse error:", e, repr(raw[:200]))
        sys.exit(3)

    pages = (d.get("query", {}) or {}).get("pages", {}) or {}
    # Some candidates may lack extmetadata from generator=search; collect titles + first-pass
    candidates = []
    titles_missing_meta = []
    for pid, pg in pages.items():
        ii = (pg.get("imageinfo") or [{}])[0]
        mime = ii.get("mime", "")
        full_url = ii.get("thumburl") or ii.get("url", "")
        meta = ii.get("extmetadata", {}) or {}
        lic = (meta.get("LicenseShortName", {}) or {}).get("value", "")
        creator = (meta.get("Artist", {}) or {}).get("value", "")
        title = pg.get("title", "")
        if not title:
            continue
        if mime in OK_MIME and full_url and ok_license(lic) and not any(str(full_url).lower().endswith(b) for b in BAD_EXT):
            candidates.append({"url": full_url, "mime": mime, "license": lic,
                               "creator": creator, "title": title})
        else:
            titles_missing_meta.append(title)

    # Step 2: follow-up get_imageinfo for those lacking validated meta
    if titles_missing_meta:
        candidates += get_imageinfo(titles_missing_meta)

    if not candidates:
        print("NO usable image for", slug)
        sys.exit(4)

    c = candidates[0]
    dl_url = c["url"]
    # strip ?utm_source=... query params (bare path needed)
    dl_url = re.sub(r"\?.*$", "", dl_url)

    img = curl(dl_url)
    # wikimedia needs Referer sometimes; retry with referer header
    if not img or len(img) < 1000:
        p = subprocess.run(["curl", "-s", "-L", "--max-time", "45", "-A", UA,
                            "-e", REFERER, dl_url], capture_output=True)
        img = p.stdout

    if not img or len(img) < 1000:
        print("ERR download", slug)
        sys.exit(5)

    os.makedirs("assets/images", exist_ok=True)
    ext = "jpg" if c["mime"].endswith("jpeg") else "png" if c["mime"].endswith("png") else "webp"
    out = os.path.join("assets/images", slug + "." + ext)

    # Resize if > 2 MB
    try:
        from PIL import Image
        im = Image.open(io.BytesIO(img))
        if im.size[0] > 1600:
            ratio = 1600 / float(im.size[0])
            newh = max(1, int(im.size[1] * ratio))
            im = im.resize((1600, newh), Image.Resampling.LANCZOS)
        im.save(out, "JPEG" if ext == "jpg" else "PNG", quality=82, optimize=True)
    except Exception:
        with open(out, "wb") as f:
            f.write(img)

    # Patch frontmatter image: + image_caption
    fp = os.path.join("content/news", slug + ".md")
    if os.path.exists(fp):
        with open(fp, encoding="utf-8") as f:
            t = f.read()
        caption = "Photo: {}, {} via Wikimedia Commons".format(
            c["creator"] or "Wikimedia Commons", c["license"] or "Creative Commons")
        # Ensure image: path line exists (fixes pitfall: script did not write image: line)
        image_line = f"image: {out}"
        if not re.search(r"^image:\s*\S+", t, re.M):
            t = re.sub(r"^(time:\s*\S+)$", r'\1\n' + image_line, t, count=1, flags=re.M)
        elif not re.search(r"^image:\s*assets/", t, re.M):
            t = re.sub(r"^image:.*$", image_line, t, count=1, flags=re.M)
        # Ensure image_caption: line exists and is fresh
        if re.search(r"^image_caption:", t, re.M):
            t = re.sub(r"^image_caption:.*$", "image_caption: " + caption, t, count=1, flags=re.M)
        else:
            t = re.sub(r"^(time:\s*\S+)$", r'\1\nimage_caption: ' + caption, t, count=1, flags=re.M)
        with open(fp, "w", encoding="utf-8") as f:
            f.write(t)
        print("OK", out, len(img), c["license"])
        print("PATCHED", fp, "caption:")
        print(" ", caption)
    else:
        print("OK", out, len(img), c["license"])
        print("WARN: content file", fp, "not found — image downloaded only")


if __name__ == "__main__":
    main()
