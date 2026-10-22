#!/usr/bin/env python3
import xml.etree.ElementTree as ET, os, glob, re

tree = ET.parse('/tmp/sd-top.xml')
root = tree.getroot()

# Collect existing content — grep for stable tokens across ALL articles
existing_titles = set()
existing_slugs = set()
existing_ids = set()
for d in ['content/news', 'content/blog']:
    for f in glob.glob(f'{d}/*.md'):
        slug = os.path.splitext(os.path.basename(f))[0]
        existing_slugs.add(slug)
        with open(f) as fh:
            content = fh.read()
        # find sd release ids (12-digit format YYMMDDHHMMSS)
        for m in re.findall(r'/releases/\d{4}/\d{2}/(\d{12})', content):
            existing_ids.add(m)
        # extract title
        for line in content.split('\n')[:3]:
            if line.startswith('title:'):
                t = line.split(':',1)[1].strip()
                existing_titles.add(t)
                break

print(f"Existing slugs count: {len(existing_slugs)}")
print(f"Existing SD IDs count: {len(existing_ids)}")
for eid in sorted(existing_ids):
    print(f"  Existing ID: {eid}")

# Now parse all items from the feed
print("\n=== Full ScienceDaily top feed — checking freshness: ===")
items = root.findall('.//item')
for item in items:
    title = item.findtext('title', '') or ''
    link = item.findtext('link', '') or ''
    m = re.search(r'/releases/\d{4}/\d{2}/(\d{12})\.htm', link)
    rel_id = m.group(1) if m else 'N/A'
    already = "ALREADY WRITTEN" if rel_id in existing_ids else "FRESH"
    print(f"[{already}] {rel_id} | {title}")
