#!/usr/bin/env python3
"""Scan _sci_top.xml for fresh kid-safe science candidates via release-ID dedup."""
import re, os, glob, json

BLOCK = ("war", "attack", "death toll", "killed", "murder", "court", "lawsuit",
         "covid", "pandemic", "election", "politic", "terror", "bomb", "shooting",
         "cancer", "alzheimer", "parkinson", "diabetes", "brain injury", "ptsd",
         "blood pressure", "aspirin", "cannabis", "cbn", "thc", "gummy",
         "obesity", "weight loss", "diet,", "arthritis", "inflammatory bowel",
         "crohn", "ulcerative colitis", "lung cancer", "brain cancer",
         "glioblastoma", "heart disease", "cardiovascular", "cholesterol",
         "statin", "muscle pain", "hypertension", "medication", "drug",
         "microbiome", "gene therapy", "immunotherapy", "radiation therapy",
         "clinical trial", "clinical study", "trial", "risk", "death",
         "fatal", "deadly", "vaccine", "autism", "depression", "mental health",
         "marijuana", "steroid", "hormone", "injection", "dental", "implant",
         "colorectal", "processed food", "ultra-processed", "alcohol",
         "fish oil", "omega-3", "brain shrinkage", "memory loss")

def extract_release_ids():
    ids = set()
    for f in glob.glob("/home/ubuntu/our-world/content/**/*.md", recursive=True):
        with open(f, errors="ignore") as fh:
            txt = fh.read()
        for m in re.finditer(r'/releases/(\d{4})/(\d{2})/(\d{12})\.htm', txt):
            ids.add(m.group(3))  # 12-digit ID
    return ids

existing = extract_release_ids()
print(f"Existing release IDs: {len(existing)}")

with open("/home/ubuntu/our-world/_sci_top.xml", errors="ignore") as f:
    raw = f.read()

# Strip trailing HTML comment
raw = re.sub(r"<!--.*?-->", "", raw, flags=re.S)

import xml.etree.ElementTree as ET
try:
    root = ET.fromstring(raw)
except Exception as e:
    print(f"Parse error: {e}")
    # Regex fallback
    items = re.findall(r'<item>(.*?)</item>', raw, re.S)
    root = None

fresh = []
if root is not None:
    for it in root.iter("item"):
        title = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        desc = (it.findtext("description") or "").strip()[:200]
        # Extract release ID
        m = re.search(r'/releases/(\d{4})/(\d{2})/(\d{12})\.htm', link)
        rid = m.group(3) if m else None
        if not rid:
            continue
        if rid in existing:
            continue
        # kid-safety check
        low = (title + " " + desc).lower()
        if any(b in low for b in BLOCK):
            continue
        fresh.append({"title": title, "link": link, "desc": desc, "id": rid})
else:
    for block in items:
        t = re.search(r'<title>(.*?)</title>', block, re.S)
        l = re.search(r'<link>(.*?)</link>', block, re.S)
        d = re.search(r'<description>(.*?)</description>', block, re.S)
        title = t.group(1).strip() if t else ""
        link = l.group(1).strip() if l else ""
        desc = d.group(1).strip()[:200] if d else ""
        m = re.search(r'/releases/(\d{4})/(\d{2})/(\d{12})\.htm', link)
        rid = m.group(3) if m else None
        if not rid or rid in existing:
            continue
        low = (title + " " + desc).lower()
        if any(b in low for b in BLOCK):
            continue
        fresh.append({"title": title, "link": link, "desc": desc, "id": rid})

print(f"\nFresh kid-safe candidates: {len(fresh)}")
for i, f in enumerate(fresh):
    print(f"[{i+1}] {f['title']}")
    print(f"    ID: {f['id']}")
    print(f"    URL: {f['link']}")
    print(f"    Desc: {f['desc']}")
    print()
