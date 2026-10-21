#!/usr/bin/env python3
"""Extract text snippets from a saved Bing search results page."""
import sys, re, html as htmllib
filepath = sys.argv[1] if len(sys.argv) > 1 else "/tmp/bing1.html"
raw = open(filepath, encoding="utf-8", errors="replace").read()
# Bing result snippets
results = re.findall(r'<p[^>]*>(.*?)</p>', raw, re.S|re.I)
count = 0
for r in results:
    txt = re.sub(r'<[^>]+>', ' ', r)
    txt = htmllib.unescape(txt)
    txt = re.sub(r'\s+', ' ', txt).strip()
    if len(txt) > 40 and count < 15:
        print(txt[:300])
        print("---")
        count += 1
# Also look for specific keywords
print("\n=== KEYWORD SEARCH ===")
for kw in ['wasp-17b', 'transmission', 'lopsided', 'nature astronomy', 'james webb', 'cornell']:
    c = raw.lower().count(kw.lower())
    print(f"  {kw}: {c}")
