#!/usr/bin/env python3
"""Extract key facts: SpaceX CRS-35 launch/dock from Wikipedia ISS + SpaceX sources as 2nd source."""
import re, html, os, json
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
def load(p): return open(p,encoding="utf-8",errors="replace").read()

# Check Wikipedia ISS page for CRS-35
w=load("/tmp/owcheck/wikipedia_iss.html")
print("=== Wikipedia ISS page ===")
print("LEN:", len(w))
# search for CRS-35 mentions
idxs=[m.start() for m in re.finditer(r'CRS-35|cargo|capsule|Dragon', w[:800000], re.I)]
print("CRS-35/Dragon/Capsule/cargo mention positions (first 10):", idxs[:10])
if idxs:
    seg=w[max(0,idxs[0]-200):idxs[0]+800]
    print("SNIPPET:", html.unescape(re.sub(r'<[^>]+>',' ',seg)).strip()[:500])

# SpaceX launch page
s=load("/tmp/owcheck/spacex_crs35.html")
print("\n=== SpaceX CRS-35 launch page ===")
print("LEN:", len(s))
print("TITLE:", (re.search(r"<title>(.*?)<",s,re.S|re.I) or [None]).group(1) if re.search(r"<title>(.*?)<",s,re.S|re.I) else "?")
# look for any launch data or redirect meta
rdr=re.search(r'<meta[^>]+http-equiv="refresh"[^>]*content="[^"]*url=([^"]+)"', s, re.I)
print("REDIRECT:", rdr.group(1) if rdr else "none")

# Also fetch NASA's main ISS research recent news as structured 2nd source
import subprocess
r=subprocess.run(["curl","-s","--compressed","--max-time","25","-A",UA,
  "https://www.nasa.gov/news/298050/spacex-crs-35-resupply-mission-to-international-space-station/","-o","/tmp/owcheck/nasa_crs35.html"],
  capture_output=True, text=True)
sz=os.path.getsize("/tmp/owcheck/nasa_crs35.html") if os.path.exists("/tmp/owcheck/nasa_crs35.html") else 0
print("\nNASA news 298050 size:", sz, "exit:", r.returncode)
