#!/usr/bin/env python3
"""List ALL BBC World items from raw feed."""
import xml.etree.ElementTree as ET, os, re

existing = {}
for d in ["content/blog", "content/news"]:
    if os.path.isdir(d):
        for f in os.listdir(d):
            if f.endswith(".md"):
                existing[f] = open(os.path.join(d, f), encoding="utf-8", errors="ignore").read().lower()

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

root = ET.parse('/tmp/bbc_world.xml').getroot()
items = []
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    l = (it.findtext("link") or "").strip()
    d = (it.findtext("description") or "").strip()[:300]
    if len(t) < 25:
        continue
    items.append((t, l, d))

print(f"Total BBC World items: {len(items)}\n")
for t, l, d in items:
    dup = is_dup(t)
    status = f"DUP: {dup}" if dup else "FRESH"
    # Check for any animal keywords in title
    animal = any(k in t.lower() for k in ['animal','bear','whale','shark','bird','turtle','dolphin','elephant','monkey','frog','fish','bee','butterfly','snake','rabbit','deer','elk','crocodile','bat','owl','horse','cow','pig','chicken','duck','squirrel','bison','wildlife','habitat','conservation','species','nest','migration','reef','coral','mammal','predator','flock','seal','otter','penguin','cat','dog','pup','kitten'])
    marker = "[ANIMAL]" if animal else ""
    print(f"[{status}] {marker} {t}")
    print(f"  url: {l}")
    print(f"  desc: {d[:200]}")
    print()
