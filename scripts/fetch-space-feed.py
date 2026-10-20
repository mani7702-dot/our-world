#!/usr/bin/env python3
"""Fetch ScienceDaily space RSS and list all items."""
import subprocess, xml.etree.ElementTree as ET, re

UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
url = "https://www.sciencedaily.com/rss/news/space/annotated/"
r = subprocess.run(['curl', '-s', '--compressed', '--max-time', '25', '-A', UA, url],
                   capture_output=True, text=True)
print(f"bytes: {len(r.stdout)}")
try:
    root = ET.fromstring(r.stdout)
    items = list(root.iter('item'))
    print(f"items: {len(items)}")
    for it in items[:20]:
        t = (it.findtext('title') or '').strip()
        l = (it.findtext('link') or '').strip()
        print(f'  {t[:80]} | {l[:100]}')
except Exception as e:
    # Maybe it's not valid RSS - look for URLs
    print(f"PARSE ERROR: {e}")
    urls = re.findall(r'https://www\.sciencedaily\.com/releases/[^\s"]+', r.stdout)
    print(f"Found {len(urls)} release URLs")
    for u in urls[:10]:
        print(f'  {u}')
