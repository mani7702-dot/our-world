#!/usr/bin/env python3
"""Download GNN + BBC World raw feeds, find FRESH animal stories."""
import subprocess, xml.etree.ElementTree as ET, os, re

UA = "Mozilla/5.0 (OurWorld raw-fallback; contact andugulamani722@gmail.com)"

existing = {}
for d in ["content/blog", "content/news"]:
    if os.path.isdir(d):
        for f in os.listdir(d):
            if f.endswith(".md"):
                existing[f] = open(os.path.join(d, f), encoding="utf-8", errors="ignore").read().lower()

ANIMAL_KW = ['animal','bear','whale','shark','bird','turtle','dolphin','elephant','monkey','frog','fish',
             'bee','butterfly','snake','rabbit','deer','elk','crocodile','bat','owl','horse','cow','pig',
             'chicken','duck','squirrel','bison','wildlife','habitat','species','nest','migration','reef',
             'coral','mammal','predator','flock','swarm','seal','otter','penguin','cat','dog','pup','kitten',
             'ape','chimp','gorilla','lemur','sloth','armadillo','hedgehog','fox','wolf','lion','tiger','panda']

BLOCK = ("war","attack","death toll","killed","murder","court","lawsuit","covid","pandemic",
         "election","politic","terror","bomb","shooting","military","conflict","invasion","terrorism")
MED = ("cancer","disease","treatment","therapy","diagnos","mental","depression","anxiety","poisoning",
       "medical","patient","clinical")

def is_dup(title):
    tl = title.lower()
    safe = re.sub(r'[^a-zA-Z0-9 ]', ' ', tl)
    words = [w for w in safe.split() if len(w) >= 5]
    for fname, txt in existing.items():
        if tl in txt[:500]:
            return fname + " [TITLE]"
        mc = sum(1 for w in words if w in txt)
        if mc >= 3:
            return fname + f" [tokens={mc}]"
    return None

def parse(url, path):
    r = subprocess.run(["curl", "-s", "--compressed", "--max-time", "25", "-A", UA, url, "-o", path], capture_output=True)
    size = os.path.getsize(path) if os.path.exists(path) else 0
    if size < 500:
        print(f"  SKIP {url}: {size} bytes")
        return []
    try:
        root = ET.parse(path).getroot()
    except:
        print(f"  PARSE ERR {url}")
        return []
    items = []
    for it in root.iter("item"):
        t = (it.findtext("title") or "").strip()
        d = (it.findtext("description") or "").strip()[:300]
        l = (it.findtext("link") or "").strip()
        if len(t) < 25:
            continue
        items.append((t, l, d))
    print(f"  {url}: {len(items)} items")
    return items

print("=== Downloading raw feeds ===")
items = []
items += parse("https://www.goodnewsnetwork.org/feed/", "/tmp/gnn.xml")
items += parse("https://feeds.bbci.co.uk/news/world/rss.xml", "/tmp/bbc_world.xml")

# Dedupe
seen_titles = set()
uniq = []
for t, l, d in items:
    key = t.lower()
    if key in seen_titles:
        continue
    seen_titles.add(key)
    uniq.append((t, l, d))

print(f"\nTotal unique items: {len(uniq)}")
print("\n=== FRESH ANIMAL-RELEVANT STORIES ===")
for t, l, d in uniq:
    tl = t.lower()
    if any(b in tl for b in BLOCK):
        continue
    if any(m in tl for m in MED):
        continue
    if not any(k in tl for k in ANIMAL_KW):
        continue
    dup = is_dup(t)
    if dup:
        print(f"  [DUP: {dup}] {t}")
    else:
        print(f"  *** FRESH *** {t}")
        print(f"    url: {l}")
        print(f"    desc: {d[:200]}")
        print()
