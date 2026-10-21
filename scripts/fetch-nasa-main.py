#!/usr/bin/env python3
"""NASA main feed fallback — last escalation for fresh space/science stories."""
import subprocess, os
UA = "Mozilla/5.0 (OurWorld raw-fallback; contact andugulamani722@gmail.com)"
url = "https://www.nasa.gov/feed/"
out = "/tmp/nasa-main-feed.xml"
r = subprocess.run(["curl", "-s", "--compressed", "--max-time", "25", "-A", UA, url, "-o", out], capture_output=True)
sz = os.path.getsize(out) if os.path.exists(out) else 0
print(f"NASA main feed: {sz} bytes")
if sz > 0:
    import xml.etree.ElementTree as ET
    root = ET.parse(out).getroot()
    items = list(root.iter('item'))
    print(f"items: {len(items)}")
    for it in items[:15]:
        t = (it.findtext('title') or '').strip()
        l = (it.findtext('link') or '').strip()
        print(f"  - {t[:90]}")
        print(f"    {l[:90]}")
