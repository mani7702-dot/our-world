#!/usr/bin/env python3
"""Check ALL GNN items for animal relevance + dup status (stable token check across both dirs)."""
import xml.etree.ElementTree as ET, os, re

root = ET.parse('/tmp/gnn.xml').getroot()
items = []
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    d = (it.findtext("description") or "").strip()[:300]
    l = (it.findtext("link") or "").strip()
    if len(t) < 25:
        continue
    items.append((t, l, d))

ANIMAL_KW = ['animal','bear','whale','shark','bird','turtle','dolphin','elephant','monkey','frog',
             'fish','bee','butterfly','snake','rabbit','deer','elk','crocodile','alligator','panda',
             'tiger','lion','wolf','fox','owl','bat','horse','cow','pig','chicken','duck','squirrel',
             'prairie','bison','wildlife','habitat','conservation','species','endangered','pet','pup',
             'kitten','puppy','nest','migration','savanna','jungle','reef','coral','mammal','aquatic',
             'predator','herd','colony','flock','swarm','seal','otter','walrus','penguin','arctic',
             'forest','cat','dog','puppy','kitten']

# Read all existing content into memory for quick search
existing_texts = {}
for d in ["content/blog", "content/news"]:
    if os.path.isdir(d):
        for f in os.listdir(d):
            if f.endswith(".md"):
                fp = os.path.join(d, f)
                existing_texts[f] = open(fp, encoding="utf-8", errors="ignore").read().lower()

def is_dup(title):
    tl = title.lower()
    safe = re.sub(r'[^a-zA-Z0-9 ]', ' ', tl)
    words = [w for w in safe.split() if len(w) >= 5]
    for fname, txt in existing_texts.items():
        if tl in txt[:500]:
            return fname + " [TITLE]"
        mc = sum(1 for w in words if w in txt)
        if mc >= 3:
            return fname + f" [tokens={mc}]"
    return None

print(f"Total GNN items: {len(items)}\n")
print("=== ALL ANIMAL-RELEVANT STORIES (with dup check) ===")
for t, l, d in items:
    tl = t.lower()
    if not any(k in tl for k in ANIMAL_KW):
        continue
    dup = is_dup(t)
    status = f"DUP: {dup}" if dup else "FRESH!"
    print(f"[{status}] {t}")
    print(f"  url: {l}")
    print(f"  desc: {d[:180]}")
    print()
