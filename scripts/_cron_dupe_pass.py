#!/usr/bin/env python3
"""Dupes + guardrails pass over every trending-candidate from raw RSS.
Checks against BOTH content/blog and content/news using stable core tokens.
Tirith-safe: file-based, no curl|python3, no backslash-heavy inline body."""
import os, re, sys

NEWS = "content/news"
BLOG = "content/blog"

CANDIDATES = {
    # (slug, [(token1, token2, ...)])
    "doomsday-prediction-nov-13-2026": ("doomsday", "november 13", "2026", "population explosion", "brave new world"),
    "crawzilla-giant-crayfish-tennessee": ("crawzilla", "crayfish", "tennessee", "giant crayfish"),
    "webb-wild-weather-20-light-year-world": ("wild weather", "20 light-year", "tepid", "atmospheric state"),
    "ghostly-green-star-white-dwarf": ("green star", "green star", "white dwarf", "wdj"),
    "two-monster-black-holes-collide-100-years": ("two monster black holes", "mrk 501", "supermassive black holes", "collision"),
    "how-deep-sleep-builds-muscle": ("deep sleep", "growth hormone", "muscle", "sleep builds"),
    "scientists-discover-eyeless-cave-snail-china": ("eyeless", "cave snail", "chinese cave", "ghostly"),
    "train-delayed-by-solar-storm": ("train delayed", "solar storm", "1848", "brigadoon"),
    "silverpit-crater-tsunami-north-sea": ("silverpit", "tsunami", "north sea", "asteroid"),
    "magic-mushroom-fish-aggression": ("magic mushroom", "psilocybin", "aggressive fish", "aggression"),
    "altermagnetism-third-magnetism": ("altermagnetism", "third form of magnetism", "magnetic"),
    "masaya-volcano-magma": ("masaya", "magma", "nicaragua", "volcano"),
    "spacex-jellyfish-launch": ("jellyfish", "spacex", "crs-35", "jellyfish launch"),
    "amazon-hidden-fires": ("amazon", "hidden fires", "el nino", "rainforest"),
    "roman-telescope-nasa": ("roman telescope", "nancy grace roman", "telescope exceeds"),
    "bennu-boulders": ("bennu", "boulders", "osiris-rex", "cracks"),
    "arctic-sea-ice-low-2026": ("arctic sea ice", "arctic", "sea ice", "record low"),
    "green-star-white-dwarf": ("green star", "white dwarf", "color", "wdj1330"),
    "coral-recovery-touch": ("coral", "bleaching", "recovery", "touch"),
    "ultra-processed-food-cancer": ("ultra-processed", "colorectal cancer", "460000", "food"),
    "freud-neuroscience-rediscovery": ("freud", "neuroscience", "prediction", "brain"),
    "perseverance-mars-driving-record": ("perseverance", "mars", "driving record", "autonav"),
    "colorectal-cancer-ultra-processed": ("ultra-processed", "colorectal", "cancer", "460000"),
    "reverse-cellular-aging": ("reverse aging", "cellular aging", "stem cells", "80-year-old"),
    "statins-muscle-pain": ("statins", "muscle pain", "cholesterol"),
    "alzheimers-sleep-immune-cells": ("alzheimer", "sleep", "immune cells", "plaque"),
    "vitamin-c-cancer-survival": ("vitamin c", "cancer", "survival", "precancerous"),
    "salt-sugar-diabetes-risk": ("sugar", "red meat", "diabetes", "63"),
    "blueberries-mood-depression": ("blueberries", "mood", "depression", "older adults"),
    "volcanic-apocalypse-japan": ("volcanic apocalypse", "kikai", "japan", "7300 years"),
    "brain-cells-cognitive-decline": ("brain cells", "cognitive decline", "protective"),
    "skin-cells-males-females": ("skin cells", "male", "female", "different rules"),
    "alzheimers-sleep-restored": ("alzheimer", "sleep", "two hours", "immune cells"),
    "dinosaur-squid-wyoming": ("squid", "belemnite", "jurassic", "wyoming", "barrel"),
    "astronauts-hearts-mars": ("astronaut", "heart", "mars", "spaceflight"),
    "sleep-growth-hormone": ("sleep", "growth hormone", "brain", "two-way"),
    "sweeteners-gut-bacteria": ("sweetener", "gut bacteria", "gut microbes", "sugar"),
    "fatty-liver-drug-gut": ("fatty liver", "drug", "gut", "microbiome"),
    "black-holes-collide-mrk501": ("black hole", "mrk 501", "collision", "supermassive"),
    "youth-protein-aging-brain": ("youth protein", "aging brain", "brain cells", "protein"),
    "alzheimers-high-risk-gene": ("alzheimer", "high-risk gene", "genetic", "mutation"),
    "nobel-prize-brain-light": ("nobel prize", "brain", "light", "opsin", "algae"),
    "taste-covid-lingering": ("taste", "covid", "lingering", "taste buds"),
    "quantum-fermi-sea": ("fermi sea", "quantum", "ultracold atoms", "fractional"),
    "nasa-doomsday-november-13": ("doomsday", "november 13", "2026", "population explosion"),
    "crawfish-crayfish-record": ("crawfish", "crayfish", "record", "tennessee"),
}

MED = ("treatment", "therapy", "diagnos", "mental disorder", "cure", "patients with", "condition", "alzheimer", "cancer", "depression", "diabetes", "liver disease", "blood cancer", "brain damage")
POL = ("politic", "election", "court ", "lawsuit", "terror", "bomb", "shooting", "war ", "attack", "nuclear", "nazi", "spy", "intelligence operation", "treason", "drug raid")
VIOLENT = ("behead", "murder", "killed", "death", "slaughter", "massacre", "abducted", "kidnap", "horror", "scary", "terror")

def scan_all():
    allfiles = []
    for d in [NEWS, BLOG]:
        if os.path.isdir(d):
            for f in os.listdir(d):
                if f.endswith(".md"):
                    allfiles.append(os.path.join(d, f))
    return allfiles

def main():
    files = scan_all()
    print(f"Total existing articles: {len(files)}")
    print("=" * 70)
    for slug, tokens in CANDIDATES.items():
        found_dup = []
        for tf in tokens:
            for fp in files:
                try:
                    txt = open(fp, encoding="utf-8", errors="ignore").read().lower()
                    if tf.lower() in txt:
                        found_dup.append(fp)
                except Exception:
                    continue
        found_dup = list(set(found_dup))
        if found_dup:
            print(f"DUP: {slug} -> matched tokens in: {found_dup[:2]}")
        else:
            # check guardrails on slug (rough)
            slug_lower = slug.lower()
            blocked = []
            for b in MED:
                if b in slug_lower:
                    blocked.append(f"MED:{b}")
            for b in POL:
                if b in slug_lower:
                    blocked.append(f"POL:{b}")
            for b in VIOLENT:
                if b in slug_lower:
                    blocked.append(f"VIOLENT:{b}")
            if blocked:
                print(f"BLOCKED: {slug} -> {blocked}")
            else:
                print(f"FRESH-KID-SAFE: {slug}")

if __name__ == "__main__":
    main()
