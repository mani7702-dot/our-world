#!/usr/bin/env python3
"""Scan BBC Science & Environment RSS for fresh, kid-safe candidates."""
import urllib.request, re, os

# Full content tree dedup
existing_slugs = set()
existing_ids = set()
for root, dirs, files in os.walk('content/'):
    for f in files:
        if f.endswith('.md'):
            existing_slugs.add(f[:-3])
            content = open(os.path.join(root, f), 'r', errors='ignore').read()
            for m in re.finditer(r'releases/\d+/\d+/(\d+)', content):
                existing_ids.add(m.group(1))

url = 'https://feeds.bbci.co.uk/news/science_and_environment/rss.xml'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})
raw = urllib.request.urlopen(req, timeout=25).read().decode('utf-8', errors='ignore')
items = re.findall(r'<item>(.*?)</item>', raw, re.S)
print(f'Total BBC Science & Environment items: {len(items)}')
print()

BLOCK_KW = ['cancer', 'tumor', 'covid', 'pandemic', 'death', 'killed', 'murder',
            'lawsuit', 'court', 'election', 'politic', 'bomb', 'shooting',
            'death toll', 'aspirin', 'blood pressure', 'dementia', 'alzheimer',
            'war', 'attack', 'conflict', 'military', 'nuclear weapon',
            'climate crisis', 'climate emergency', 'extinction', 'doomsday']

for i, item in enumerate(items):
    title_m = re.search(r'<title>(.*?)</title>', item, re.S)
    link_m = re.search(r'<link>(.*?)</link>', item, re.S)
    desc_m = re.search(r'<description>(.*?)</description>', item, re.S)
    if not title_m or not link_m:
        continue
    title = re.sub(r'<.*?>', '', title_m.group(1)).strip()
    article_url = link_m.group(1).strip()
    desc = re.sub(r'<.*?>', '', desc_m.group(1) if desc_m else '').strip()[:400]

    # Check if link is BBC news article
    if 'bbc.co.uk/news/' not in article_url and 'bbc.com/news/' not in article_url:
        continue

    # Extract ID from URL
    id_m = re.search(r'/news/(\d+)', article_url)
    article_id = id_m.group(1) if id_m else None

    # Check dedup - extract significant title tokens
    title_tokens = set(re.findall(r'\b\w{6,}\b', title.lower()))
    is_dup = False
    for existing in existing_slugs:
        existing_tokens = set(re.findall(r'\b\w{6,}\b', existing.lower()))
        if len(title_tokens & existing_tokens) >= 3:
            is_dup = True
            break

    is_blocked = any(b in title.lower() or b in desc.lower() for b in BLOCK_KW)
    status = 'DUP' if is_dup else ('BLOCK' if is_blocked else 'POTENTIAL')

    if status != 'DUP':
        print(f'[{status}] {title}')
        print(f'  url: {article_url}')
        print(f'  id: {article_id}')
        print(f'  desc: {desc[:250]}')
        print()
