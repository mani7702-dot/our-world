#!/usr/bin/env python3
"""Scan ScienceDaily top.xml for fresh, non-medical science candidates."""
import urllib.request, re, os

# Fetch live ScienceDaily top.xml
url = 'https://www.sciencedaily.com/rss/top.xml'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})
raw = urllib.request.urlopen(req, timeout=25).read().decode('utf-8', 'ignore')
# Strip trailing HTML comments
raw = re.sub(r'<!--.*-->', '', raw, flags=re.S)

# Parse items using regex (fallback for malformed XML)
items = re.findall(r'<item>(.*?)</item>', raw, re.S)
print(f'Found {len(items)} items in top.xml')

# Extract release IDs from all content
existing_ids = set()
for root, dirs, files in os.walk('content/'):
    for f in files:
        if f.endswith('.md'):
            filepath = os.path.join(root, f)
            content = open(filepath, 'r', errors='ignore').read()
            for m in re.finditer(r'/releases/(\d+)/(\d+)/(\d+).*?\.htm', content):
                rid = m.group(3)
                existing_ids.add(rid)

print(f'Found {len(existing_ids)} existing release IDs')

# BLOCK list for medical/legal/violence
BLOCK_KW = ['cancer', 'tumor', 'covid', 'pandemic', 'death', 'killed', 'murder',
            'lawsuit', 'court', 'election', 'politic', 'bomb', 'shooting',
            'death toll', 'aspirin', 'blood pressure', 'dementia', 'alzheimer',
            'fish oil', 'ultra-processed', 'flavanol', 'flavonoid']

LIFE_KW = ['study', 'scientists', 'discovery', 'discovered', 'research', 'found',
           'how', 'why', 'what', 'new', 'earth', 'space', 'planetary', 'galaxy',
           'climate', 'ocean', 'ancient', 'dinosaur', 'fossil', 'volcan',
           'supervolcan', 'supernova', 'quantum', 'particle', 'physics', 'astronomy',
           'planet', 'mars', 'moon', 'telescope', 'satellite', 'magma', 'crystal',
           'language', 'brain', 'cavity', 'cavities', 'superconduct', 'bias']

for item in items:
    title_m = re.search(r'<title>(.*?)</title>', item, re.S)
    link_m = re.search(r'<link>(.*?)</link>', item, re.S)
    desc_m = re.search(r'<description>(.*?)</description>', item, re.S)
    if not title_m or not link_m:
        continue
    title = re.sub(r'<.*?>', '', title_m.group(1)).strip()
    article_url = link_m.group(1).strip()
    desc = re.sub(r'<.*?>', '', desc_m.group(1) if desc_m else '').strip()[:400]

    # Extract release ID
    rid_m = re.search(r'/releases/(\d+)/(\d+)/(\d+)\.htm', article_url)
    rid = rid_m.group(3) if rid_m else None
    is_dup = rid in existing_ids if rid else False
    is_blocked = any(b in title.lower() or b in desc.lower() for b in BLOCK_KW)

    status = 'DUP' if is_dup else ('BLOCK' if is_blocked else 'OK')
    print(f'[{status}] {title}')
    print(f'  url: {article_url}')
    print(f'  rid: {rid}')
    print(f'  desc: {desc[:300]}')
    print()
