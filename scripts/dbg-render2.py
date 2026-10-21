#!/usr/bin/env python3
import sys
sys.path.insert(0, "/home/ubuntu/our-world")
import build
text = open("/home/ubuntu/our-world/content/news/history-solar-storm-train-delay-typo.md").read()
p, body = build.parse_frontmatter(text)
v = p.get("for-grown-ups")
print("type:", type(v))
print("repr(v)[:200]:", repr(v)[:200])
print("bool(v):", bool(v))
print("len(v):", len(v) if v is not None else "N/A")
print("all keys:", sorted(p.keys()))
# Check the EXACT bytes of the for-grown-ups line in the source file
lines = text.split("\n")
for ln in lines:
    if ln.startswith("for-grown-ups"):
        print("RAW LINE repr first 120:", repr(ln[:120]))
        break
