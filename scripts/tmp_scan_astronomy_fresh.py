#!/usr/bin/env python3
"""Scan ScienceDaily astronomy feeds for fresh, non-medical science candidates."""
import urllib.request, re, os

ASTRONOMY_FEEDS = [
    'https://www.sciencedaily.com/rss/space_time/astronomy.xml',
    'https://www.sciencedaily.com/rss/space_time/solar_system.xml',
]

# Extract release IDs from all content
existing_ids = set()
for root, dirs, files in os.walk('content/'):
    for f in files:
        if f.endswith('.md'):
            filepath = os.path.join(root, f)
            content = open(filepath, 'r', errors='ignore').read()
            for m in re.finditer(r'/releases/(\d+)/(\d+)/(\d+)\.htm', content):
                existing_ids.add(m.group(3))
print(f'Existing release IDs: {len(existing_ids)}')

BLOCK_KW = ['cancer', 'tumor', 'covid', 'pandemic', 'death', 'killed', 'murder',
            'lawsuit', 'court', 'election', 'politic', 'bomb', 'shooting',
            'death toll', 'aspirin', 'blood pressure', 'dementia', 'alzheimer',
            'fish oil', 'ultra-processed', 'flavanol', 'flavonoid', 'ptsd',
            'arthritis', 'parkinson', 'alcohol', 'cannabis', 'gummy',
            'rheumatoid', 'implant', 'blood sugar', 'diabetes']

for feed_url in ASTRONOMY_FEEDS:
    print(f'\n=== {feed_url} ===')
    req = urllib.request.Request(feed_url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    raw = urllib.request.urlopen(req, timeout=25).read().decode('utf-8', 'ignore')
    raw = re.sub(r'<!--.*-->', '', raw, flags=re.S)
    items = re.findall(r'<item>(.*?)</item>', raw, re.S)
    print(f'Found {len(items)} items')

    for item in items[:20]:
        title_m = re.search(r'<title>(.*?)</title>', item, re.S)
        link_m = re.search(r'<link>(.*?)</link>', item, re.S)
        desc_m = re.search(r'<description>(.*?)</description>', item, re.S)
        if not title_m or not link_m:
            continue
        title = re.sub(r'<.*?>', '', title_m.group(1)).strip()
        article_url = link_m.group(1).strip()
        desc = re.sub(r'<.*?>', '', desc_m.group(1) if desc_m else '').strip()[:400]
        rid_m = re.search(r'/releases/(\d+)/(\d+)/(\d+)\.htm', article_url)
        rid = rid_m.group(3) if rid_m else None
        is_dup = rid in existing_ids if rid else False
        is_blocked = any(b in title.lower() or b in desc.lower() for b in BLOCK_KW)
        status = 'DUP' if is_dup else ('BLOCK' if is_blocked else 'OK')
        if status != 'DUP':
            print(f'[{status}] {title}')
            print(f'  url: {article_url}')
            print(f'  rid: {rid}')
            print(f'  desc: {desc[:300]}')
            print()
