#!/usr/bin/env python3
"""Deep check GNN feed with more detailed dedup - check each title individually."""
import urllib.request, re, os

UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
URL = "https://www.goodnewsnetwork.org/feed/"

existing_files = []
existing_slugs = []
for f in os.listdir("/home/ubuntu/our-world/content/news"):
    if f.endswith(".md"):
        path = os.path.join("/home/ubuntu/our-world/content/news", f)
        with open(path) as fh:
            existing_files.append(fh.read().lower())
        existing_slugs.append(f)

BLOCK = ("cancer", "alzheimer", "diabetes", "ptsd", "parkinson", "surgery",
         "covid", "death", "killed", "murder", "bomb", "shooting", "war",
         "attack", "tumor", "disease", "stroke", "heart attack", "risk")

req = urllib.request.Request(URL, headers={"User-Agent": UA})
import xml.etree.ElementTree as ET
raw = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
idx = raw.rfind("</rss>")
if idx != -1:
    raw = raw[:idx + 6]
root = ET.fromstring(raw)
items = list(root.iter("item"))
print(f"=== GNN ({len(items)} items) - detailed dedup ===")
for it in items:
    t = (it.findtext("title") or "").strip()
    link = (it.findtext("link") or "").strip()
    low = t.lower()
    blocked = any(b in low for b in BLOCK)
    
    # Check title match in existing articles
    title_match = any(t.lower()[:30] in existing for existing in existing_files)
    
    # Check key topic words
    words = re.findall(r'\b[a-zA-Z]{4,}\b', low)
    core_words = [w for w in words if w not in ("the", "and", "that", "this", "with", "for", "scientists", "new", "how", "why", "what", "study", "research", "discovery", "found", "reveal", "could", "your", "from", "in", "a", "of", "to", "is", "are")][:10]
    
    # Check each existing file for 3+ keyword matches
    match = False
    for existing in existing_files:
        cnt = sum(1 for w in core_words if w in existing)
        if cnt >= 3:
            match = True
            break
    
    tag = "PUBLISHED" if match or title_match else ("BLOCKED" if blocked else "FRESH")
    if tag == "FRESH":
        print(f"[{tag}] {t}")
        print(f"  url: {link}")
        print(f"  core: {core_words[:8]}")
    elif tag == "BLOCKED":
        print(f"[{tag}] {t}")
        print(f"  url: {link}")
