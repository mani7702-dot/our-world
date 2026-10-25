#!/usr/bin/env python3
"""Trending lane fallback: fetch ScienceDaily top.xml, strip trailing junk, print candidates."""
import subprocess, xml.etree.ElementTree as ET, sys

UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
URL = "https://www.sciencedaily.com/rss/top.xml"

p = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, URL], capture_output=True)
data = p.stdout
if data[:2] == b"\x1f\x8b":
    import gzip; data = gzip.decompress(data)
raw = data.decode("utf-8", "replace")
# Strip trailing content after </rss>
idx = raw.rfind("</rss>")
if idx != -1:
    raw = raw[:idx + len("</rss>")]

try:
    root = ET.fromstring(raw)
except ET.ParseError as e:
    print(f"PARSE ERROR: {e}", file=sys.stderr)
    sys.exit(1)

BLOCK = ("war", "attack", "death toll", "killed", "murder", "court", "lawsuit", "covid",
         "pandemic", "election", "politic", "terror", "bomb", "shooting")
# Extra kid-safety: medical/scary/violence
EXTRA_BLOCK = ("cancer", "death", "dies", "killed", "murder", "suicide", "violence",
               "horror", "scary", "fear", "pandemic", "disease", "illness", "infection",
               "clinical trial", "tumor", "leukemia", "covid", "autism", "epidemic")

out = []
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    if not t or len(t) < 20:
        continue
    link = (it.findtext("link") or "").strip()
    desc = (it.findtext("description") or "").strip()[:250]
    blocked = any(b in t.lower() for b in BLOCK) or any(b in t.lower() for b in EXTRA_BLOCK)
    out.append({"title": t, "link": link, "desc": desc, "blocked": blocked})

print(f"Total candidates: {len(out)}")
print(f"Non-blocked: {sum(1 for r in out if not r['blocked'])}")
print(f"Blocked: {sum(1 for r in out if r['blocked'])}")
print()
for i, r in enumerate(out[:30]):
    tag = "BLOCKED" if r["blocked"] else "ok"
    print(f"[{tag}] #{i+1} {r['title']}")
    print(f"  url: {r['link']}")
    if r["desc"]:
        print(f"  desc: {r['desc'][:200]}")
    print()
