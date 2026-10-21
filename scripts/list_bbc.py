#!/usr/bin/env python3
"""List all BBC Science items."""
import xml.etree.ElementTree as ET

tree = ET.parse("/tmp/bbc_science.xml")
root = tree.getroot()
items = root.findall(".//item")
print(f"Total items: {len(items)}")
print()
for it in items:
    title = it.findtext("title","").strip()
    link = it.findtext("link","").strip()
    desc = it.findtext("description","").strip()[:300]
    print(f"TITLE: {title}")
    print(f"URL: {link}")
    print(f"DESC: {desc}")
    print("---")
