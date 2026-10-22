#!/usr/bin/env python3
"""Parse an RSS XML file and print title+link for each item."""
import xml.etree.ElementTree as ET, sys, os
path = sys.argv[1]
root = ET.parse(path).getroot()
n = 0
for it in root.iter('item'):
    t = (it.findtext('title') or '').strip()
    l = (it.findtext('link') or '').strip()
    if len(t) > 20:
        n += 1
        print(f"{n}. {t}")
        print(f"   {l[:110]}")
        if n >= 15:
            break
