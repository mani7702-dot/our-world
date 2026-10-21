#!/usr/bin/env python3
"""Scan parsed sdi.xml candidates, flag likely-written ones via grep."""
import json, re, subprocess, sys
from xml.etree import ElementTree as ET

tree = ET.parse("/tmp/sdi.xml")
root = tree.getroot()
raw = []
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    d = re.sub(r"<[^>]+>", "", it.findtext("description") or "").strip()
    l = (it.findtext("link") or "").strip()
    raw.append((t, d, l))

# Medical guardrail keywords (treatment/therapy/drug/diagnosis/condition)
MED = re.compile(r"treat|therap|cure|drug|medic|diagnos|intervention|symptom|disease|disorder|depressi|alzheimer|cancer|diabet|brain.*health|brain.*act|neuro|stem cell|vision loss|vision.*impair", re.I)
# Political/world-affairs keywords
POL = re.compile(r"political|government|war|conflict|leadership|govern|parliament|president|minister|council|climate.*polic|policy", re.I)
# Dup check: core tokens to grep across content/
def written(title, desc):
    # build a few core tokens from the title
    tokens = re.split(r"[^a-zA-Z0-9]+", title.lower())
    tokens = [t for t in tokens if len(t) >= 4 and t not in ("the","with","have","this","from","their","scientists","science","astronomers","researchers")]
    hits = []
    for tok in tokens[:6]:
        if len(tok) < 5: continue
        out = subprocess.run(["grep","-ril",tok,"content/"],capture_output=True,text=True)
        files = out.stdout.strip().split("\n") if out.stdout.strip() else []
        dup_files = [f for f in files if f.endswith(".md")]
        if dup_files:
            hits.append((tok, dup_files))
    return hits

for i,(t,d,l) in enumerate(raw,1):
    tag = ""
    if MED.search(t) or MED.search(d): tag="MED-BLOCK"
    elif POL.search(t) or POL.search(d): tag="POL-BLOCK"
    if tag:
        print(f"[{i}] {tag}: {t[:80]}")
        continue
    hits = written(t,d)
    if hits:
        print(f"[{i}] DUP: {t[:80]}")
        for tok,files in hits: print(f"      token '{tok}' -> {files[:2]}")
    else:
        print(f"[{i}] FRESH-KID-SAFE: {t[:80]}")
        print(f"      URL: {l}")
        print(f"      DESC: {d[:180]}")
