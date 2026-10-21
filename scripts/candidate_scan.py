#!/usr/bin/env python3
"""Scan RSS feeds for kid-safe animal candidates, flag dups and guardrails."""
import xml.etree.ElementTree as ET
import sys
import os
import re

CONTENT_DIRS = ["/home/ubuntu/our-world/content/news", "/home/ubuntu/our-world/content/blog"]

def load_existing_slugs_and_text():
    """Load all existing article titles and body text for dup checking."""
    slugs = set()
    all_text = []
    for d in CONTENT_DIRS:
        if not os.path.isdir(d):
            continue
        for fn in os.listdir(d):
            if not fn.endswith(".md"):
                continue
            slug = fn[:-3]
            slugs.add(slug)
            fp = os.path.join(d, fn)
            try:
                with open(fp, "r", encoding="utf-8") as f:
                    txt = f.read().lower()
                    all_text.append(txt)
            except Exception:
                pass
    return slugs, all_text

def is_duplicate(title, desc, existing_slugs, existing_texts):
    """Check if this candidate is already published."""
    tl = title.lower()
    dl = desc.lower()
    combined = tl + " " + dl
    # Check slugs
    for slug in existing_slugs:
        slug_words = slug.replace("-", " ").lower()
        if slug_words in tl:
            return True
    # Check stable core tokens in existing text
    tokens = re.findall(r'\b\w{4,}\b', combined)
    for text in existing_texts:
        matches = 0
        for tok in tokens:
            if tok not in ("this", "that", "with", "from", "have", "will", "their", "they", "what", "when", "where", "which", "scient", "research", "scientists", "discov", "study", "found", "new", "first", "could", "may", "might", "some"):
                if tok in text:
                    matches += 1
        if matches >= 5:
            return True
    return False

def is_medical_block(title, desc):
    """Medical guardrail."""
    text = (title + " " + desc).lower()
    medical_kw = [
        "alzheimer", "cancer", "treatment", "therapy", "diagnos", "patient",
        "disease", "disorder", "mental health", "depression", "anxiety",
        "autism", "adhd", "brain damage", "brain injury",
        "diabetes", "heart disease", "cholesterol", "statin",
        "immune system", "vaccine", "covid", "infection", "poisoning",
        "addiction", "tumor", "stroke", "dementia", "neuroscience",
        "psychiatric", "psychological", "clinical",
    ]
    return any(k in text for k in medical_kw)

def is_political_block(title, desc):
    """Political/world-affairs guardrail."""
    text = (title + " " + desc).lower()
    pol_kw = [
        "political", "government", "election", "parliament", "senate", "congress",
        "trump", "biden", "musk", "merger", "deal", "agreement",
        "war", "conflict", "military", "army", "attack", "battle",
        "protest", "riot", "strike", "sanction", "treaty",
        "leadership", "minister", "president", "diplomatic",
    ]
    return any(k in text for k in pol_kw)

def is_violent_block(title, desc):
    """Violence guardrail."""
    text = (title + " " + desc).lower()
    violent_kw = [
        "killed", "murder", "death", "die", "dead", "casualty",
        "violent", "attack", "terrorist", "terror",
        "massacre", "genocide", "mass violence",
    ]
    return any(k in text for k in violent_kw)

def is_animal_related(title, desc):
    """Check if candidate is animal-related."""
    text = (title + " " + desc).lower()
    animal_kw = [
        "animal", "wildlife", "bird", "fish", "whale", "dolphin", "turtle",
        "shark", "bear", "elephant", "monkey", "ape", "cat", "dog", "bat",
        "bee", "butterfly", "insect", "species", "habitat", "conservation",
        "rescue", "endangered", "migrat", "crayfish", "crustacean", "coral",
        "reptile", "amphibian", "mammal", "predator", "prey",
        "ecosystem", "biodiversity", "fauna", "zoo", "aquarium",
    ]
    return any(k in text for k in animal_kw)

def parse_feed(path):
    """Parse RSS feed and return list of (title, link, desc)."""
    candidates = []
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        items = root.findall(".//item")
        for it in items:
            title = it.findtext("title", "").strip()
            link = it.findtext("link", "").strip()
            desc = it.findtext("description", "").strip()
            if title and link:
                candidates.append((title, link, desc))
    except Exception as e:
        print(f"ERROR parsing {path}: {e}", file=sys.stderr)
    return candidates

def main():
    slugs, texts = load_existing_slugs_and_text()
    print(f"Loaded {len(slugs)} existing slugs, {len(texts)} existing texts")

    feeds = [
        ("/tmp/sdi_top.xml", "ScienceDaily top"),
        ("/tmp/bbc_science.xml", "BBC Science"),
        ("/tmp/gnn.xml", "GNN"),
    ]

    fresh_animals = []
    for feed_path, feed_name in feeds:
        if not os.path.exists(feed_path):
            print(f"Feed not found: {feed_path}")
            continue
        candidates = parse_feed(feed_path)
        print(f"\n=== {feed_name}: {len(candidates)} items ===")
        for title, link, desc in candidates:
            if not is_animal_related(title, desc):
                continue
            animal = is_animal_related(title, desc)
            dup = is_duplicate(title, desc, slugs, texts)
            med = is_medical_block(title, desc)
            pol = is_political_block(title, desc)
            viol = is_violent_block(title, desc)
            status = "DUP" if dup else ("MED-BLOCK" if med else ("POL-BLOCK" if pol else ("VIOLENT-BLOCK" if viol else "FRESH")))
            print(f"[{status}] {title[:100]}")
            print(f"  URL: {link}")
            if not dup and not med and not pol and not viol:
                fresh_animals.append((title, link, desc, feed_name))

    print(f"\n=== FRESH ANIMAL CANDIDATES: {len(fresh_animals)} ===")
    for title, link, desc, source in fresh_animals:
        print(f"\nTITLE: {title}")
        print(f"URL: {link}")
        print(f"SOURCE: {source}")
        print(f"DESC: {desc[:300]}")

if __name__ == "__main__":
    main()
