#!/usr/bin/env python3
import sys, os
sys.path.insert(0, "/home/ubuntu/our-world")
import build

news = build.load_posts("news")
p = next(x for x in news if x["slug"]=="history-solar-storm-train-delay-typo")

# Reproduce the EXACT article_page body up to the tokens dict, with prints
section = p["section"]
prefix = "../"
meta_extra = ""
tag_list = ""
if p["tag_list"]:
    tag_list = "<ul>"+"".join('<li>%s</li>'%build.esc(t) for t in p["tag_list"])+"</ul>"

print("STEP1: p has for-grown-ups:", "for-grown-ups" in p, "value len:", len(p.get("for-grown-ups","")))
grownups = ""
fg = p.get("for-grown-ups")
print("STEP2: fg truthy?", bool(fg), "repr first 60:", repr(fg)[:60] if fg else "EMPTY")
print("STEP3: fg is None?", fg is None)
print("STEP4: type fg:", type(fg))
print("STEP5: checking 'for-grown-ups' in p.keys():", "for-grown-ups" in list(p.keys()))
# Check if it's a weird unicode/hyphen issue
for k in p.keys():
    if "grown" in k.lower():
        print(f"  key={k!r} len={len(p[k])}")
