#!/usr/bin/env python3
"""Download BBC Science & Environment raw feed and parse for animal-relevant stories."""
import subprocess, xml.etree.ElementTree as ET, os, re

UA = "Mozilla/5.0 (OurWorld raw-fallback; contact andugulamani722@gmail.com)"
FEED = "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml"

r = subprocess.run(["curl", "-s", "--compressed", "--max-time", "25", "-A", UA, FEED, "-o", "/tmp/bbc_science.xml"], capture_output=True)
print(f"Downloaded: {os.path.getsize('/tmp/bbc_science.xml')} bytes")

root = ET.parse('/tmp/bbc_science.xml').getroot()
items = []
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    d = (it.findtext("description") or "").strip()[:300]
    l = (it.findtext("link") or "").strip()
    if len(t) < 25:
        continue
    items.append((t, l, d))

# Filter for animal-relevant + non-blocked
animal_kw = ['dog','cat','bird','bear','whale','shark','turtle','dolphin','elephant','monkey',
             'frog','fish','bee','butterfly','snake','rabbit','deer','elk','crocodile','alligator',
             'panda','tiger','lion','wolf','fox','owl','bat','horse','cow','pig','chicken','duck',
             'squirrel','prairie','bison','wildlife','habitat','conservation','species','endangered',
             'pet','pup','kitten','puppy','nest','migration','savanna','jungle','reef','coral',
             'mammal','aquatic','predator','prey','herd','colony','flock','swarm','whale','dolphin',
             'seal','otter','walrus','penguin','polar','arctic']

BLOCK = ("war","attack","death toll","killed","murder","court","lawsuit","covid","pandemic",
         "election","politic","terror","bomb","shooting","military","conflict","invasion","terrorism")

print(f"Total items: {len(items)}")
print("\n=== ANIMAL-RELEVANT CANDIDATES ===")
for t, l, d in items:
    tl = t.lower()
    if any(b in tl for b in BLOCK):
        continue
    if any(k in tl for k in animal_kw):
        # Check dup
        print(f"TITLE: {t}")
        print(f"  url: {l}")
        print(f"  desc: {d[:200]}")
        print()
