#!/usr/bin/env python3
"""Download and parse BBC Science & Environment feed for animal stories."""
import xml.etree.ElementTree as ET
import os
import re

CONTENT_DIRS = ["/home/ubuntu/our-world/content/news", "/home/ubuntu/our-world/content/blog"]

def load_existing():
    all_text = []
    slugs = set()
    for d in CONTENT_DIRS:
        if not os.path.isdir(d):
            continue
        for fn in os.listdir(d):
            if not fn.endswith(".md"):
                continue
            slugs.add(fn[:-3])
            try:
                with open(os.path.join(d, fn), "r", encoding="utf-8") as f:
                    all_text.append(f.read().lower())
            except Exception:
                pass
    return slugs, all_text

def main():
    slugs, texts = load_existing()

    # Parse BBC Science feed
    tree = ET.parse("/tmp/bbc_science.xml")
    root = tree.getroot()
    items = root.findall(".//item")

    # Check each item for animal keywords
    animal_kw = [
        "bat", "wildlife", "animal", "bird", "whale", "dolphin", "turtle",
        "shark", "bear", "elephant", "monkey", "ape", "insect", "butterfly",
        "species", "habitat", "conservation", "rescue", "endangered",
        "migrat", "coral", "reptile", "amphibian", "mammal", "predator",
        "ecosystem", "biodiversity", "fauna", "crustacean", "crayfish",
        "squirrel", "capybara", "owl", "farmer", "farm", "nest", "wasp",
        "bee", "pollinator", "cattle", "cows", "livestock",
    ]

    for it in items:
        title = it.findtext("title","").strip()
        link = it.findtext("link","").strip()
        desc = it.findtext("description","").strip()
        text = (title + " " + desc).lower()

        is_animal = any(k in text for k in animal_kw)
        # Check if it's a dup
        title_lower = title.lower()
        is_dup = False
        for slug in slugs:
            slug_words = slug.replace("-", " ").lower()
            if slug_words in title_lower:
                is_dup = True
                break
        if not is_dup:
            # Check stable tokens
            title_tokens = re.findall(r'\b\w{5,}\b', title_lower)
            for existing_text in texts:
                matches = sum(1 for tok in title_tokens
                              if tok not in ("scientists", "research", "study", "found", "first",
                                             "could", "may", "might", "some", "more", "than",
                                             "been", "were", "said", "their", "they", "have",
                                             "this", "that", "with", "from")
                          and tok in existing_text)
                if matches >= 4:
                    is_dup = True
                    break

        if is_animal and not is_dup:
            print(f"FRESH+ANIMAL: {title}")
            print(f"  URL: {link}")
            print(f"  DESC: {desc[:300]}")
            print()

if __name__ == "__main__":
    main()
