#!/usr/bin/env python3
"""Scan BBC Science & Environment RSS - extract titles properly."""
import urllib.request, re, os

existing_slugs = set()
for root, dirs, files in os.walk('content/'):
    for f in files:
        if f.endswith('.md'):
            existing_slugs.add(f[:-3])

url = 'https://feeds.bbci.co.uk/news/science_and_environment/rss.xml'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})
raw = urllib.request.urlopen(req, timeout=25).read().decode('utf-8', errors='ignore')

# Use proper XML parsing
import xml.etree.ElementTree as ET
try:
    root = ET.fromstring(raw)
    for item in root.findall('.//item'):
        title = item.findtext('title', '').strip()
        link = item.findtext('link', '').strip()
        desc = item.findtext('description', '').strip()[:300]

        if not title or not link:
            continue

        # Extract significant title tokens
        title_tokens = set(re.findall(r'\b\w{6,}\b', title.lower()))
        is_dup = False
        for existing in existing_slugs:
            existing_tokens = set(re.findall(r'\b\w{6,}\b', existing.lower()))
            if len(title_tokens & existing_tokens) >= 3:
                is_dup = True
                break

        BLOCK_KW = ['cancer', 'tumor', 'covid', 'pandemic', 'death', 'killed',
                    'election', 'politic', 'bomb', 'shooting', 'war', 'attack',
                    'conflict', 'military', 'nuclear weapon', 'climate crisis',
                    'doomsday', 'PTSD', 'dementia', 'alzheimer', 'aspirin',
                    'blood pressure', 'ultra-processed', 'fish oil',
                    'cannabis', 'gummy', 'alcohol', 'drinking']

        is_blocked = any(b in title.lower() or b in desc.lower() for b in BLOCK_KW)
        status = 'DUP' if is_dup else ('BLOCK' if is_blocked else 'POTENTIAL')

        if status != 'DUP':
            print(f'[{status}] {title}')
            print(f'  url: {link}')
            print(f'  desc: {desc[:300]}')
            print()

except Exception as e:
    print(f'XML parse error: {e}')
    # Fallback to regex
    items = re.findall(r'<item>(.*?)</item>', raw, re.S)
    for item in items[:20]:
        title_m = re.search(r'<title>(.*?)</title>', item, re.S)
        if title_m:
            print(f'  Title: {title_m.group(1)}')
