#!/usr/bin/env python3
"""File-based abort-pass checker — Tirith-safe."""
import re, os, glob

candidates = [
    ("10 Movie Antagonists Who Deserved More Sympathy", "listicle"),
    ("10 Lakes Where Nature Gets Seriously Weird", "listicle"),
    ("10 of the Biggest Music Careers Launched by Sitcoms", "listicle"),
    ("10 Period-Drama Details That Look Fake but Are Historically Accurate", "listicle"),
    ("10 Sunken Villages That Mysteriously Reappear", "listicle"),
    ("10 Wild Facts You Might Not Know About Bears", "listicle"),
    ("10 Terrifying Medical Mysteries That Turned Out to Be Poisoning", "listicle"),
    ("Nigeria confirms Ebola case linked to East Africa", "world"),
    ("Borneo toxic haze life frontline South East Asia", "world"),
    ("North America Largest Wildlife Overpass I 25 Collisions Down 91", "animals"),
    ("massive study 460000 people challenges ultra-processed food cancer fears", "science"),
    ("something strange happening beneath a volcano near 2 million people", "science"),
    ("modern neuroscience rediscovering surprising idea freud 130 years ago", "science"),
    ("simple touch brings dying corals back to life in just 7 weeks", "science"),
    ("Northern Ireland courage leadership tackle climate change", "world"),
    ("Jackdaw ignites row over climate and costs", "world"),
]

med_terms = re.compile(r'\b(treat|therapy|diagnos|mental disorder|patient|cure|remedy|disease|syndrome|vaccine|medic)\w*', re.I)
pol_terms = re.compile(r'\b(trump|musk|merger|political|opposition|government|election|war|conflict|riot|protest|court|trial|crime|attack|violence|terror|murder)\w*', re.I)

files = glob.glob("content/news/*.md") + glob.glob("content/blog/*.md")

for title, lane in candidates:
    # slug candidate
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:60]
    dupes = []
    for f in files:
        try:
            with open(f, encoding="utf-8") as fh:
                txt = fh.read()
        except Exception:
            continue
        short = title.split()[0:4]
        needle = " ".join(short)
        if re.search(re.escape(needle), txt, re.I):
            dupes.append(f)
        if os.path.basename(f).replace('.md','') == slug:
            dupes.append(f)
    dupes = sorted(set(dupes))
    med = bool(med_terms.search(title))
    pol = bool(pol_terms.search(title))
    status = []
    if dupes:
        status.append(f"DUP({len(dupes)})")
    if med:
        status.append("MED-BLOCK")
    if pol:
        status.append("POL-BLOCK")
    verdict = " | ".join(status) if status else "FRESH"
    print(f"[{lane:10}] {verdict:20} | {title}")
    for d in dupes[:2]:
        print(f"            dupe: {d}")
