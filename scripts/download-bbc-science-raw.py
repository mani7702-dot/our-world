#!/usr/bin/env python3
"""BBC Science & Environment raw RSS fallback — sibling feed for fresh science stories."""
import subprocess, os
UA = "Mozilla/5.0 (OurWorld raw-fallback; contact andugulamani722@gmail.com)"
url = "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml"
out = "/tmp/bbc-science-raw.xml"
r = subprocess.run(["curl", "-s", "--compressed", "--max-time", "25", "-A", UA, url, "-o", out], capture_output=True)
print(f"downloaded: {os.path.getsize(out)} bytes")
