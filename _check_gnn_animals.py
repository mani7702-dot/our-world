#!/usr/bin/env python3
"""Filter GNN raw feed for animal-specific stories with a broader keyword set."""
import xml.etree.ElementTree as ET

root = ET.parse('/tmp/gnn.xml').getroot()
items = []
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    d = (it.findtext("description") or "").strip()[:300]
    l = (it.findtext("link") or "").strip()
    if len(t) < 25:
        continue
    items.append((t, l, d))

animal_kw = ['dog','cat','bird','bear','whale','shark','turtle','dolphin','elephant','monkey',
             'frog','fish','bee','butterfly','snake','rabbit','deer','elk','crocodile','alligator',
             'panda','tiger','lion','wolf','fox','owl','bat','horse','cow','pig','chicken','duck',
             'squirrel','prairie','bison','overpass','wildlife','habitat','conservation','species',
             'endangered','pet','pup','kitten','puppy','nest','migration','savanna','jungle','reef',
             'coral','mammal','aquatic','predator','prey','herd','colony','flock','swarm']

for t, l, d in items:
    tl = t.lower()
    if any(k in tl for k in animal_kw):
        print(f"ANIMAL: {t}")
        print(f"  url: {l}")
        print(f"  desc: {d[:180]}")
        print()
