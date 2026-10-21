#!/usr/bin/env python3
"""Triage raw RSS candidates with positional field handling (3-col TSV)."""
import csv, re, subprocess, sys

MED = re.compile(r"treat|therap|cure|drug|medic|diagnos|intervention|symptom|disease|\n"
                 r"disorder|depressi|alzheimer|cancer|diabet|brain.*health|neuro|\n"
                 r"stem cell|vision loss|impair|mental.*ill|psilocybin|magic mushroom|\n"
                 r"obesity|weight.?loss|appetite|statin|cholesterol", re.I)
POL = re.compile(r"political|government|war|conflict|leadership|govern|\n"
                 r"president|minister|council|climate.*polic|policy|election|court|lawsuit|\n"
                 r"terror|bomb|shooting|killed|death toll|attack|merger|anthropic|\n"
                 r"musk|tesla|starlink|ukraine|senate|parliament|brexit|trump", re.I)
VIOLENT = re.compile(r"\b(kill|murder|massacre|slaughter|fatal|violence)\b", re.I)

rows = list(csv.reader(open(sys.argv[1]), delimiter="\t"))
print(f"total={len(rows)}\n")
for i, row in enumerate(rows, 1):
    if len(row) < 3:
        continue
    t, l, d = row[0], row[1], row[2]
    desc_clean = re.sub(r"<[^>]+>", "", d)
    
    if MED.search(t) or MED.search(desc_clean):
        print(f"[{i}] MED-BLOCK: {t[:90]} | {l[:80]}")
        continue
    if POL.search(t) or POL.search(desc_clean):
        print(f"[{i}] POL-BLOCK: {t[:90]} | {l[:80]}")
        continue
    if VIOLENT.search(t) or VIOLENT.search(desc_clean):
        print(f"[{i}] VIOLENT: {t[:90]} | {l[:80]}")
        continue
    
    # stable token dupe check: use distinctive nouns from title
    title_lower = t.lower()
    skip = {"the","with","have","this","from","their","scientists","science",
            "astronomers","researchers","for","and","that","have","will","are",
            "some","more","most","what","why","how","can","could","new","find"}
    tokens = [w for w in re.split(r"[^a-zA-Z0-9]+", title_lower)
              if w and len(w) >= 5 and w not in skip]
    tokens = tokens[:6]
    
    hits = []
    for tok in tokens:
        out = subprocess.run(["grep", "-ril", tok, "content/"], capture_output=True, text=True)
        files = [f for f in out.stdout.strip().split("\n") if f and f.endswith(".md")]
        if files:
            hits.append((tok, files[:2]))
    
    if hits:
        print(f"[{i}] DUP: {t[:90]}")
        for tok, files in hits:
            print(f"      '{tok}' -> {files}")
    else:
        print(f"[{i}] FRESH: {t[:90]}")
        print(f"      URL: {l[:120]}")
        print(f"      DESC: {desc_clean[:150]}")
