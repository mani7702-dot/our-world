#!/usr/bin/env python3
import re, sys
from xml.etree import ElementTree as ET

tree = ET.parse(sys.argv[1])
root = tree.getroot()
ns = {"m": "http://search.yahoo.com/mrss/"}

items = []
for it in root.iter("item"):
    title = (it.findtext("title") or "").strip()
    desc_raw = it.findtext("description") or ""
    # strip HTML tags from description
    desc = re.sub(r"<[^>]+>", "", desc_raw).strip()
    link = (it.findtext("link") or "").strip()
    items.append((title, desc, link))

for i, (t, d, l) in enumerate(items, 1):
    print(f"[{i}] {t}")
    print(f"    URL: {l}")
    print(f"    DESC: {d[:280]}")
    print()