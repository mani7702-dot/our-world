#!/usr/bin/env python3
"""Scan Smithsonian feed for kid-safe animal candidates."""
import xml.etree.ElementTree as ET
import os
import re

CONTENT_DIRS = ["/home/ubuntu/our-world/content/news", "/home/ubuntu/our-world/content/blog"]

def load_existing_texts():
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

def is_duplicate(title, desc, slugs, texts):
    tl = title.lower() + " " + desc.lower()
    for slug in slugs:
        if slug.replace("-", " ").lower() in tl:
            return True
    tokens = re.findall(r'\b\w{4,}\b', tl)
    for text in texts:
        matches = sum(1 for tok in tokens if tok not in ("this","that","with","from","have","will","their","they","what","when","where","which","scient","research","scientists","discov","study","found","new","first","could","may","might","some","more","than","have","been","were","said") and tok in text)
        if matches >= 6:
            return True
    return False

def is_medical_block(text):
    kw = ["alzheimer","cancer","treatment","therapy","diagnos","patient","disease","disorder","mental health","depression","anxiety","autism","adhd","brain damage","brain injury","diabetes","cholesterol","statin","immune system","vaccine","covid","infection","poisoning","addiction","tumor","stroke","dementia","neuroscience","psychiatric","psychological","clinical"]
    return any(k in text for k in kw)

def is_political_block(text):
    kw = ["political","government","election","parliament","senate","congress","trump","biden","musk","merger","deal","agreement","war","conflict","military","army","attack","battle","protest","riot","strike","sanction","treaty","leadership","minister","president","diplomatic"]
    return any(k in text for k in kw)

def is_animal_related(text):
    kw = ["animal","wildlife","bird","fish","whale","dolphin","turtle","shark","bear","elephant","monkey","ape","cat","dog","bat","bee","butterfly","insect","species","habitat","conservation","rescue","endangered","migrat","crayfish","crustacean","coral","reptile","amphibian","mammal","predator","prey","ecosystem","biodiversity","fauna","zoo","aquarium","farm","farmer","cattle","cow","pig","horse","sheep","goat","poultry","livestock"]
    return any(k in text for k in kw)

def main():
    slugs, texts = load_existing_texts()
    print(f"Loaded {len(slugs)} existing slugs")

    tree = ET.parse("/tmp/smithsonian.xml")
    root = tree.getroot()
    items = root.findall(".//item")
    print(f"Smithsonian: {len(items)} items")

    fresh = []
    for it in items:
        title = it.findtext("title","").strip()
        link = it.findtext("link","").strip()
        desc = it.findtext("description","").strip()[:300]
        text = (title + " " + desc).lower()
        if not is_animal_related(text):
            continue
        dup = is_duplicate(title, desc, slugs, texts)
        med = is_medical_block(text)
        pol = is_political_block(text)
        status = "DUP" if dup else ("MED-BLOCK" if med else ("POL-BLOCK" if pol else "FRESH"))
        print(f"[{status}] {title[:120]}")
        print(f"  URL: {link}")
        if not dup and not med and not pol:
            fresh.append((title, link, desc))

    print(f"\n=== FRESH ANIMAL FROM SMITHSONIAN: {len(fresh)} ===")
    for title, link, desc in fresh:
        print(f"\nTITLE: {title}")
        print(f"URL: {link}")
        print(f"DESC: {desc}")

if __name__ == "__main__":
    main()
