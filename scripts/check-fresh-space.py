#!/usr/bin/env python3
"""List all FRESH ScienceDaily candidates (by SD release ID) that are NOT already published.
Only show ones that mention astronomy/space keywords."""
import re, glob

published = set()
for f in glob.glob('content/news/*.md') + glob.glob('content/blog/*.md'):
    txt = open(f).read()
    published.update(re.findall(r'2610(\d{8})', txt))

space_kw = re.compile(r'astronom|telescope|galaxy|nebula|star|planet|mars|moon|rocket|satellite|cosmic|space|asteroid|comet|meteor|black hole|webb|jwst|chandra|hubble|roman|phobos|deimos|jupiter|saturn|venus|mercury|neptune|uranus|orion|orionid|cassiopeia|constellation', re.I)

for line in open('/tmp/raw-candidates.tsv'):
    parts = line.rstrip('\n').split('\t')
    if len(parts) < 3:
        continue
    title, link, desc = parts[0], parts[1], parts[2]
    m = re.search(r'2610(\d{8})\.htm', link)
    sdid = m.group(1) if m else 'BBC'
    if sdid in published:
        continue  # already published
    combined = title + ' ' + desc[:200]
    if space_kw.search(combined):
        print(f"FRESH SD:{sdid} | {title}")
        print(f"  URL: {link}")
        print(f"  DESC: {desc[:200]}")
        print()
