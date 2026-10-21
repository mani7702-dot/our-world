#!/usr/bin/env python3
"""Check Smithsonian history candidates for dupes + guardrails (Tirith-safe, file-based)."""
import os, re, sys

DIRS = ["content/blog", "content/news"]
allfiles = []
for d in DIRS:
    if os.path.isdir(d):
        for f in os.listdir(d):
            if f.endswith(".md"):
                allfiles.append(os.path.join(d, f))

# (slug, [tokens that MUST NOT all appear in any existing file to be fresh])
CANDIDATES = [
    ("sherlock-holmes-joseph-bell-real-surgeon", ["sherlock holmes", "conan doyle", "joseph bell"]),
    ("horror-movies-history-exhibition", ["slasher film", "horror movie", "sinners", "psycho", "shining"]),
    ("lafayette-brother-in-law-haiti", ["lafayette", "haiti", "revolution"]),
    ("elizabeth-i-secretary-letters", ["elizabeth i", "elizabeth's", "queen mary", "scot"]),
    ("lancaster-pennsylvania-one-day-capital", ["lancaster", "pennsylvania", "capital for one day", "philadelphia"]),
    ("georgia-tann-orphan-abductor", ["georgia tann", "orphan", "abducted", "sold children"]),
    ("new-york-times-175-years", ["new york times", "1851", "fit to print", "public importance"]),
    ("magic-protection-witch-bottles", ["witch bottle", "apotropaic", "magic protect", "mystical symbol"]),
    ("peasants-revolt-1381-uprising", ["peasants' revolt", "1381", "uprising", "lancaster"]),
    ("how-america-got-its-name", ["united states of america", "united colonies", "alleghania", "united states of the earth", "1776"]),
    ("turtle-submarine-bushnell", ["turtle submarine", "david bushnell", "bomb-carrying", "royal navy"]),
    ("wwi-automobile-commandos", ["world war i", "wwi", "automobile", "mechanization", "royal automobile"]),
    ("wwii-american-commando-francis-coolidge", ["francis lowell coolidge", "jefferson", "office of strategic", "world war ii", "wwii"]),
    ("cave-paintings-moving-light", ["cave painting", "prehistoric", "lascaux", "altamira", "torchlight"]),
    ("thurgood-marshall-civil-rights-strategy", ["thurgood marshall", "supreme court", "jim crow", "separate but equal"]),
    ("queen-caroline-arthur-pr-merlin", ["king arthur", "caroline of brandenburg", "merlin's cave", "hanover", "pr strateg"]),
]

MED = ("treatment", "therapy", "diagnos", "mental disorder", "cure for", "patients with", "condition")
POL = ("politic", "election", "court decision", "lawsuit", "terror", "bomb", "shooting", "war crime")
# VIOLENT/scar terms that make a story unsuitable for kids
SCARY = ("behead", "beheading", "murder", "killed", "massacre", "slaue", "tortur", "brutally", "horror", "slasher", "vampire", "sinners", "psycho", "shining")

files_read = {}
for fp in allfiles:
    try:
        files_read[fp] = open(fp, encoding="utf-8", errors="ignore").read().lower()
    except Exception:
        files_read[fp] = ""

print(f"Total existing articles: {len(allfiles)}")
print("=" * 70)

for slug, tokens in CANDIDATES:
    dup_hits = []
    for fp, txt in files_read.items():
        for tok in tokens:
            if tok.lower() in txt:
                dup_hits.append(f"{fp} (token:'{tok}')")
                break
    if dup_hits:
        print(f"DUP: {slug} -> {dup_hits[:2]}")
    else:
        slug_lower = slug.lower()
        blocked = []
        for b in SCARY:
            if b in slug_lower:
                blocked.append(f"SCARY:{b}")
        for b in MED:
            if b in slug_lower:
                blocked.append(f"MED:{b}")
        for b in POL:
            if b in slug_lower:
                blocked.append(f"POL:{b}")
        status = "BLOCKED:" + ",".join(blocked) if blocked else "FRESH-KID-SAFE"
        print(f"{status}: {slug}")
