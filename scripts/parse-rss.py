#!/usr/bin/env python3
"""Tirith-safe file-based RSS parser. Usage: python3 scripts/parse-rss.py <feed.xml>"""
import sys, xml.etree.ElementTree as ET
path = sys.argv[1]
root = ET.parse(path).getroot()
items = root.iter("item") if root.tag == "rss" or root.tag.endswith("rss") else root.iter("item")
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    l = (it.findtext("link") or "").strip()
    d = (it.findtext("description") or "").strip()[:250]
    if t:
        print(f"TITLE: {t}")
        print(f"  LINK: {l}")
        if d:
            print(f"  DESC: {d}")
        print()
