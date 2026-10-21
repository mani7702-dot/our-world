#!/usr/bin/env python3
"""Check more candidates more precisely + look for stable tokens."""
import re, glob

candidates = {
    "gut-bacteria-c-diff": ["c. diff", "clostridium difficile", "gut microbiome", "good bacteria", "dangerous gut bacteria"],
    "blueberries-mood": ["blueberries", "mood", "surprising effect", "berries every day", "eat blueberries"],
    "red-meat-sugar-diabetes": ["sugar", "red meat", "diabetes", "63% higher", "neu5", "neu5gc", "cancer"],
    "skin-male-female-different": ["male and female skin", "skin play", "different rules", "skin cells", "sex differences skin"],
    "youth-protein-brain-cells": ["youth protein", "brain cells", "aging brain", "act young again", "protein helps"],
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
            print(f"  {f} -> {hits}")
    else:
        print(f"[{key}] FRESH - no multi-token match with 2+ hits")

# Check medical concern
print("\n=== MEDICAL GUARDRAIL CHECK ===")
for key, tokens in candidates.items():
    med_hits = [t for t in ["disease", "treat", "therapy", "cure", "drug", "diagnos", "patient", "cancer", "alzheim", "diabet", "brain damage", "neurodegener"] if t in key.lower()]
    # also check if the candidate is about a disease treatment
    med_concern = ""
    if "c diff" in key or "difficile" in " ".join(tokens):
        med_concern = "C. diff is a medical infection topic"
    if "blueberries" in key:
        med_concern = "mood/behavior - generally safe for kids"
    if "diabetes" in key or "sugar" in key:
        med_concern = "diabetes risk - borderline medical"
    if "brain" in key and "aging" in key:
        med_concern = "brain aging - borderline medical"
    if "skin" in key:
        med_concern = "skin biology - safe for kids"
    if key == "youth-protein-brain-cells":
        med_concern = "brain aging / youth protein - borderline medical"
    print(f"  [{key}] {med_concern}")
