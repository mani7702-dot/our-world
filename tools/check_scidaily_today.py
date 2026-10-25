#!/usr/bin/env python3
"""Fetch ScienceDaily top.xml and find articles from today's date (Oct 26, 2026) that may be fresh."""
import urllib.request, xml.etree.ElementTree as ET, re, os

UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
URL = "https://www.sciencedaily.com/rss/top.xml"

existing_files = []
for f in os.listdir("/home/ubuntu/our-world/content/news"):
    if f.endswith(".md"):
        path = os.path.join("/home/ubuntu/our-world/content/news", f)
        with open(path) as fh:
            existing_files.append(fh.read().lower())

BLOCK = ("cancer", "alzheimer", "diabetes", "ptsd", "parkinson", "surgery",
         "covid", "death", "killed", "murder", "bomb", "shooting", "war",
         "attack", "tumor", "disease", "stroke", "heart attack", "risk",
         "depression", "anxiety", "autism", "inflammation", "arthritis",
         "opioid", "addiction", "obese", "overdose", "casualty", "fatal",
         "brain cancer", "lung cancer", "colorectal")

req = urllib.request.Request(URL, headers={"User-Agent": UA})
raw = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
idx = raw.rfind("</rss>")
if idx != -1:
    raw = raw[:idx + 6]
root = ET.fromstring(raw)
items = list(root.iter("item"))

for it in items:
    t = (it.findtext("title") or "").strip()
    link = (it.findtext("link") or "").strip()
    low = t.lower()
    blocked = any(b in low for b in BLOCK)
    # Check dedup - just slug/title keywords
    slug = re.sub(r'[^a-z0-9]+', '-', low)[:50]
    match = False
    for existing in existing_files:
        if slug in existing or t.lower()[:30] in existing:
            match = True
            break
    print(f"[{'BLOCKED' if blocked else ('PUBLISHED' if match else 'FRESH')}] {t}")
