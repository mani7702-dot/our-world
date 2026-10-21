#!/usr/bin/env python3
"""Tirith-safe scan of remaining raw-candidate titles for fresh non-dupes."""
import os, re, subprocess, xml.etree.ElementTree as ET
from html.parser import HTMLParser

CONTENT_DIRS = ["/home/ubuntu/our-world/content/news", "/home/ubuntu/our-world/content/blog"]

def grep_any(term):
    for d in CONTENT_DIRS:
        if not os.path.isdir(d): continue
        for fn in os.listdir(d):
            p = os.path.join(d, fn)
            try:
                txt = open(p, encoding="utf-8", errors="ignore").read()
            except: continue
            if re.search(term, txt, re.I):
                return p
    return None

# Parse the raw BBC world+GNR.tsv we saved
rows = []
for line in open("/tmp/world-raw.tsv", encoding="utf-8"):
    parts = line.rstrip("\n").split("\t")
    if len(parts) >= 1:
        rows.append(parts[0])

# Already confirmed dupes / blocks / already-written today:
skip = {
    "borneo", "ebola", "windermere", "fin whale", "shipwreck", "orionid",
    "elon musk", "trump", "mars", "albert", "iron", "svitolina", "haitian",
    "trash island", "stephen hubbard", "australian mp", "katy adler",
    "north korea", "us airman", "kenya cult", "cornell", "albanian",
    "ukraine", "obama", "npr", "bbc inside", "hurricane"
}

for t in rows:
    tl = t.lower()
    if any(s in tl for s in skip): continue
    # noun extraction: big-capped words that arent Good News Network
    nouns = [w for w in re.findall(r'[A-Z][A-Za-z]+', t) if w.lower() not in {"good","news","network","with","and","the","a","of","to","in","on","for","from","after","via","is","by","at","vs","uk","us","dna","ai"}]
    # try the first distinctive noun as dupe probe
    found = None
    for n in nouns[:3]:
        if len(n) < 4: continue
        found = grep_any(re.escape(n))
        if found: break
    status = "DUP:" + (found.split("/")[-1] if found else "?") if found else "FRESH"
    print(f"  [{status}] {t}  ::nouns={nouns[:3]}")
