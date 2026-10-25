import urllib.request, json, time, os
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36'

queries = [
    "dwarf reed snake Pseudorabdion",
    "Pseudorabdion saravacense",
    "reed snake rolling",
    "dwarf snake southeast asia",
]

def search(q):
    url = "https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=" + urllib.request.quote(q) + "&srnamespace=6&srlimit=10&format=json"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    data = json.loads(urllib.request.urlopen(req, timeout=30).read().decode())
    return data.get("query", {}).get("search", [])

def info(title):
    url = "https://commons.wikimedia.org/w/api.php?action=query&prop=imageinfo&iiprop=url|metadata&titles=" + urllib.request.quote(title) + "&format=json"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    data = json.loads(urllib.request.urlopen(req, timeout=30).read().decode())
    pages = data.get("query", {}).get("pages", {})
    for pid, pg in pages.items():
        return pg.get("imageinfo", [{}])[0] if pg.get("imageinfo") else None

found = []
for q in queries:
    print(f"--- query: {q}")
    for r in search(q):
        title = r.get("title")
        # skip non-files or obvious non-images
        if not title:
            continue
        time.sleep(0.5)
        img = info(title)
        if not img:
            continue
        url = img.get("url")
        meta_raw = img.get("metadata", [])
        lic = json.dumps(meta_raw)
        ok = ("public domain" in lic or "cc0" in lic or "cc by" in lic or "no restrictions" in lic)
        print(f"  {title} | ok={ok} | {url}")
        if ok:
            found.append((title, url, img))
    time.sleep(1.5)

print("\n=== ACCEPTABLE ===")
for title, url, img in found:
    print(f"{title}\n  {url}")
