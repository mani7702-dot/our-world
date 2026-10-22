#!/usr/bin/env python3
"""Parse Smithsonian feeds for animal-relevant fresh stories."""
import xml.etree.ElementTree as ET, os, re

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
             'ape','chimp','gorilla','lemur','sloth','armadillo','hedgehog','porcupine','skunk']

BLOCK = ("war","attack","death toll","killed","murder","court","lawsuit","covid","pandemic",
         "election","politic","terror","bomb","shooting","military","conflict","invasion","terrorism")

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

for label, path in [("Smithsonian", "/tmp/smithsonian.xml"), ("Smithsonian-history", "/tmp/smithsonian_hist.xml")]:
    try:
        root = ET.parse(path).getroot()
    except:
        print(f"  SKIP {label}: parse error")
        continue
    items = []
    for it in root.iter("item"):
        t = (it.findtext("title") or "").strip()
        d = (it.findtext("description") or "").strip()[:300]
        l = (it.findtext("link") or "").strip()
        if len(t) < 25:
            continue
        items.append((t, l, d))
    print(f"\n=== {label}: {len(items)} items ===")
    for t, l, d in items:
        tl = t.lower()
        if any(b in tl for b in BLOCK):
            continue
        if not any(k in tl for k in ANIMAL_KW):
            continue
        dup = is_dup(t)
        status = f"DUP: {dup}" if dup else "FRESH!"
        print(f"[{status}] {t}")
        print(f"  url: {l}")
        print(f"  desc: {d[:200]}")
        print()
