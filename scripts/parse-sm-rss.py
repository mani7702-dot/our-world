#!/usr/bin/env python3
"""Brute-force extract <title> and <guid>/<link> pairs from Smithsonian science RSS,
tolerating malformed XML by scanning line-by-line for <item> blocks."""
import re, os
path = "/tmp/smithsonian_science.xml"
raw = open(path, encoding="utf-8", errors="ignore").read()

# Extract item blocks via regex (tolerate bad entities)
items = re.findall(r'<item[^>]*>(.*?)</item>', raw, re.S)
print(f"Found {len(items)} <item> blocks (brute-force)")
for i, block in enumerate(items[:18]):
    t = re.search(r'<title[^>]*>(.*?)</title>', block, re.S)
    l = re.search(r'<link>(.*?)</link>', block, re.S)
    g = re.search(r'<guid[^>]*>(.*?)</guid>', block, re.S)
    title = re.sub(r'<[^>]+>','', t.group(1)).strip() if t else "NO TITLE"
    link = (g or l)
    link = link.group(1).strip() if link else ""
    print(f"{i+1}. {title[:90]}")
    print(f"   {link[:110]}")
