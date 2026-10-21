#!/usr/bin/env python3
"""Fetch 2nd source: Wikipedia on brown dwarfs + SIMP 0136 concept check."""
import subprocess, os
UA = "Mozilla/5.0 (OurWorld; contact andugulamani722@gmail.com)"
# Wikipedia: brown dwarf article (concept-level 2nd source for SIMP 0136)
url = "https://en.wikipedia.org/wiki/Brown_dwarf"
out = "/tmp/wikipedia-brown-dwarf.html"
r = subprocess.run(["curl", "-s", "--compressed", "--max-time", "25", "-A", UA, url, "-o", out], capture_output=True)
print(f"wikipedia downloaded: {os.path.getsize(out)} bytes")
