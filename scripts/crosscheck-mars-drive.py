#!/usr/bin/env python3
"""Cross-check the Mars rover 'longest drive' story with NASA source + Wikipedia 2nd source."""
import subprocess, os
UA = "Mozilla/5.0 (OurWorld raw-fallback; contact andugulamani722@gmail.com)"

# NASA main feed item: we need the article URL
# The title is "Tracks Along the Longest Drive on Another World"
# Let me find the link in the NASA feed
import xml.etree.ElementTree as ET
root = ET.parse('/tmp/nasa-main-feed.xml').getroot()
for it in root.iter('item'):
    t = (it.findtext('title') or '').strip()
    if "Longest Drive" in t:
        l = (it.findtext('link') or '').strip()
        print(f"Title: {t}")
        print(f"URL: {l}")
        # Download the article
        out = "/tmp/nasa-longest-drive.html"
        r = subprocess.run(["curl", "-s", "--compressed", "--max-time", "25", "-A", UA, l, "-o", out], capture_output=True)
        sz = os.path.getsize(out) if os.path.exists(out) else 0
        print(f"Downloaded: {sz} bytes")
        # Also download Wikipedia Perseverance page
        wp_out = "/tmp/wikipedia-perseverance.html"
        r2 = subprocess.run(["curl", "-s", "--compressed", "--max-time", "25", "-A", UA, "https://en.wikipedia.org/wiki/Mars_2020_(rover)", "-o", wp_out], capture_output=True)
        sz2 = os.path.getsize(wp_out) if os.path.exists(wp_out) else 0
        print(f"Wikipedia Perseverance: {sz2} bytes")
        break
