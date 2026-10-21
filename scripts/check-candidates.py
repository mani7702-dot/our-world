#!/usr/bin/env python3
"""Careful dupe-check for the top candidate stories using stable tokens."""
import re, glob

candidates = {
    "nasa-roman-telescope-exceeds-expectations": ["nasa", "roman telescope", "expectations", "30 percent"],
    "perseverance-mars-rover-driving-record": ["perseverance", "mars rover", "driving record", "off-world"],
    "nasa-jellyfish-launch": ["jellyfish", "spacex", "launch", "glowing"],
    "bennu-boulders-mystery": ["bennu", "boulders", "mystery", "heat"],
    "alaska-tsunami-tracy-arm": ["tsunami", "1580", "alaska", "tracy arm", "landslide"],
    "masaya-volcano-magma": ["masaya", "volcano", "magma", "nicaragua"],
    "space-x-crs35-jellyfish": ["jellyfish", "spacex", "crs35", "launch"],
}

files = glob.glob("/home/ubuntu/our-world/content/news/*.md") + glob.glob("/home/ubuntu/our-world/content/blog/*.md")

candidate_slugs = {
    "nasa-roman-telescope-exceeds-expectations": "nasa-roman-telescope-exceeds-expectations",
    "perseverance-mars-rover-driving-record": "perseverance-mars-rover-off-world-driving-record",
    "nasa-jellyfish-launch": "spacex-jellyfish-launch",
    "bennu-boulders-mystery": "bennu-boulders-heat-loss-mystery",
    "alaska-tsunami-tracy-arm": "alaska-landslide-tsunami-tracy-arm-1580-feet",
    "masaya-volcano-magma": "masaya-volcano-hidden-magma",
    "space-x-crs35-jellyfish": "spacex-crs35-jellyfish-launch",
}

for key, tokens in candidates.items():
    found = []
    for f in files:
        try:
            with open(f, encoding="utf-8") as fh:
                txt = fh.read().lower()
        except:
            continue
        hits = [t for t in tokens if t.lower() in txt]
        if len(hits) >= 2:
            found.append((f, hits))
    if found:
        print(f"[{key}] DUP - matches:")
        for f, hits in found:
            print(f"  {f} -> {hits}")
    else:
        print(f"[{key}] FRESH - no multi-token match")
