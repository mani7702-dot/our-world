#!/usr/bin/env python3
# Tirith-safe raw world-feed inspector: download BBC World RSS to a file, parse ALL items.
import subprocess, sys, xml.etree.ElementTree as ET
UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
URL = "https://feeds.bbci.co.uk/news/world/rss.xml"
OUT = "/tmp/bbc_world_raw.xml"
p = subprocess.run(["curl","-s","--compressed","--max-time","25","-A",UA,URL,"-o",OUT],
                   capture_output=True, text=True)
print("curl exit:", p.returncode, "size:", len(p.stdout), "err:", p.stderr[:200])
tree = ET.parse(OUT)
root = tree.getroot()
BLOCK = ("war","attack","death toll","killed","murder","court","lawsuit","covid","pandemic","election","politic","terror","bomb","shooting")
print("\n=== ALL raw BBC World titles (in feed order) ===")
n=0
for it in root.iter("item"):
    t=(it.findtext("title") or "").strip()
    n+=1
    blocked = any(b in t.lower() for b in BLOCK)
    flag = "BLOCKED" if blocked else "ok"
    print(f"[{n:02d} {flag}] {t}")
print(f"\nTotal items in feed: {n}")
