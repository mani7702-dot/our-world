#!/usr/bin/env python3
"""Check raw candidates TSV against published ScienceDaily release IDs."""
import re, glob, sys

published = set()
for f in glob.glob('content/news/*.md') + glob.glob('content/blog/*.md'):
    txt = open(f).read()
    published.update(re.findall(r'2610(\d{8})', txt))

print(f"Published SD IDs: {sorted(published)}")
print()

candidates = []
for line in open('/tmp/raw-candidates.tsv'):
    parts = line.rstrip('\n').split('\t')
    if len(parts) < 2:
        continue
    title, link = parts[0], parts[1]
    m = re.search(r'2610(\d{8})\.htm', link)
    if m:
        candidates.append((m.group(1), title))
    else:
        candidates.append(('BBC', title))

print("=== FRESH (not in published) ===")
for sdid, title in candidates:
    if sdid != 'BBC' and sdid not in published:
        print(f"  {sdid}: {title}")

print()
print("=== DUP (already published) ===")
for sdid, title in candidates:
    if sdid != 'BBC' and sdid in published:
        print(f"  {sdid}: {title}")
