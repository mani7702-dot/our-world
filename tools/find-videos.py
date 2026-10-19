import io, os, re, json, time, subprocess, urllib.parse
API = "https://commons.wikimedia.org/w/api.php"
UA = "OurWorldSite/1.0 (contact: andugulamani722@gmail.com)"
VQ = {
    "axolotl-facts-never-grows-up": "axolotl",
    "how-do-bees-make-honey": "bee honeycomb",
    "how-do-volcanoes-work": "volcano eruption",
    "how-does-an-octopus-change-color": "octopus",
    "how-do-birds-know-where-to-go": "birds flock",
    "what-is-the-milky-way": "milky way timelapse",
    "why-do-clouds-float": "clouds timelapse",
    "bronze-whaler-shark-busan-canal": "shark aquarium",
    "cheetah-cub-cam-five-cubs": "cheetah",
    "million2": None,
}

def cj(params):
    u = API + "?" + urllib.parse.urlencode(params)
    for _ in range(3):
        r = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, u], capture_output=True, text=True).stdout.strip()
        if r:
            try:
                d = json.loads(r)
                if "error" in d:
                    time.sleep(25)
                    continue
                return d
            except Exception:
                pass
        time.sleep(8)
    return None

def pick(pid, pg):
    ii = (pg.get("imageinfo") or [{}])[0]
    mime = ii.get("mime", "")
    url = ii.get("url", "")
    if mime != "video/webm" or not url.endswith(".webm"):
        return None
    size = (ii.get("size") or 0)
    if size > 30 * 1024 * 1024:
        return None
    return url, size

got = 0
for dirpath, _, files in sorted(os.walk("content")):
    for fn in sorted(files):
        if not fn.endswith(".md"):
            continue
        fp = os.path.join(dirpath, fn)
        slug = fn[:-3]
        t = io.open(fp, encoding="utf-8").read()
        if re.search(r"^video:", t, re.M):
            continue
        q = VQ.get(slug)
        if not q:
            continue
        print("QUERY", q)
        d = cj({"action": "query", "format": "json", "generator": "search",
                "gsrsearch": q + " filetype:video", "gsrnamespace": "6", "gsrlimit": "15",
                "prop": "imageinfo", "iiprop": "url|mime|size"})
        time.sleep(6)
        if not d:
            continue
        pages = (d.get("query", {}) or {}).get("pages", {}) or {}
        chosen = None
        for pid, pg in pages.items():
            r = pick(pid, pg)
            if r:
                chosen = r
                break
        if not chosen:
            print("  no usable video for", slug)
            continue
        url, size = chosen
        t2 = re.sub(r"^(image_caption\d?:\s*.+)$",
                    r"\1\nvideo: " + url, t, count=1, flags=re.M)
        if t2 == t:
            t2 = t.replace("\n---\n", "\nvideo: " + url + "\n---\n", 1)
        if t2 == t:
            print("  no anchor for", slug)
            continue
        io.open(fp, "w", encoding="utf-8", newline="").write(t2)
        got += 1
        print("  OK video %s (%d MB)" % (slug, size // 1048576))
print("VIDEOS ADDED:", got)
