#!/usr/bin/env python3
"""Verify specific FRESH candidates against existing posts with stable-token grep (cross-check the blind spot)."""
import os
ROOT="/home/ubuntu/our-world"
checks={
 "alaska_tsunami": ("alaska","tsunami","1580","tracy arm"),
 "spaceX_iss_cargo": ("spaceship","spaceX","carg","iss"),
 "peat_fire": ("peat","fire","indonesia","burn"),
 "antarctica_dinosaur": ("antarctica","dinosaur","fossil","amulet","drawer"),
 "youth_protein": ("youth","protein","aging","cell"),
 "asteroid_north_sea": ("asteroid","north sea","tsunami"),
}
dirs=["content/blog","content/news"]
for slug,terms in checks.items():
    hits=[]
    for d in dirs:
        p=os.path.join(ROOT,d)
        if not os.path.isdir(p): continue
        for fn in sorted(os.listdir(p)):
            if not fn.endswith(".md"): continue
            fpath=os.path.join(p,fn)
            txt=open(fpath,encoding="utf-8",errors="replace").read().lower()
            if all(t in txt for t in terms):
                hits.append(fpath.replace(ROOT+"/", ""))
    print(f"[{'DUP' if hits else 'FRESH'}] {slug} ({','.join(terms)}) -> {hits if hits else ''}")
