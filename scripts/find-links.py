#!/usr/bin/env python3
"""Find external source links in an HTML file."""
import re, sys

with open(sys.argv[1], 'r', errors='replace') as f:
    html = f.read()

links = re.findall(r'href="(https?://[^"]+)"', html)
seen = set()
for l in links:
    if l in seen:
        continue
    seen.add(l)
    lower = l.lower()
    # Show BBC, SWNS, Guinness, press, etc.
    if any(kw in lower for kw in ['bbc', 'swns', 'guinness', 'rendcomb', 'wikipedia', 'aerosuper', 'press']):
        print(l)
