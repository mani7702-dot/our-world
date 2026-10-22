#!/usr/bin/env python3
import xml.etree.ElementTree as ET, os, glob, re

# Collect existing content stable tokens
existing_tokens = set()
for d in ['content/news', 'content/blog']:
    for f in glob.glob(f'{d}/*.md'):
        slug = os.path.splitext(os.path.basename(f))[0]
        existing_tokens.add(slug)
        with open(f) as fh:
            content = fh.read()
        for line in content.split('\n')[:8]:
            if line.startswith('title:'):
                t = line.split(':',1)[1].strip().lower()
                existing_tokens.add(t)
        # also check for-grownups and excerpt for keywords
        for kw in ['freud', 'doomsday', 'blueberry', 'statin', 'alzheimer', 'retina', 'brain organoid', 'crayfish', 'nightjar', 'microscope living', 'uranium cube', 'arctic sea ice', 'celestial chaos', 'roman telescope', 'amazon fire', 'jellyfish launch', 'black hole collide', 'fatty liver', 'youth protein', 'deep sleep muscle', 'red meat sugar', 'sugar diabetes', 'depression', 'covid taste', 'arthritis', 'alzheimer', 'alzheimers']:
            if kw in content.lower():
                existing_tokens.add(kw)

# Fetch BBC Science feed
import subprocess
result = subprocess.run(['curl', '-s', '--compressed', '--max-time', '25', '-A', 'Mozilla/5.0',
    'https://feeds.bbci.co.uk/news/science_and_environment/rss.xml'], capture_output=True, text=True)
with open('/tmp/bbc-science.xml', 'w') as f:
    f.write(result.stdout)
print(f"BBC Science bytes: {len(result.stdout)}")

tree = ET.parse('/tmp/bbc-science.xml')
root = tree.getroot()
items = root.findall('.//item')
print(f"BBC Science items: {len(items)}")

# Medical/block keywords
medical = ['cancer', 'alzheimer', 'depression', 'covid', 'statin', 'arthritis', 'diabetes', 'brain damage', 'mental', 'liver', 'treat', 'therapy', 'diagnos', 'disease']
political = ['northern ireland', 'climate change', 'politic', 'election', 'brexit', 'government']
violent = ['killed', 'death toll', 'massacre', 'war ', 'battle', 'attack']

for item in items:
    title = item.findtext('title', '') or ''
    link = item.findtext('link', '') or ''
    desc = item.findtext('description', '') or ''
    full = (title + ' ' + desc[:200]).lower()
    
    # Check guardrails
    is_med = any(k in full for k in medical)
    is_pol = any(k in full for k in political)
    is_violent = any(k in full for k in violent)
    
    # Check if already written (simple token check)
    already = "??" if not is_med and not is_pol and not is_violent else "BLOCKED"
    
    print(f"[{already}] {'MED' if is_med else ''}{'POL' if is_pol else ''}{'VIO' if is_violent else ''} | {title[:80]}")
    print(f"  URL: {link}")
