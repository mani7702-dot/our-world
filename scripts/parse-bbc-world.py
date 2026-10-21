#!/usr/bin/env python3
"""Tirith-safe file-based BBC World RSS parser."""
import sys, os
import xml.etree.ElementTree as ET

feed_file = sys.argv[1] if len(sys.argv) > 1 else "/tmp/bbc-world.xml"

root = ET.parse(feed_file)
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    l = (it.findtext("link") or "").strip()
    d = (it.findtext("description") or "").strip()[:300]
    if t and len(t) > 15:
        print(t)
        print("  URL:", l)
        if d:
            print("  DESC:", d)
        print()
