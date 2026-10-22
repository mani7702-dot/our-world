#!/usr/bin/env python3
import re, os, glob

sd_url_re = re.compile(r'sciencedaily\.com/releases/\d{4}/\d{2}/(\d{12})\.htm')
existing = {}
for fp in glob.glob("content/blog/*.md") + glob.glob("content/news/*.md"):
    txt = open(fp, encoding="utf-8", errors="ignore").read()
    for m in sd_url_re.finditer(txt):
        existing.setdefault(m.group(1), []).append(os.path.basename(fp))

# The 8 candidates from raw RSS that were marked FRESH by token checker
candidates = [
    ("261019093353", "kill dangerous gut bacteria (C diff) - MED-BLOCK"),
    ("261018205047", "Alaska monster tsunami 1580 feet"),
    ("261017230035", "third form of magnetism (altermagnetism)"),
    ("261017230028", "blueberries mood"),
    ("261017230025", "corals back to life touch"),
    ("261017230018", "ghostly green star"),
    ("261016081103", "39 sweeteners gut"),
    ("261016080912", "drug reverses fatty liver - MED-BLOCK"),
    # Also recheck the ones my checker falsely cleared
    ("261019093445", "ghostly eyeless cave snail"),
    ("261019093443", "hurricane warning maps"),
    ("261018205101", "Bennu boulders asteroid"),
    ("261019093434", "Jurassic squid belemnite"),
    ("261019093439", "10 diets slower aging"),
    ("261019093437", "vitamin C cancer survival - MED"),
    ("261019093355", "Alzheimer brain damage - MED"),
    ("261019093357", "aging brain memory"),
    ("261019093442", "Universe first five minutes helium"),
    ("261018205053", "quantum limit on a surface"),
    ("261018205050", "16 galaxies hiding cosmic chaos"),
    ("261017230020", "male female skin different rules"),
    ("261017230032", "soy salt brain compound"),
    ("261017230036", "magic mushroom aggressive fish"),
    ("261018084644", "fractional fermi sea"),
    ("261019093447", "statins muscle pain - MED"),
    ("261019093432", "??"),
    ("261020084818", "Perseverance Mars rover driving record"),
    ("261020085014", "ultra-processed food cancer - MED"),
    ("261020085013", "reverse 60 years aging cells"),
    ("261020085016", "astronauts hearts Mars"),
    ("261020085021", "train delayed solar storm"),
    ("261020085023", "too much RNA starve cells"),
    ("261020085025", "4 minutes strength after 65"),
    ("261020085727", "asteroid North Sea tsunami"),
    ("261018205037", "Nobel brain cells light"),
    ("261018205039", "Masaya volcano Nicaragua"),
    ("261018205044", "escape Alzheimer high-risk gene - MED"),
    ("261019093443", "hurricane maps"),
    ("261018084421", "Alzheimer sleep plaques - MED"),
    ("261018205033", "taste food after COVID - MED"),
]

print("=== DEFINITIVE DEDUP: candidate SD IDs vs content-cited SD IDs ===")
for cid, desc in candidates:
    if cid in existing:
        print(f"  DUP: SD {cid} ({desc[:45]}) -> already in {existing[cid][0][:55]}")
    else:
        print(f"  *** FRESH: SD {cid} ({desc[:45]}) *** - NOT cited in ANY content file")
