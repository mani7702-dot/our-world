#!/usr/bin/env python3
"""Show ALL GNN items with their dedup status - lower threshold."""
import urllib.request, re, os

UA = "Mozilla/5.0 (OurWorld picker; contact anddugalmani722@gmail.com)"
URL = "https://www.goodnewsnetwork.org/feed/"

existing_files = []
for f in os.listdir("/home/ubuntu/our-world/content/news"):
    if f.endswith(".md"):
        path = os.path.join("/home/ubuntu/our-world/content/news", f)
        with open(path) as fh:
            existing_files.append(fh.read().lower())

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
print(f"=== GNN ({len(items)} items) ===")
for it in items:
    t = (it.findtext("title") or "").strip()
    link = (it.findtext("link") or "").strip()
    low = t.lower()
    blocked = any(b in low for b in BLOCK)
    
    words = re.findall(r'\b[a-zA-Z]{4,}\b', low)
    core_words = [w for w in words if w not in ("the", "and", "that", "this", "with", "for", "scientists", "new", "how", "why", "what", "study", "research", "discovery", "found", "reveal", "could", "your", "from", "in", "a", "of", "to", "is", "are")][:10]
    
    # Check each existing file for keyword matches, print the match count
    best_match = 0
    best_file = ""
    for f_name, existing in zip(os.listdir("/home/ubuntu/our-world/content/news"), existing_files):
        cnt = sum(1 for w in core_words if w in existing)
        if cnt > best_match:
            best_match = cnt
            best_file = f_name
    
    tag = "BLOCKED" if blocked else (f"PUBLISHED({best_match}kw)" if best_match >= 3 else f"FRESH({best_match}kw)")
    print(f"[{tag} {best_file[:30]}] {t}")
    print(f"  url: {link}")
