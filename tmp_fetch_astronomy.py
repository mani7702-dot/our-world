#!/usr/bin/env python3
"""Scan ScienceDaily astronomy RSS feeds for fresh kid-safe candidates."""
import re, glob, urllib.request, gzip, sys

# Load existing release IDs
existing_ids = set()
for f in glob.glob('content/**/*.md', recursive=True):
    try:
        txt = open(f, encoding='utf-8', errors='replace').read()
    except:
        continue
    for m in re.finditer(r'releases/(\d+)/(\d+)/(\d+)\.htm', txt):
        existing_ids.add(m.group(3))
print(f"[dedup] Existing release IDs: {len(existing_ids)}")

urls = [
    ("astronomy.xml", "https://www.sciencedaily.com/rss/space_time/astronomy.xml"),
    ("solar_system.xml", "https://www.sciencedaily.com/rss/space_time/solar_system.xml"),
    ("space_telescopes.xml", "https://www.sciencedaily.com/rss/space_telescopes.xml"),
]

medical_kw = ['cancer', 'disease', 'dementia', 'alzheimer', 'diabetes', 'depression',
              'anxiety', 'ptsd', 'parkinson', 'aspirin', 'blood pressure', 'clinical trial',
              'drug', 'therapy', 'treatment', 'medication', 'cavity', 'tooth', 'brain health',
              'omega-3', 'alcohol', 'gummies', 'cannabis', 'implant', 'infection', 'antibiotic']

all_fresh = []
for name, url in urls:
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
    })
    try:
        raw = urllib.request.urlopen(req, timeout=30).read()
        if raw[:2] == b'\x1f\x8b':
            raw = gzip.decompress(raw)
        xml_text = raw.decode('utf-8', errors='replace')
        if '<html' in xml_text.lower()[:500]:
            print(f"[{name}] returned HTML, not XML — directory listing?")
            continue
    except Exception as e:
        print(f"[{name}] fetch error: {e}")
        continue

    items = []
    for m in re.finditer(r'<item>(.*?)</item>', xml_text, re.DOTALL):
        block = m.group(1)
        title_m = re.search(r'<title>(.*?)</title>', block, re.DOTALL)
        link_m = re.search(r'<link>(.*?)</link>', block, re.DOTALL)
        desc_m = re.search(r'<description>(.*?)</description>', block, re.DOTALL)
        title = title_m.group(1).strip() if title_m else ''
        link = link_m.group(1).strip() if link_m else ''
        desc = desc_m.group(1).strip() if desc_m else ''
        rid_m = re.search(r'releases/(\d+)/(\d+)/(\d+)\.htm', link)
        rid = rid_m.group(3) if rid_m else ''
        items.append({'title': title, 'link': link, 'desc': desc, 'rid': rid})

    print(f"\n[{name}] {len(items)} items")
    fresh = []
    for it in items:
        if not it['rid'] or it['rid'] in existing_ids:
            continue
        # Kid-safety: reject medical keywords
        blob = (it['title'] + ' ' + it['desc']).lower()
        if any(k in blob for k in medical_kw):
            continue
        fresh.append(it)
    print(f"  FRESH kid-safe: {len(fresh)}")
    for i, it in enumerate(fresh[:15]):
        print(f"  {i+1}. [{it['rid']}] {it['title']}")
        print(f"     URL: {it['link']}")
        print(f"     DESC: {it['desc'][:150]}")
        print()
    all_fresh.extend(fresh)

print(f"\n=== TOTAL FRESH ASTRONOMY CANDIDATES: {len(all_fresh)} ===")
