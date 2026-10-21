#!/usr/bin/env python3
"""Triage raw RSS candidates TSV for the space lane.
Tag each candidate FRESH-KID-SAFE / DUP / MED-BLOCK / POL-BLOCK by
stable-token grep across content/blog/ and content/news/ + regex guardrails.
Reads TSV (title<TAB>link<TAB>description<TAB>feed) from argv[1].
"""
import csv, re, subprocess, sys

MED = re.compile(r"treat|therap|cure|drug|medic|diagnos|intervention|symptom|disease|"
                 r"disorder|depressi|alzheimer|cancer|diabet|brain.*health|neuro|"
                 r"stem cell|vision loss|impair|mental.*ill|psilocybin|psilocybin|magic mushroom", re.I)
POL = re.compile(r"political|government|war|conflict|leadership|govern|parliament|"
                 r"president|minister|council|climate.*polic|policy|election|court|lawsuit|"
                 r"terror|bomb|shooting|killed|death toll|attack", re.I)
VIOLENT = re.compile(r"\b(kill|murder|massacre|slaughter|fatal)\b", re.I)

SKIP_TOKS = {"the","with","have","this","from","their","scientists","science",
             "astronomers","researchers","for","and","that","have","will","are"}

def written(title, desc):
    tokens = [t for t in re.split(r"[^a-zA-Z0-9]+", title.lower())
              if t and len(t) >= 5 and t not in SKIP_TOKS]
    # add stable nouns from description
    tokens = tokens[:8]
    hits = []
    for tok in tokens:
        out = subprocess.run(["grep","-ril",tok,"content/"],capture_output=True,text=True)
        files = [f for f in out.stdout.strip().split("\n") if f and f.endswith(".md")]
        if files:
            hits.append((tok, files[:2]))
    return hits

rows = list(csv.DictReader(open(sys.argv[1]), delimiter="\t"))
print(f"total={len(rows)}")
for i, r in enumerate(rows, 1):
    t, d, l = r["title"], r["description"], r["link"]
    if MED.search(t) or MED.search(d):
        print(f"[{i}] MED-BLOCK: {t[:85]}"); continue
    if POL.search(t) or POL.search(d):
        print(f"[{i}] POL-BLOCK: {t[:85]}"); continue
    if VIOLENT.search(t) or VIOLENT.search(d):
        print(f"[{i}] VIOLENT: {t[:85]}"); continue
    hits = written(t, d)
    if hits:
        print(f"[{i}] DUP: {t[:85]}")
        for tok,files in hits: print(f"      '{tok}' -> {files}")
    else:
        print(f"[{i}] FRESH: {t[:85]}")
        print(f"      URL: {l}")
        print(f"      DESC: {re.sub(r'<[^>]+>','',d)[:170]}")
