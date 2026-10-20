"""Fallback: download a feed file with curl --compressed then parse with ElementTree.
Usage: python3 scripts/rss-raw-fallback.py <url> <outfile.xml>
"""
import sys, subprocess, urllib.parse
url = sys.argv[1]
out = sys.argv[2]
subprocess.run(["curl", "-s", "--compressed", "--max-time", "35", "-A",
                "Mozilla/5.0 (OurWorldSite/1.0; contact: andugulamani722@gmail.com)",
                url, "-o", out], check=False, timeout=40)
print("saved", out, "bytes=", __import__("os").path.getsize(out))
