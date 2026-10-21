#!/usr/bin/env python3
"""Check remaining fresh candidates and download them for cross-check."""
import re, glob, os

# The genuinely fresh ones from the RSS parse
candidates = {
    "ghostly-eyeless-cave-creature": ["ghostly", "eyeless", "chinese cave", "cave", "snail"],
    "gut-bacteria-c-diff": ["c diff", "clostridium", "gut bacteria", "dangerous gut"],
    "quantum-limit-surface": ["quantum limit", "surface", "ultimate quantum"],
    "brain-salt-compound": ["salt", "brain", "compound", "too much salt"],
    "crawzilla-crayfish": ["crawzilla", "crayfish", "huge", "bigger"],
    "doomsday-prediction-2026": ["doomsday", "november 13", "2026", "prediction"],
    "blueberries-mood": ["blueberries", "mood", "surprising effect"],
    "red-meat-sugar-diabetes": ["sugar", "red meat", "diabetes", "63 percent"],
    "skin-male-female-different": ["male and female skin", "skin", "different rules"],
    "youth-protein-brain-cells": ["youth protein", "brain cells", "aging brain"],
}

files = glob.glob("/home/ubuntu/our-world/content/news/*.md") + glob.glob("/home/ubuntu/our-world/content/blog/*.md")

for key, tokens in candidates.items():
    found = []
    for f in files:
        try:
            with open(f, encoding="utf-8") as fh:
                txt = fh.read().lower()
        except:
            continue
        hits = [t for t in tokens if t.lower() in txt]
        if len(hits) >= 2:
            found.append((f, hits))
    if found:
        print(f"[{key}] DUP - matches:")
        for f, hits in found:
            print(f"  {os.path.basename(f)} -> {hits}")
    else:
        print(f"[{key}] FRESH - no multi-token match")
    
import os
