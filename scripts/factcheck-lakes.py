#!/usr/bin/env python3
"""Targeted fact-check: grep Wikipedia saves for Listverse lake claims. Tirith-safe."""
CLAIMS = {
    "/tmp/wiki-natron.html": [
        ("calcium carbonate", "Lake Natron turns animals to stone - calcium carbonate casts"),
        ("alkaline", "Lake Natron is alkaline (pH ~10-12)"),
        ("red", "Lake Natron water appears red"),
    ],
    "/tmp/wiki-abraham.html": [
        ("methane", "Abraham Lake ice bubbles are methane"),
        ("bubbles", "methane bubbles frozen in ice"),
    ],
    "/tmp/wiki-kaindy.html": [
        ("1911", "Kaindy Lake formed by 1911 earthquake landslide"),
        ("underwater forest", "underwater drowned forest"),
    ],
    "/tmp/wiki-jelly.html": [
        ("golden jellyfish", "Jellyfish Lake has golden jellyfish migration"),
        ("Mastigias", "Mastigias papua subspecies"),
    ],
}
import re, html as H
for path, checks in CLAIMS.items():
    try:
        h = open(path, encoding="utf-8", errors="ignore").read()
    except FileNotFoundError:
        print(f"{path}: NOT FOUND"); continue
    t = re.sub(r'<[^>]+>', ' ', h)
    t = H.unescape(t)
    t = re.sub(r'\s+', ' ', t).lower()
    print(f"=== {path.split('/')[-1]} ===")
    for term, claim in checks:
        if term.lower() in t:
            print(f"  [CONFIRMED] {claim}")
        else:
            print(f"  [NOT FOUND] '{term}' for: {claim}")
    print()
