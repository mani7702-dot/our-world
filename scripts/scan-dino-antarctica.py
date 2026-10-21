#!/usr/bin/env python3
"""Tirith-safe: check the Antarctica dinosaur candidate against existing content."""
import os, re
CONTENT_DIRS = ["/home/ubuntu/our-world/content/news", "/home/ubuntu/our-world/content/blog"]
terms = ["antarctica", "dinosaur", "chilesaurus", "hera", "james claeys", "university of brighton", "cage"]
for d in CONTENT_DIRS:
    if not os.path.isdir(d): continue
    for fn in os.listdir(d):
        p=os.path.join(d,fn)
        try: txt=open(p,encoding="utf-8",errors="ignore").read()
        except: continue
        for t in terms:
            if re.search(re.escape(t), txt, re.I):
                print(f"  DUP: term='{t}' -> {p}")
                break
print("scan done")
