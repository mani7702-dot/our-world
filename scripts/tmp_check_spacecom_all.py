#!/usr/bin/env python3
"""Check ALL Space.com RSS candidates for duplicates using full content tree dedup."""
import urllib.request, re, os

# Full content tree dedup
existing_slugs = set()
existing_ids = set()
for root, dirs, files in os.walk('content/'):
    for f in files:
        if f.endswith('.md'):
            existing_slugs.add(f[:-3])
            content = open(os.path.join(root, f), 'r', errors='ignore').read()
            for m in re.finditer(r'release_id.*?(\d{12})', content):
                existing_ids.add(m.group(1))
            for m in re.finditer(r'/releases/(\d+)/(\d+)/(\d+)\.htm', content):
                existing_ids.add(m.group(3))

# Fetch Space.com RSS
url = 'https://www.space.com/feeds/rss'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})
raw = urllib.request.urlopen(req, timeout=25).read().decode('utf-8', 'ignore')
items = re.findall(r'<item>(.*?)</item>', raw, re.S)

ENTERTAINMENT_KW = ['entertainment', 'donnie', 'star trek', 'halo', 'x-files',
                    'blade runner', 'podcast', 'review', 'trailer', 'op-ed',
                    'coloring book', 'cult classic', 'movie', 'show', 'tv ',
                    'costume', 'halloween outfit', 'book']

print(f'Total items: {len(items)}')
print()

for i, item in enumerate(items):
    title_m = re.search(r'<title>(.*?)</title>', item, re.S)
    link_m = re.search(r'<link>(.*?)</link>', item, re.S)
    if not title_m or not link_m:
        continue
    title = re.sub(r'<.*?>', '', title_m.group(1)).strip()
    article_url = link_m.group(1).strip()
    slug = re.sub(r'https?://[^/]+/', '', article_url).replace('.html', '').strip('/')
    
    # Check if slug or close match exists
    is_dup = False
    for existing in existing_slugs:
        # Check if slugs share significant tokens
        slug_tokens = set(re.findall(r'\b\w{5,}\b', slug))
        existing_tokens = set(re.findall(r'\b\w{5,}\b', existing))
        if len(slug_tokens & existing_tokens) >= 3:
            is_dup = True
            break
    
    is_entertainment = any(kw in title.lower() or '/entertainment/' in article_url for kw in ENTERTAINMENT_KW)
    
    status = 'DUP' if is_dup else ('ENT' if is_entertainment else 'CHECK')
    print(f'[{i+1:2d}] [{status}] {title[:80]}')
    print(f'     url: {article_url}')
    print(f'     slug: {slug}')
    print()
