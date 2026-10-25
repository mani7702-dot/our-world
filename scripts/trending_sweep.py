#!/usr/bin/env python3
"""Trending lane saturation sweep — checks ALL ScienceDaily top.xml candidates with meaningful dedup."""
import subprocess, gzip, xml.etree.ElementTree as ET, re, os, json

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
BLOCK = ("war", "attack", "death toll", "killed", "murder", "court", "lawsuit", "covid",
         "pandemic", "election", "politic", "terror", "bomb", "shooting", "coronavirus")

def fetch(url):
    p = subprocess.run(["curl","-s","--max-time","25","-A",UA,url], capture_output=True)
    data = p.stdout
    if data[:2] == b"\x1f\x8b":
        data = gzip.decompress(data)
    # Strip after </rss>
    idx = data.rfind(b"</rss>")
    if idx > 0:
        data = data[:idx+7]
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
        out.append({"title": t, "link": l})
    return out

def topic_keycheck(title, existing_files):
    """Check if this title's specific topic is already covered.
    Extract distinctive nouns (not common words), require 3+ to match."""
    stopwords = {"the","and","for","with","this","that","from","have","are","was","has","his","her",
                 "their","our","your","a","an","in","on","to","of","at","by","it","is","as","be",
                 "or","not","but","if","when","what","how","why","which","who","will","may","can",
                 "new","study","scientists","research","discover","reveal","suggest","propose","find",
                 "linked","risk","disease","health","may","could","first","earth","could"}
    all_words = re.findall(r'\b[A-Za-z]+\b', title.lower())
    core = [k for k in all_words if len(k) >= 5 and k not in stopwords and not k.isdigit()]
    # Use the most distinctive 2-3 keywords
    distinctive = core[:3] if len(core) >= 3 else core
    if not distinctive:
        return [], True  # can't check
    matches = []
    for fname in existing_files:
        if not fname.endswith(".md"):
            continue
        path = os.path.join("content/news/", fname)
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read().lower()
            matched = sum(1 for k in distinctive if k in text)
            if matched >= 2:  # 2+ of our distinctive keywords
                matches.append(fname)
        except:
            continue
    return distinctive, matches

# Load existing files
existing_files = sorted(os.listdir("content/news/"))

data = fetch("https://www.sciencedaily.com/rss/top.xml")
items = parse(data)
print(f"Total items: {len(items)}")

fresh = []
for it in items:
    blocked = any(b in it["title"].lower() for b in BLOCK)
    distinctive, dups = topic_keycheck(it["title"], existing_files)
    if blocked:
        status = "BLOCKED"
    elif dups:
        status = "DUPE"
    else:
        status = "FRESH"
        fresh.append(it)
    
    print(f"[{status}] {it['title'][:80]}")
    print(f"  link: {it['link'][:100]}")
    if dups:
        print(f"  matched: {dups[:3]}")

print(f"\n=== SUMMARY ===")
print(f"FRESH candidates: {len(fresh)}")
for f in fresh:
    print(f"  {f['title']} | {f['link']}")
