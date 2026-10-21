#!/usr/bin/env python3
"""Final check: NASA main feed items against existing content + guardrails."""
import xml.etree.ElementTree as ET
import re, os

root = ET.parse('/tmp/nasa-main-feed.xml').getroot()
items = list(root.iter('item'))

existing = set()
for d in ("content/blog", "content/news"):
    if not os.path.isdir(d): continue
    for f in os.listdir(d):
        if f.endswith(".md"):
            existing.add(f.replace(".md", "").lower())

med = ["cancer","alzheim","covid","therapy","treatment","disease","syndrome","depression","mental","drug","trial","diagnos","health","hospital","patient","illness","disorder","symptom","cure","medicine"]
pol = ["politic","election","government","minister","parliament","congress","senate","trump","musk","merger","deal","budget","spending","war","conflict","invasion","military","law","court","ban","policy"]

for it in items:
    t = (it.findtext('title') or '').strip()
    l = (it.findtext('link') or '').strip()
    if len(t) < 25: continue
    tl = t.lower()
    med_block = any(w in tl for w in med)
    pol_block = any(w in tl for w in pol)
    # literal dup on slug words
    sig = [w for w in re.sub(r'[^a-z]+',' ',tl).split() if len(w)>=4]
    dup_hits = []
    for es in existing:
        es_words = es.split('-')
        overlap = set(sig) & set(es_words)
        if len(overlap) >= 2:
            dup_hits.append(f"{es} ({overlap})")
    
    flags = []
    if med_block: flags.append("MED")
    if pol_block: flags.append("POL")
    if dup_hits: flags.append("DUP")
    
    status = "|".join(flags) if flags else "FRESH"
    print(f"[{status}] {t[:85]}")
    print(f"   {l[:90]}")
    if dup_hits:
        for h in dup_hits[:2]:
            print(f"   -> {h}")
    print()
