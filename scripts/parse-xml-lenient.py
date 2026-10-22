#!/usr/bin/env python3
"""Lenient RSS parser - strips bad XML entities and prints all items."""
import sys, re
from xml.etree import ElementTree as ET

path = sys.argv[1]
raw = open(path, encoding="utf-8", errors="ignore").read()
# strip problematic control chars and & not followed by entity
raw = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', '', raw)
raw = re.sub(r'&(?![a-zA-Z#0-9]+;)', '&amp;', raw)
try:
    root = ET.fromstring(raw)
except ET.ParseError as e:
    print(f"PARSE ERROR even after cleanup: {e}", file=sys.stderr)
    sys.exit(1)
n = 0
for it in root.iter('item'):
    t = (it.findtext('title') or '').strip()
    l = (it.findtext('link') or '').strip()
    if len(t) > 20:
        n += 1
        print(f"{n}. {t[:90]}")
        print(f"   {l[:110]}")
        if n >= 20:
            break
