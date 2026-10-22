#!/usr/bin/env python3
"""Fetch full BBC World RSS feed and list all items for kid-safe filtering."""
import subprocess, xml.etree.ElementTree as ET, gzip

UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
url = "https://feeds.bbci.co.uk/news/world/rss.xml"

p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
data = p.stdout
if data[:2] == b"\x1f\x8b":
    data = gzip.decompress(data)
root = ET.fromstring(data)

BLOCK = ("war", "attack", "death toll", "killed", "murder", "court", "lawsuit", "covid",
         "pandemic", "election", "politic", "terror", "bomb", "shooting", "captiv", "treason",
         "curbs", "raid", "chaotic", "blunder")

out = []
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    l = (it.findtext("link") or "").strip()
    d = (it.findtext("description") or "").strip()[:200]
    blocked = any(b in t.lower() for b in BLOCK)
    out.append({"title": t, "link": l, "desc": d, "blocked": blocked})
    print(f"[{'BLOCKED' if blocked else 'ok'}] {t}")
    print(f"  url: {l}")
    if d:
        print(f"  desc: {d}")
    print("---")

print(f"\nTOTAL: {len(out)}")
print(f"NOT BLOCKED: {len([r for r in out if not r['blocked']])}")
