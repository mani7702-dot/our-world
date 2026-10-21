#!/usr/bin/env python3
"""Parse all raw ScienceDaily RSS items — show 21-40 with FRESH candidates."""
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
med_block_exceptions = ['slow aging', 'strength', 'mobility', 'steps', 'brain', 'heart', 'memory', 'diet']
pol_terms = re.compile(r'\b(trump|musk|merger|political|government|election|riot|protest|court|war|conflict)\w*', re.I)

for i in range(20, min(len(items), 50)):
    t, l = items[i]
    med = bool(med_terms.search(t)) and not any(e in t.lower() for e in med_block_exceptions)
    pol = bool(pol_terms.search(t))
    
    dupe_files = []
    for f, txt in existing_texts.items():
        if re.search(re.escape(t[:30]), txt, re.I):
            dupe_files.append(f)
    
    status = []
    if dupe_files:
        status.append(f"DUP")
    if med:
        status.append("MED-BLOCK")
    if pol:
        status.append("POL-BLOCK")
    verdict = " | ".join(status) if status else "FRESH"
    
    # Highlight interesting ones
    interesting = any(kw in t.lower() for kw in ['asteroid', 'tsunami', 'mars', 'bennu', 'nasa', 'deepest', 'ancient', 'record', 'giant', 'massive', 'mystery', 'discovery', 'ghostly', 'eyeless'])
    marker = " ***" if (verdict == "FRESH" and interesting) else ""
    
    print(f"[{i+1}] {verdict:12} | {t}{marker}")
    if dupe_files:
        for df in dupe_files[:1]:
            print(f"    dupe: {os.path.basename(df)}")
    print(f"    url: {l}")
    print()
