#!/usr/bin/env python3
"""List ALL GNN items from the raw feed without filtering."""
import xml.etree.ElementTree as ET

root = ET.parse('/tmp/gnn.xml').getroot()
items = []
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    l = (it.findtext("link") or "").strip()
    if len(t) < 25:
        continue
    items.append((t, l))

print(f"Total: {len(items)} items\n")
for i, (t, l) in enumerate(items):
    print(f"{i+1}. {t}")
    print(f"   {l}")
    print()
