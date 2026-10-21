#!/usr/bin/env python3
"""Extract existing ScienceDaily release IDs from already-written content."""
import re, os

ids = set()
print("DEBUG cwd =", os.getcwd())
for d in ["content/blog", "content/news"]:
    print("DEBUG isdir", d, "=", os.path.isdir(d))
    if os.path.isdir(d):
        for f in os.listdir(d):
            if f.endswith(".md"):
                t = open(os.path.join(d, f), encoding="utf-8", errors="ignore").read()
                ids.update(re.findall(r"releases/(\d{14})\.htm", t))

print("EXISTING SD IDs count =", len(ids))
for i in sorted(ids):
    print(i)

# Now scan candidates file for IDs and mark which are dupes
cand_ids = []
for line in open("/tmp/sc-candidates.tsv"):
    m = re.search(r"releases/(\d{14})\.htm", line)
    if m:
        cand_ids.append((m.group(1), line.split("\t")[0].strip()))

print("\nCandidate IDs and dupe status:")
for cid, title in cand_ids:
    status = "DUP" if cid in ids else "FRESH"
    print(f"  [{status}] {cid}  {title}")
