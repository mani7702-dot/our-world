#!/usr/bin/env python3
"""Download ScienceDaily top feed raw and parse ALL items, run full abort pass."""
import subprocess, xml.etree.ElementTree as ET, os, re

UA = "Mozilla/5.0 (OurWorld raw-fallback; contact andugulamani722@gmail.com)"
FEED = "https://www.sciencedaily.com/rss/top.xml"
PATH = "/tmp/sd_top.xml"

r = subprocess.run(["curl", "-s", "--compressed", "--max-time", "25", "-A", UA, FEED, "-o", PATH], capture_output=True)
print(f"Downloaded SD top: {os.path.getsize(PATH)} bytes")

try:
    root = ET.parse(PATH).getroot()
except ET.ParseError:
    print("PARSE ERROR")
    exit()

items = []
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    d = (it.findtext("description") or "").strip()[:350]
    l = (it.findtext("link") or "").strip()
    if len(t) < 25:
        continue
    items.append((t, l, d))

print(f"Total items: {len(items)}")

BLOCK = ("war","attack","death toll","killed","murder","court","lawsuit","covid","pandemic",
         "election","politic","terror","bomb","shooting","military","conflict","invasion","terrorism")
MED = ("cancer","disease","treatment","therapy","diagnos","mental disorder","depression","anxiety",
       "poisoning","medical mystery","patient","clinical")
ANIMAL_KW = ['animal','bear','whale','shark','bird','turtle','dolphin','elephant','monkey','frog',
             'fish','bee','butterfly','snake','rabbit','deer','elk','crocodile','alligator','panda',
             'tiger','lion','wolf','fox','owl','bat','horse','cow','pig','chicken','duck','squirrel',
             'prairie','bison','wildlife','habitat','conservation','species','endangered','pet','pup',
             'kitten','puppy','nest','migration','savanna','jungle','reef','coral','mammal','aquatic',
             'predator','herd','colony','flock','swarm','seal','otter','walrus','penguin','arctic',
             'forest','tree','plant','insect','microbe','bacteria','cell','genome','dna','genetic']

print("\n=== ALL NON-BLOCKED ITEMS ===")
for t, l, d in items:
    tl = t.lower()
    if any(b in tl for b in BLOCK):
        continue
    if any(m in tl for m in MED):
        continue
    # Check for animal keyword
    has_animal = any(k in tl for k in ANIMAL_KW)
    marker = "[ANIMAL]" if has_animal else "[other]"
    print(f"{marker} {t}")
    print(f"  url: {l}")
    print(f"  desc: {d[:200]}")
    print()
