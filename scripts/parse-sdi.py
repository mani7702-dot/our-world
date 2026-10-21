#!/usr/bin/env python3
"""Parse a saved ScienceDaily XML feed file and list titles + links."""
import sys, xml.etree.ElementTree as ET
path = sys.argv[1] if len(sys.argv) > 1 else "/tmp/sdi.xml"
root = ET.fromstring(open(path, encoding="utf-8").read())
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    l = (it.findtext("link") or "").strip()
    print(t, "|", l)
