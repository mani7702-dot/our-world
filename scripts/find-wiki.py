#!/usr/bin/env python3
"""Find Wikipedia article URL from search results for a given term."""
import re
html = open("/tmp/wiki-search.html", encoding="utf-8", errors="replace").read()
links = re.findall(r'href="/wiki/([^"]+)"', html)
for l in links:
    if "silverpit" in l.lower() or "crater" in l.lower():
        print("candidate:", l)
# Also search within the HTML for silverpit mentions
idxs = [m.start() for m in re.finditer(r"silverpit", html, re.I)]
print("silverpit mentions:", len(idxs))
for i in idxs[:3]:
    print(html[max(0,i-80):i+80])
