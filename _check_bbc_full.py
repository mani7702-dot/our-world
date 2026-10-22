#!/usr/bin/env python3
"""Show ALL BBC Science & Environment items (non-blocked) so we can manually inspect."""
import xml.etree.ElementTree as ET

root = ET.parse('/tmp/bbc_science.xml').getroot()
items = []
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    d = (it.findtext("description") or "").strip()[:300]
    l = (it.findtext("link") or "").strip()
    if len(t) < 25:
        continue
    items.append((t, l, d))

BLOCK = ("war","attack","death toll","killed","murder","court","lawsuit","covid","pandemic",
         "election","politic","terror","bomb","shooting","military","conflict","invasion","terrorism")

for t, l, d in items:
    tl = t.lower()
    if any(b in tl for b in BLOCK):
        continue
    print(f"TITLE: {t}")
    print(f"  url: {l}")
    print(f"  desc: {d[:220]}")
    print()
