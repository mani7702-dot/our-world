#!/usr/bin/env python3
"""Parse raw ScienceDaily RSS and list all headlines for abort pass."""
import xml.etree.ElementTree as ET
import re, glob, os

# Parse the downloaded XML
tree = ET.parse('/tmp/raw-science.xml')
root = tree.getroot()

items = []
for item in root.iter('item'):
    title_el = item.find('title')
    link_el = item.find('link')
    desc_el = item.find('description')
    t = (title_el.text or '').strip() if title_el is not None else ''
    l = (link_el.text or '').strip() if link_el is not None else ''
    d = (desc_el.text or '').strip()[:200] if desc_el is not None else ''
    if t and l:
        items.append((t, l, d))

# Load all existing content for dupe-grep
files = glob.glob("/home/ubuntu/our-world/content/news/*.md") + glob.glob("/home/ubuntu/our-world/content/blog/*.md")
existing_texts = {}
for f in files:
    try:
        with open(f, encoding="utf-8") as fh:
            existing_texts[f] = fh.read().lower()
    except Exception:
        pass

med_terms = re.compile(r'\b(treat|therapy|diagnos|mental disorder|patient|cure|remedy|disease|syndrome|vaccine|medic)\w*', re.I)
pol_terms = re.compile(r'\b(trump|musk|merger|political|opposition|government|election|war|conflict|riot|protest|court|trial|crime|attack|violence|terror|murder)\w*', re.I)

# Extract ScienceDaily release ID from URL for dedup
def sd_release_id(url):
    m = re.search(r'/releases/(\d{8})/', url)
    return m.group(1) if m else None

# Collect existing SD release IDs
existing_ids = set()
for f, txt in existing_texts.items():
    ids = re.findall(r'sciencedaily\.com/releases/(\d{8})', txt)
    existing_ids.update(ids)
# also check frontmatter links
for f in files:
    try:
        with open(f) as fh:
            for line in fh:
                m = sd_release_id(line)
                if m:
                    existing_ids.add(m)
    except:
        pass

print(f"Existing SD release IDs in content: {existing_ids}")
print()

for i, (t, l, d) in enumerate(items[:20]):
    sd_id = sd_release_id(l)
    # Check med/pol
    med = bool(med_terms.search(t))
    pol = bool(pol_terms.search(t))
    
    # Check dupe by literal headline
    dupe_files = []
    for f, txt in existing_texts.items():
        if re.search(re.escape(t[:30]), txt, re.I):
            dupe_files.append(f)
    
    # Check SD release ID dupe
    id_dupe = sd_id in existing_ids if sd_id else False
    
    status = []
    if id_dupe:
        status.append("SD-ID-DUP")
    elif dupe_files:
        status.append(f"LIT-DUP({len(dupe_files)})")
    if med:
        status.append("MED-BLOCK")
    if pol:
        status.append("POL-BLOCK")
    verdict = " | ".join(status) if status else "FRESH"
    
    print(f"[{i+1}] {verdict:15} | SD_ID:{sd_id or '-'} | {t}")
    if dupe_files:
        for df in dupe_files[:2]:
            print(f"    dupe: {df}")
    if d:
        print(f"    desc: {d[:120]}")
    print()
