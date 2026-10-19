import io, os, re, json, time, subprocess, urllib.parse
API = "https://commons.wikimedia.org/w/api.php"
UA = "OurWorldSite/1.0 (contact: andugulamani722@gmail.com)"
BAD = (".svg", ".tif", ".tiff", ".gif", ".gz", ".webm", ".ogg", ".ogv", ".pdf")
OKM = ("image/jpeg", "image/png", "image/webp")
NOISE = {"why","how","do","does","for","are","in","on","of","to","we","you","they","it","is","the","a","an","what","that","this","its","your","our","when","make","made","get","and","but","howitworks","have","can","their"}
Q = {
    "axolotl-facts-never-grows-up": "axolotl",
    "tardigrade-facts-water-bear": "tardigrade",
    "bear-bread-farmers-market-aspen": "black bear",
    "bronze-whaler-shark-busan-canal": "shark",
    "cheetah-cub-cam-five-cubs": "cheetah cubs",
    "manhattan-barn-owls-water-tower": "barn owl",
    "nasa-moon-base-cave-search": "lunar cave",
    "orangutans-return-borneo-wild": "orangutan",
    "record-breaking-crayfish-tennessee": "crayfish",
    "roman-telescope-best-inventions-2026": "Nancy Grace Roman Space Telescope",
    "webb-brown-dwarf-weather": "brown dwarf",
}

def lic_ok(l):
    l = l.lower()
    return any(k in l for k in ("public domain", "cc0", "cc by")) and "nc" not in l and "nd" not in l

def cj(params):
    u = API + "?" + urllib.parse.urlencode(params)
    for _ in range(3):
        r = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, u], capture_output=True, text=True).stdout.strip()
        if r:
            try:
                d = json.loads(r)
                if "error" in d:
                    time.sleep(25); continue
                return d
            except Exception:
                pass
        time.sleep(8)
    return None

def down(u):
    return subprocess.run(["curl", "-s", "--max-time", "45", "-A", UA, u], capture_output=True).stdout

added = 0
for dirpath, _, files in sorted(os.walk("content")):
    for fn in sorted(files):
        if not fn.endswith(".md"):
            continue
        fp = os.path.join(dirpath, fn)
        slug = fn[:-3]
        t = io.open(fp, encoding="utf-8").read()
        have = re.findall(r"^image\d?:\s*(.+)$", t, re.M)
        need = 3 - len(have)
        if need <= 0:
            continue
        query = Q.get(slug) or " ".join(w for w in re.sub(r"[^a-z ]", " ", slug).split() if w not in NOISE and len(w) > 2) or slug
        print("%-40s want %d more" % (slug, need))
        d = cj({"action": "query", "format": "json", "generator": "search",
                "gsrsearch": "file:" + query, "gsrnamespace": "6", "gsrlimit": "25",
                "prop": "imageinfo", "iiprop": "url|mime|extmetadata", "iiurlwidth": "1200"})
        time.sleep(6)
        if not d:
            print("  no response"); continue
        pages = (d.get("query", {}) or {}).get("pages", {}) or {}
        seen = " ".join(have)
        got = 0
        for pid, pg in pages.items():
            ii = (pg.get("imageinfo") or [{}])[0]
            mime = ii.get("mime", ""); url = ii.get("thumburl") or ii.get("url", "")
            lc = ((ii.get("extmetadata", {}) or {}).get("LicenseShortName", {}) or {}).get("value", "")
            base = url.split("/")[-1].split("?")[0].rsplit(".", 1)[0][:24]
            if mime not in OKM or any(url.lower().endswith(b) for b in BAD) or not lic_ok(lc):
                continue
            if base in seen:
                continue
            ext = "jpg" if mime.endswith("jpeg") else "png" if mime.endswith("png") else "webp"
            idx = "" if (not have and got == 0) else str(len(have) + got)
            out = "assets/images/%s%s.%s" % (slug, idx, ext)
            img = down(url)
            if not img or len(img) < 5000:
                continue
            io.open(out, "wb").write(img)
            t = re.sub(r"^(image_caption:\s*.+)$",
                       r"\1\nimage" + idx + ": " + out.replace("\\", "/") + "\nimage_caption" + idx + ": Photo: Wikimedia Commons",
                       t, count=1, flags=re.M)
            io.open(fp, "w", encoding="utf-8", newline="").write(t)
            seen += " " + base
            got += 1
            added += 1
            print("  OK", out, len(img), lc)
            if got >= need:
                break
print("ADDED:", added)
