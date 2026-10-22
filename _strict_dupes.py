#!/usr/bin/env python3
"""Literal dupe grep — strict: every term must appear in the file."""
import os
ROOT = "/home/ubuntu/our-world"
checks = {
    "masaya_volcano": ("masaya", "volcano"),
    "jackdaw": ("jackdaw",),
    "mexico_treason": ("treason", "jáuregui"),
    "trump_green_card": ("green card", "indian", "tech worker"),
    "freud_neuroscience": ("freud", "neuroscience"),
}
dirs = [os.path.join(ROOT,"content/blog"), os.path.join(ROOT,"content/news")]
for slug, terms in checks.items():
    hits=[]
    for d in dirs:
        if not os.path.isdir(d): continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".md"): continue
            p=os.path.join(d,fn)
            txt=open(p,encoding="utf-8",errors="replace").read().lower()
            if all(t.lower() in txt for t in terms):
                hits.append(p.replace(ROOT+"/", ""))
    print(f"[{'DUP' if hits else 'FRESH'}] {slug} ({', '.join(terms)}) -> {hits if hits else ''}")
