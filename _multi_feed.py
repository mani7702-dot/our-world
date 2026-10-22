#!/usr/bin/env python3
import subprocess, xml.etree.ElementTree as ET, os, glob, re

# Try multiple raw feed sources
feeds = {
    'smithsonian': 'https://www.smithsonianmag.com/feed/',
    'nasa_main': 'https://www.nasa.gov/feed/',
    'bbc_science': 'https://feeds.bbci.co.uk/news/science_and_environment/rss.xml',
}

# Existing topics (stable tokens from slugs)
existing_slugs = set()
for d in ['content/news', 'content/blog']:
    for f in glob.glob(f'{d}/*.md'):
        existing_slugs.add(os.path.splitext(os.path.basename(f))[0])

for name, url in feeds.items():
    result = subprocess.run(['curl', '-s', '--compressed', '--max-time', '20', '-A', 'Mozilla/5.0', url],
                          capture_output=True, text=True)
    if len(result.stdout) < 100:
        print(f"\n=== {name}: EMPTY/DEAD ({len(result.stdout)} bytes) ===")
        continue
    
    try:
        with open(f'/tmp/{name}.xml', 'w') as f:
            f.write(result.stdout)
        tree = ET.parse(f'/tmp/{name}.xml')
        root = tree.getroot()
        items = root.findall('.//item')
        print(f"\n=== {name}: {len(items)} items ({len(result.stdout)} bytes) ===")
        for item in items[:15]:
            title = item.findtext('title', '') or ''
            link = item.findtext('link', '') or ''
            print(f"  | {title[:80]}")
            print(f"    URL: {link[:100]}")
    except Exception as e:
        print(f"\n=== {name}: PARSE ERROR: {e} ===")
        print(result.stdout[:200])
