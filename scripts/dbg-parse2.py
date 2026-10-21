#!/usr/bin/env python3
import sys
sys.path.insert(0, "/home/ubuntu/our-world")
import build
text = open("/home/ubuntu/our-world/content/news/history-solar-storm-train-delay-typo.md").read()
p, body = build.parse_frontmatter(text)
print("keys:", sorted(p.keys()))
print("has for-grown-ups?:", "for-grown-ups" in p)
print("for-grown-ups value (first 80):", repr(p.get("for-grown-ups", "<MISSING>")[:80]))
print("for-grown-ups value len:", len(p.get("for-grown-ups", "")))
