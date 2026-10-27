#!/usr/bin/env python3
"""Fetch Space.com RSS directly with browser UA and scan all items for fresh candidates."""
import urllib.request, re, os

# Extract release IDs from all content
existing_slugs = set()
existing_ids = set()
for root, dirs, files in os.walk('content/'):
    for f in files:
        if f.endswith('.md'):
            filepath = os.path.join(root, f)
            content = open(filepath, 'r', errors='ignore').read()
            # Extract slug from filename
            slug = f[:-3]  # remove .md
            existing_slugs.add(slug)
            for m in re.finditer(r'/releases/(\d+)/(\d+)/(\d+)\.htm', content):
                existing_ids.add(m.group(3))

print(f'Existing slugs: {len(existing_slugs)}')
print(f'Existing release IDs: {len(existing_ids)}')

BLOCK_KW = ['cancer', 'tumor', 'covid', 'pandemic', 'death', 'killed', 'murder',
            'lawsuit', 'court', 'election', 'politic', 'bomb', 'shooting',
            'death toll', 'aspirin', 'blood pressure', 'dementia', 'alzheimer',
            'fish oil', 'ultra-processed', 'flavanol', 'flavonoid', 'ptsd',
            'arthritis', 'parkinson', 'alcohol', 'cannabis', 'gummy',
            'rheumatoid', 'implant', 'blood sugar', 'diabetes',
            'entertainment', 'donnie darko', 'star trek', 'halo', 'x-files',
            'blade runner', 'podcast', 'review', 'trailer', 'op-ed',
            'failed rescue', 'failed.*attempt']

# Fetch Space.com RSS
url = 'https://www.space.com/feeds/rss'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})
raw = urllib.request.urlopen(req, timeout=25).read().decode('utf-8', 'ignore')
items = re.findall(r'<item>(.*?)</item>', raw, re.S)
print(f'\n=== Space.com RSS: {len(items)} items ===')

for item in items:
    title_m = re.search(r'<title>(.*?)</title>', item, re.S)
    link_m = re.search(r'<link>(.*?)</link>', item, re.S)
    desc_m = re.search(r'<description>(.*?)</description>', item, re.S)
    if not title_m or not link_m:
        continue
    title = re.sub(r'<.*?>', '', title_m.group(1)).strip()
    article_url = link_m.group(1).strip()
    desc = re.sub(r'<.*?>', '', desc_m.group(1) if desc_m else '').strip()[:500]

    # Extract release ID if ScienceDaily
    rid = None
    if 'sciencedaily.com' in article_url:
        rid_m = re.search(r'/releases/(\d+)/(\d+)/(\d+)\.htm', article_url)
        rid = rid_m.group(3) if rid_m else None

    # Check if already published (slug substring match)
    # Extract slug from URL
    path_parts = re.sub(r'^https?://[^/]+', '', article_url).strip('/').split('/')
    url_slug = path_parts[-1].replace('.html', '') if path_parts else ''

    is_dup = False
    if rid and rid in existing_ids:
        is_dup = True
    # Check slug substring
    for existing in existing_slugs:
        if url_slug and (url_slug in existing or existing in url_slug):
            # Further check: is it really the same? Check title tokens
            # Extract a few significant words from title
            title_words = set(w.lower() for w in re.findall(r'\b\w{5,}\b', title))
            existing_words = set(w.lower() for w in existing.replace('-', ' ').split())
            if title_words & existing_words:
                is_dup = True
                break

    is_blocked = any(re.search(b, title.lower() + ' ' + desc.lower()) for b in BLOCK_KW)
    status = 'DUP' if is_dup else ('BLOCK' if is_blocked else 'POTENTIAL')
    if status == 'POTENTIAL':
        print(f'[{status}] {title}')
        print(f'  url: {article_url}')
        print(f'  slug: {url_slug}')
        print(f'  desc: {desc[:300]}')
        print()
