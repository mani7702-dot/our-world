#!/usr/bin/env python3
"""Check for Oct 26 (today) articles in top.xml that might be truly fresh."""
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
         "opioid", "addiction", "overdose", "casualty", "fatal",
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
    # Extract date from link
    m = re.search(r'/releases/2026/(\d{2})/(\d{8})', link)
    date_str = f"2026-{m.group(1)}-{m.group(2)[6:8]}" if m else "unknown"
    
    low = t.lower()
    blocked = any(b in low for b in BLOCK)
    if blocked:
        continue
    
    # Thorough dedup
    words = re.findall(r'\b[a-zA-Z]{4,}\b', low)
    core_words = [w for w in words if w not in ("the", "and", "that", "this", "with", "for", "scientists", "new", "how", "why", "what", "study", "research", "discovery", "found", "reveal", "could")][:8]
    match = False
    for existing in existing_files:
        cnt = sum(1 for w in core_words if w in existing)
        if cnt >= 3:
            match = True
            break
    
    tag = "PUBLISHED" if match else "FRESH"
    if date_str.startswith("2026-10-26"):
        print(f"[{tag}/{date_str}] {t}")
        print(f"  url: {link}")
        print(f"  kw: {core_words[:5]}")
