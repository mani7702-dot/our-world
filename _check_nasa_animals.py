#!/usr/bin/env python3
"""Download NASA main feed + check for animal-relevant stories."""
import subprocess, xml.etree.ElementTree as ET, os

UA = "Mozilla/5.0 (OurWorld raw-fallback; contact andugulamani722@gmail.com)"
FEED = "https://www.nasa.gov/feed/"
PATH = "/tmp/nasa_main.xml"

r = subprocess.run(["curl", "-s", "--compressed", "--max-time", "25", "-A", UA, FEED, "-o", PATH], capture_output=True)
size = os.path.getsize(PATH)
print(f"Downloaded NASA main: {size} bytes")

try:
    root = ET.parse(PATH).getroot()
except:
    print("PARSE ERROR")
    exit()

items = []
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    d = (it.findtext("description") or "").strip()[:300]
    l = (it.findtext("link") or "").strip()
    if len(t) < 25:
        continue
    items.append((t, l, d))

print(f"Total items: {len(items)}")
ANIMAL_KW = ['animal','bear','whale','shark','bird','turtle','dolphin','elephant','monkey','frog','fish',
             'bee','butterfly','snake','rabbit','deer','elk','crocodile','bat','owl','horse','cow','pig',
             'chicken','duck','squirrel','bison','wildlife','habitat','species','nest','migration','reef',
             'coral','mammal','predator','flock','swarm','seal','otter','penguin','cat','dog','pup','kitten']

for t, l, d in items:
    tl = t.lower()
    if any(k in tl for k in ANIMAL_KW):
        print(f"\nANIMAL: {t}")
        print(f"  url: {l}")
        print(f"  desc: {d[:200]}")
