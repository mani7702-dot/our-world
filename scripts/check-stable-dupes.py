#!/usr/bin/env python3
"""Stable-token dupe checker across content/blog/ and content/news/.
Usage: python3 scripts/check-stable-dupes.py <slug> <token1> <token2> ...
Grep BOTH dirs, case-insensitive."""
import glob, sys, re
tokens = [t.lower() for t in sys.argv[2:]]
hits = []
for f in glob.glob("content/blog/*.md") + glob.glob("content/news/*.md"):
    txt = open(f, encoding="utf-8", errors="replace").read().lower()
    if any(re.search(r'\b' + re.escape(t) + r'\b', txt) for t in tokens):
        hits.append(f)
print("DUPES:" if hits else "NO DUPES")
for h in hits:
    print(" ", h)
