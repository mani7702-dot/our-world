#!/usr/bin/env python3
# Tirith-safe raw RSS fallback parser: downloads a feed file with curl --compressed,
# parses ALL <item> titles+links+descriptions, applies guardrails + stable-token dupe grep.
# Reuses the file-based ElementTree pattern (no shell curl | python3 pipe).
import subprocess, sys, os, re
import xml.etree.ElementTree as ET

UA = "Mozilla/5.0 (OurWorld raw-fallback; contact andugulamani722@gmail.com)"
FEEDS = {
    "world": [
        "https://feeds.bbci.co.uk/news/world/rss.xml",
    ],
    "science": [
        "https://www.sciencedaily.com/rss/top.xml",
        "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
    ],
}

BLOCKWORDS = ("war","attack","death toll","killed","murder","court","lawsuit","covid",
              "pandemic","election","politic","terror","bomb","shooting","terrorism",
              "invasion","conflict","battle","military","troop","siege","strike dead")

def download(url, path):
    r = subprocess.run(["curl","-s","--compressed","--max-time","25","-A",UA,url,"-o",path],
                       capture_output=True)
    return os.path.exists(path) and os.path.getsize(path) > 0

def parse(path):
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError:
        return []
    items = []
    for it in root.iter("item"):
        t = (it.findtext("title") or "").strip()
        if len(t) < 25:
            continue
        items.append({"title": t,
                      "link": (it.findtext("link") or "").strip(),
                      "desc": (it.findtext("description") or "").strip()[:220]})
    return items

def grep_dup(title):
    # grep BOTH content dirs for title (case-insensitive substring) - catches literal dups
    # also extract stable core tokens for same-story-different-slug detection
    safe = re.sub(r'[^a-zA-Z0-9 ]', ' ', title.lower())
    words = [w for w in safe.split() if len(w) >= 5]  # 5+ char tokens only
    hits = []
    for d in ("content/blog","content/news"):
        if not os.path.isdir(d):
            continue
        for f in os.listdir(d):
            if not f.endswith(".md"):
                continue
            fp = os.path.join(d,f)
            try:
                txt = open(fp, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue
            if title.lower() in txt.lower()[:400]:  # title near top (frontmatter)
                hits.append(fp + " [TITLE-MATCH]")
                continue
            mc = sum(1 for w in words if w in txt.lower())
            if mc >= 3:
                hits.append(fp + f" [tokens={mc}]")
    return hits

def main():
    cat = sys.argv[1] if len(sys.argv) > 1 else "world"
    out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/raw-candidates.tsv"
    paths = []
    for i, url in enumerate(FEEDS.get(cat, [])):
        p = f"/tmp/feed-{cat}-{i}.xml"
        if download(url, p):
            paths.append(p)
            print(f"downloaded {url} -> {p}")
        else:
            print(f"FAILED download {url}")
    items = []
    for p in paths:
        items += parse(p)
    print(f"total items parsed: {len(items)}")
    # abort pass
    writers = open(out, "w", encoding="utf-8")
    writers.write("status\ttitle\tlink\tdesc\n")
    fresh = []
    for it in items:
        t = it["title"]
        tl = t.lower()
        if any(b in tl for b in BLOCKWORDS):
            writers.write(f"BLOCK\t{t}\t{it['link']}\t{it['desc']}\n")
            continue
        d = grep_dup(t)
        if d:
            writers.write(f"DUP\t{t}\t{it['link']}\t{it['desc']}\n  -> matches: {d[:2]}\n")
            continue
        writers.write(f"FRESH\t{t}\t{it['link']}\t{it['desc']}\n")
        fresh.append(it)
    writers.close()
    print(f"\nFRESH candidates: {len(fresh)}")
    for it in fresh[:15]:
        print(f"  FRESH: {it['title']}  | {it['link']}")

if __name__ == "__main__":
    main()
