#!/usr/bin/env python3
import sys, xml.etree.ElementTree as ET

feeds = {
    "bbc-world": "/tmp/bbc-world.xml",
}

for fname in sys.argv[1:]:
    tree = ET.parse(fname)
    root = tree.getroot()
    for it in root.iter("item"):
        t = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        for kw in sys.argv[2:]:
            if kw.lower() in t.lower():
                print(f"TITLE: {t}")
                print(f"  URL: {link}")
                print()
