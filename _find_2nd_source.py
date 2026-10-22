#!/usr/bin/env python3
"""Search for 2nd source on the Plant Armor strawberry story."""
import subprocess, os

UA = "Mozilla/5.0 (OurWorldSite/1.0; contact: andugulamani722@gmail.com)"

# Try to find NC State research on Plant Armor strawberry
urls = [
    "https://www.google.com/search?q=%22plant+armor%22+strawberry+fabric+nc+state+yield",
    "https://news.ncsu.edu/?s=plant+armor+strawberry",
]

for url in urls:
    path = f"/tmp/search_{url.split('//')[-1].split('.')[0]}_{hash(url) % 10000}.html"
    r = subprocess.run(["curl", "-s", "--compressed", "--max-time", "25", "-A", UA, url, "-o", path], capture_output=True)
    size = os.path.getsize(path)
    print(f"URL: {url}")
    print(f"Downloaded: {size} bytes")
    print()
