#!/usr/bin/env python3
"""Tirith-safe: precise dup-grep for specific candidate slugs. Skip generic words."""
import os, re
CONTENT_DIRS = ["/home/ubuntu/our-world/content/news", "/home/ubuntu/our-world/content/blog"]

def grep_any(term):
    hits=[]
    for d in CONTENT_DIRS:
        if not os.path.isdir(d): continue
        for fn in os.listdir(d):
            p=os.path.join(d,fn)
            try: txt=open(p,encoding="utf-8",errors="ignore").read()
            except: continue
            if re.search(term, txt, re.I):
                hits.append(p)
    return hits

CANDS = {
 "fin-whale-welsh-coast": ["fin whale", "fin whale", "wales"],
 "ww2-calculator": ["ww2", "calculator", "calculator"],
 "windermere-tunnel": ["windermere", "windermere", "sewage tunnel"],
 "dino-antarctica": ["antarctica", "antarctica", "dinosaur"],
 "roman-temple-germany": ["roman temple", "frankfurt limes", "roman fort"],
 "red-squirrels-jersey": ["red squirrel", "jersey", "channel islands"],
}
for slug,terms in CANDS.items():
    fresh=True
    for t in terms:
        hits=grep_any(re.escape(t))
        if hits:
            fresh=False
            print(f"  [{slug}] term='{t}' -> DUP {hits}")
            break
    if fresh:
        print(f"  [{slug}] FRESH (no dupes for terms {terms})")
