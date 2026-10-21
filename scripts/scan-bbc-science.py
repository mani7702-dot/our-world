#!/usr/bin/env python3
"""Show all BBC Science raw items with guardrail + dupe scan."""
import xml.etree.ElementTree as ET
import re, os
root = ET.parse('/tmp/bbc-science-raw.xml').getroot()
items = list(root.iter('item'))
print(f"total items: {len(items)}")
print()
medwords = ("cancer","alzheim","alzheimer","covid","pandemic","therapy","treatment","cure","disease","syndrome","depression","mental","brain damage","drug","trial","diagnos")
polwords = ("politic","election","government","parliament","treaty","agreement","policy","minister","congress","senate","trump","musk","merger","deal","tax","budget","spending","war","conflict","invasion","military","troop","siege")
for it in items:
    t = (it.findtext('title') or '').strip()
    if len(t) < 25: continue
    l = (it.findtext('link') or '').strip()
    tl = t.lower()
    flags = []
    if any(w in tl for w in medwords): flags.append("MED-BLOCK")
    if any(w in tl for w in polwords): flags.append("POL-BLOCK")
    # dupe check
    safe = re.sub(r'[^a-zA-Z0-9 ]',' ',tl)
    tokens = [w for w in safe.split() if len(w)>=5]
    dup = False
    for d in ("content/blog","content/news"):
        if not os.path.isdir(d): continue
        for f in os.listdir(d):
            if not f.endswith(".md"): continue
            txt = open(os.path.join(d,f),encoding="utf-8",errors="ignore").read().lower()[:800]
            tt = t.lower()
            if tt[:60] in txt:
                dup = True; break
        if dup: break
    if dup: flags.append("DUP")
    status = "|".join(flags) if flags else "FRESH"
    print(f"[{status}] {t}")
    print(f"   {l}")
