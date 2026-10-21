#!/usr/bin/env python3
"""Re-examine ALL BBC Science items for fresh, kid-safe candidates."""
import xml.etree.ElementTree as ET
import re, os

root = ET.parse('/tmp/bbc-science-raw.xml').getroot()
items = list(root.iter('item'))

# Build a set of existing filenames for quick literal check
existing = set()
for d in ("content/blog", "content/news"):
    if not os.path.isdir(d): continue
    for f in os.listdir(d):
        if f.endswith(".md"):
            existing.add(f.replace(".md", "").lower())

print(f"Total BBC Science items: {len(items)}")
print()

for i, it in enumerate(items):
    t = (it.findtext('title') or '').strip()
    l = (it.findtext('link') or '').strip()
    if len(t) < 25: continue
    tl = t.lower()
    
    # Guardrails
    med = any(w in tl for w in ["cancer","alzheim","covid","therapy","treatment","disease","syndrome","depression","mental","drug","trial","diagnos","health","hospital","patient","illness","disorder","symptom","cure","medicine","brain damage"])
    pol = any(w in tl for w in ["politic","election","government","minister","parliament","congress","senate","trump","musk","merger","deal","budget","spending","war","conflict","invasion","military","law","court","ban","policy"])
    
    # Literal dup (title in existing slugs)
    slug_words = re.sub(r'[^a-z0-9]+', '-', tl).strip('-')
    # Check if any existing slug shares 3+ significant words
    significant = [w for w in tl.split() if len(w) >= 5]
    
    flags = []
    if med: flags.append("MED")
    if pol: flags.append("POL")
    
    # Check against existing titles (not just body text)
    is_dup = False
    for es in existing:
        es_words = es.split('-')
        overlap = set(significant) & set(es_words)
        if len(overlap) >= 2:
            is_dup = True
            flags.append(f"DUP({overlap})")
    
    status = "|".join(flags) if flags else "CHECK-ME"
    print(f"[{status}] {t[:80]}")
    print(f"   {l[:90]}")
