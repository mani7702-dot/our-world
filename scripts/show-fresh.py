#!/usr/bin/env python3
"""Show all fresh candidates with their exact URLs from the RSS feed."""
import xml.etree.ElementTree as ET
import re, glob, os

tree = ET.parse('/tmp/raw-science.xml')
root = tree.getroot()

items = []
for item in root.iter('item'):
    title_el = item.find('title')
    link_el = item.find('link')
    t = (title_el.text or '').strip() if title_el is not None else ''
    l = (link_el.text or '').strip() if link_el is not None else ''
    if t and l:
        items.append((t, l))

files = glob.glob("/home/ubuntu/our-world/content/news/*.md") + glob.glob("/home/ubuntu/our-world/content/blog/*.md")
existing_texts = {}
for f in files:
    try:
        with open(f, encoding="utf-8") as fh:
            existing_texts[f] = fh.read().lower()
    except Exception:
        pass

med_terms = re.compile(r'\b(treat|therapy|diagnos|patient|cure|disease|syndrome|vaccine|medic)\w*', re.I)
med_ok = ['slow aging', 'strength', 'mobility', 'steps', 'brain', 'heart', 'memory', 'diet', 'salt', 'sleep', 'aging', 'blueberries', 'red meat', 'diabetes', 'protein', 'youth', 'skin']
pol_terms = re.compile(r'\b(trump|musk|merger|political|government|election|riot|protest|court|war|conflict)\w*', re.I)

fresh_items = []
for i, (t, l) in enumerate(items):
    med = bool(med_terms.search(t)) and not any(e in t.lower() for e in med_ok)
    pol = bool(pol_terms.search(l))
    
    dupe_files = []
    for f, txt in existing_texts.items():
        if re.search(re.escape(t[:30]), txt, re.I):
            dupe_files.append(f)
    
    if not dupe_files and not med and not pol:
        fresh_items.append((i+1, t, l))

# Print all fresh ones
for idx, t, l in fresh_items:
    print(f"[{idx}] {t}")
    print(f"    {l}")
    print()
