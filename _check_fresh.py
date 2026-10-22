#!/usr/bin/env python3
import xml.etree.ElementTree as ET, os, glob, re

tree = ET.parse('/tmp/sd-top.xml')
root = tree.getroot()
ns = {'': 'http://base.site/rss/'}

# Collect existing SD release IDs from content
existing_ids = set()
for d in ['content/news', 'content/blog']:
    for f in glob.glob(f'{d}/*.md'):
        with open(f) as fh:
            content = fh.read()
        # find all 14-digit ids
        for m in re.findall(r'\d{8}\d{6}', content):
            existing_ids.add(m)
        # also find url references
        for m in re.findall(r'releases/(\d{14})', content):
            existing_ids.add(m)

print("=== Existing SD release IDs in content: ===")
for eid in sorted(existing_ids):
    print(eid)

# Now parse all items from the feed
print("\n=== Full ScienceDaily top feed titles + IDs: ===")
items = root.findall('.//item')
for item in items:
    title = item.findtext('title', '') or ''
    link = item.findtext('link', '') or ''
    # extract release id
    m = re.search(r'releases/(\d{14})', link)
    rel_id = m.group(1) if m else 'N/A'
    already = "ALREADY WRITTEN" if rel_id in existing_ids else "FRESH"
    print(f"[{already}] {rel_id} | {title}")
    print(f"  URL: {link}")
