#!/usr/bin/env python3
"""Fetch trending lane candidates from fallback feeds and evaluate for kid-safety + dedup."""
import subprocess, gzip, xml.etree.ElementTree as ET, re, os

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

BLOCK = ("war", "attack", "death toll", "killed", "murder", "court", "lawsuit", "covid",
         "pandemic", "election", "politic", "terror", "bomb", "shooting", "coronavirus")

URLS = [
    ("ScienceDaily top", "https://www.sciencedaily.com/rss/top.xml"),
]

def fetch(url):
    p = subprocess.run(["curl","-s","--max-time","25","-A",UA,url], capture_output=True)
    data = p.stdout
    if data[:2] == b"\x1f\x8b":
        data = gzip.decompress(data)
    return data

def parse(data):
    try:
        root = ET.fromstring(data)
    except ET.ParseError:
        return []
    out = []
    for it in root.iter("item"):
        t = (it.findtext("title") or "").strip()
        l = (it.findtext("link") or "").strip()
        d = (it.findtext("description") or "").strip()[:200]
        blocked = any(b in t.lower() for b in BLOCK)
        out.append({"title": t, "link": l, "desc": d, "blocked": blocked})
    return out

def dedup_check(slug, title):
    """Grep full content/news/ for topic keywords."""
    # Extract core nouns from title
    keywords = re.findall(r'\b[A-Za-z]+\b', title.lower())
    # Take meaningful nouns (3+ chars, non-stopwords)
    stopwords = {"the","and","for","with","this","that","from","have","are","was","has","his","her","their","our","your","a","an","in","on","to","of","at","by","it","is","as","be","or","not","but","if","when","what","how","why","which","who","will"}
    core = [k for k in keywords if len(k) >= 4 and k not in stopwords]
    matches = []
    news_dir = "content/news/"
    for fname in sorted(os.listdir(news_dir)):
        if fname.endswith(".md"):
            path = os.path.join(news_dir, fname)
            try:
                with open(path, encoding="utf-8") as f:
                    text = f.read().lower()
                # Check if 3+ keywords match in the file
                matched = sum(1 for k in core if k in text)
                if matched >= 3:
                    matches.append(fname)
            except Exception:
                continue
    return core, matches

for name, url in URLS:
    print(f"=== {name} ===")
    data = fetch(url)
    print(f"  bytes: {len(data)}")
    items = parse(data)
    print(f"  items: {len(items)}")
    for i, it in enumerate(items[:20]):
        slug = re.sub(r'[^a-z0-9]+', '-', it['title'].lower()).strip('-')[:60]
        core, dups = dedup_check(slug, it['title'])
        status = "BLOCKED" if it['blocked'] else ("DUPE" if dups else "FRESH")
        print(f"  [{status}] {it['title'][:80]}")
        print(f"    slug: {slug}")
        print(f"    link: {it['link'][:120]}")
        if dups:
            print(f"    dups: {dups[:3]}")
        if status == "FRESH":
            print(f"    KEYWORDS: {core}")
