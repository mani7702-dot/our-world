#!/usr/bin/env python3
"""Fetch ScienceDaily top.xml and find fresh, kid-safe candidates via release-ID dedup."""
import re, glob, urllib.request, gzip, sys

# Load existing release IDs from all content/**/*.md files
existing_ids = set()
for f in glob.glob('content/**/*.md', recursive=True):
    try:
        txt = open(f, encoding='utf-8', errors='replace').read()
    except Exception:
        continue
    for m in re.finditer(r'releases/(\d+)/(\d+)/(\d+)\.htm', txt):
        existing_ids.add(m.group(3))

print(f"[dedup] Existing release IDs in content/**: {len(existing_ids)}")

# Fetch live ScienceDaily top.xml
url = "https://www.sciencedaily.com/rss/top.xml"
req = urllib.request.Request(url, headers={
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept": "application/xml,application/rss+xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
})
try:
    raw = urllib.request.urlopen(req, timeout=30).read()
    # Handle potential gzip
    if raw[:2] == b'\x1f\x8b':
        raw = gzip.decompress(raw)
    xml_text = raw.decode('utf-8', errors='replace')
except Exception as e:
    print(f"[fetch] Error fetching live feed: {e}", file=sys.stderr)
    sys.exit(1)

# Also try cached _sci_top.xml as fallback
cached_ids_fresh = 0
try:
    cached = open('_sci_top.xml', encoding='utf-8', errors='replace').read()
except Exception:
    cached = ''

# Parse items from live feed
items = []
for m in re.finditer(r'<item>(.*?)</item>', xml_text, re.DOTALL):
    block = m.group(1)
    title_m = re.search(r'<title>(.*?)</title>', block, re.DOTALL)
    link_m = re.search(r'<link>(.*?)</link>', block, re.DOTALL)
    desc_m = re.search(r'<description>(.*?)</description>', block, re.DOTALL)
    title = title_m.group(1).strip() if title_m else ''
    link = link_m.group(1).strip() if link_m else ''
    desc = desc_m.group(1).strip() if desc_m else ''
    # Extract release ID
    rid_m = re.search(r'releases/(\d+)/(\d+)/(\d+)\.htm', link)
    rid = rid_m.group(3) if rid_m else ''
    items.append({'title': title, 'link': link, 'desc': desc, 'rid': rid})

print(f"[fetch] Live ScienceDaily top.xml: {len(items)} items")

# Find FRESH (unpublished) items
medical_kw = ['cancer', 'cure', 'cured', 'disease', 'dementia', 'alzheimer', 'diabetes',
              'depression', 'anxiety', 'depress', 'ptsd', 'parkinson', 'aspirin', 'blood pressure',
              'brain health', 'memory loss', 'tumor', 'tumour', 'obesity', 'heart disease',
              'stroke', 'covid', 'vaccine', 'treatment', 'drug', 'medication', 'clinical trial',
              'supplement', 'omega-3', 'fish oil', 'processed food cancer', 'cavity', 'drilling',
              'dentist', 'oral', 'teeth']
reject_kw = ['cancer', 'medical', 'health', 'disease', 'clinical', 'treatment', 'drug', 'therapy',
             'depression', 'anxiety', 'ptsd', 'dementia', 'alzheimer', 'parkinson', 'stroke',
             'heart disease', 'covid', 'vaccine', 'aspirin', 'blood pressure']

fresh = []
for it in items:
    if not it['rid']:
        continue
    if it['rid'] in existing_ids:
        continue
    title_lower = it['title'].lower()
    # Kid-safety filter: reject medical/health
    is_medical = any(k in title_lower for k in reject_kw)
    is_medical_desc = any(k in it['desc'].lower() for k in medical_kw[:10])
    if is_medical or is_medical_desc:
        continue
    fresh.append(it)

print(f"\n[FRESH] {len(fresh)} unpublished kid-safe candidates:")
for i, it in enumerate(fresh[:20]):
    print(f"  {i+1}. [{it['rid']}] {it['title']}")
    print(f"     URL: {it['link']}")
    print(f"     DESC: {it['desc'][:120]}")
    print()
