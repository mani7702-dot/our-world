#!/usr/bin/env python3
# Tirith-safe batch dupe check for listicle/all candidates.
import os, re, sys
root = os.getcwd()
content_dirs = ["content/blog", "content/news"]
phrases = [
    "ultra-processed food cancer",
    "masaya volcano",
    "neuroscience freud",
    "coral back to life",
    "northern ireland climate",
    "jackdaw climate",
    "wildlife overpass",
    "movie antagonists sympathy",
    "lakes weirdness|10 rare lakes",
    "music careers sitcoms",
    "sunken villages|drowned towns",
    "wild facts bears",
    "medical mysteries poisoning",
    "intelligence operations hollywood",
]
allfiles = []
for d in content_dirs:
    if os.path.isdir(d):
        for f in os.listdir(d):
            if f.endswith(".md"):
                allfiles.append(os.path.join(d, f))

for p in phrases:
    rx = re.compile(p, re.I)
    hits = []
    for fp in allfiles:
        try:
            txt = open(fp, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        if rx.search(txt):
            hits.append(fp)
    print(f"{len(hits)}  {p}  ->  {hits[:3]}")
