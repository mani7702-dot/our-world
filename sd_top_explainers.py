#!/usr/bin/env python3
"""Tirith-safe standalone: sweep ScienceDaily top.xml for explainers lane.
Dedup by release-ID against ALL content/**/*.md files.
"""
import urllib.request
import xml.etree.ElementTree as ET
import re
import os
import glob
from datetime import datetime, timezone

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

BLOCK = ('war', 'attack', 'death toll', 'killed', 'killing', 'murder', 'court', 'lawsuit',
         'covid', 'pandemic', 'election', 'politic', 'terror', 'bomb', 'shooting', 'death',
         'dies', 'rape', 'assault', 'crash', 'collision', 'disaster', 'fatal', 'dead',
         'disease', 'cancer', 'tumor', 'virus', 'outbreak', 'epidemic', 'clinical', 'treatment',
         'cure', 'therapy', 'patient', 'illness', 'syndrome', 'symptom', 'supplement', 'vitamin',
         'drug', 'medic', 'brain', 'stroke', 'alzheimer', 'diabetes', 'arthritis', 'statin',
         'ptsd', 'immune system', 'implant', 'surgery', 'parkinson', 'dementia', 'mental health',
         'climate change', 'global warming', 'covid-19', 'coronavirus', 'brexit', 'trump',
         'jackdaw', 'spy', 'missiles', 'ukraine', 'russia', 'israel', 'gaza', 'hamas',
         'captiv', 'treason', 'raid', 'hostage', 'invasion', 'military', 'council', 'policy',
         'tax', 'spending', 'budget', 'economy', 'inflation', 'recession', 'market crash',
         'stock market', 'shares', 'ipo', 'review', 'trailer', 'podcast', 'op-ed')

# Collect ALL existing release-IDs from content/**/*.md
existing_release_ids = set()
for md in glob.glob('content/**/*.md', recursive=True):
    try:
        with open(md, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                m = re.search(r'/releases/(\d+)/(\d+)/(\d+)\.htm', line)
                if m:
                    existing_release_ids.add(m.group(0))
    except Exception:
        pass

# Also collect existing slugs
existing_slugs = set()
for d in ['content/news/', 'content/blog/', 'content/explainers/']:
    if not os.path.isdir(d):
        continue
    for fn in os.listdir(d):
        if not fn.endswith('.md'):
            continue
        stem = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', fn[:-3])
        existing_slugs.add(stem.lower())

URL = 'https://www.sciencedaily.com/rss/top.xml'
req = urllib.request.Request(URL, headers={'User-Agent': UA})
with urllib.request.urlopen(req, timeout=30) as resp:
    xml = resp.read().decode('utf-8', errors='replace')

root = ET.fromstring(xml)
items = []
for item in root.iter('item'):
    title_el = item.find('title')
    link_el = item.find('link')
    date_el = item.find('pubDate')
    if title_el is None or link_el is None:
        continue
    title = (title_el.text or '').strip()
    link = (link_el.text or '').strip()
    date_str = (date_el.text or '') if date_el is not None else ''
    try:
        pubdate = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
    except ValueError:
        try:
            pubdate = datetime.strptime(date_str[:25], '%a, %d %b %Y %H:%M:%S')
            pubdate = pubdate.replace(tzinfo=timezone.utc)
        except ValueError:
            pubdate = datetime.min.replace(tzinfo=timezone.utc)

    # Extract release-ID
    m = re.search(r'/releases/(\d+)/(\d+)/(\d+)\.htm', link)
    release_id = m.group(0) if m else None

    slug = re.sub(r'[^a-zA-Z0-9]+', '-', title.lower()).strip('-')
    tl = title.lower()

    blocked = any(b in tl for b in BLOCK)
    dup_release = release_id in existing_release_ids if release_id else False
    dup_slug = slug in existing_slugs

    # Extract the 12-digit ID portion for dedup display
    rid_short = ''
    if release_id:
        rid_short = re.sub(r'/releases/', '', release_id)

    items.append({
        'title': title, 'link': link, 'date': pubdate, 'slug': slug,
        'blocked': blocked, 'dup_release': dup_release, 'dup_slug': dup_slug,
        'release_id': rid_short,
    })

items.sort(key=lambda x: x['date'], reverse=True)
print(f"Parsed {len(items)} items from ScienceDaily top.xml")
print(f"Existing release-IDs: {len(existing_release_ids)}")
print("=" * 90)

fresh = []
for i, it in enumerate(items[:40]):
    if it['blocked']:
        status = 'BLOCKED'
    elif it['dup_release']:
        status = 'DUP(rid)'
    elif it['dup_slug']:
        status = 'DUP(slug)'
    else:
        status = 'FRESH'
        fresh.append(it)
    print(f"[{i+1:2d}] {status:10s} {it['date'].strftime('%Y-%m-%d %H:%M')} | {it['title'][:75]}")
    print(f"      slug: {it['slug']}")
    if it['release_id']:
        print(f"      rid:  {it['release_id']}")
    print(f"      url:  {it['link']}")
    print()

print(f"\nTotal FRESH: {len(fresh)}")
if fresh:
    print("\n=== TOP 5 FRESH CANDIDATES ===")
    for j, it in enumerate(fresh[:5]):
        print(f"  {j+1}. {it['title']}")
        print(f"     slug: {it['slug']}")
        print(f"     url:  {it['link']}")
        print()
