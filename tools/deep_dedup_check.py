#!/usr/bin/env python3
"""Deep check: find ScienceDaily top.xml articles that are NOT published.
Use thorough topic-level dedup with partial keyword matching."""
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

print(f"Total items in feed: {len(items)}")
fresh_count = 0
for it in items:
    t = (it.findtext("title") or "").strip()
    link = (it.findtext("link") or "").strip()
    low = t.lower()
    blocked = any(b in low for b in BLOCK)
    if blocked:
        continue
    
    # Thorough topic-level dedup: extract 3-4 core words, check if ANY existing article has 3+ matches
    words = re.findall(r'\b[a-zA-Z]{4,}\b', low)
    core_words = [w for w in words if w not in ("the", "and", "that", "this", "with", "for", "scientists", "scientists'", "new", "how", "why", "what", "study", "research", "discovery", "could", "found", "reveal", "scientists'")][:8]
    
    match = False
    match_count = 0
    for existing in existing_files:
        matches = sum(1 for w in core_words if w in existing)
        if matches >= 3:
            match = True
            match_count = matches
            break
    
    tag = "PUBLISHED" if match else "FRESH"
    if tag == "FRESH":
        fresh_count += 1
        print(f"[{tag}] {t} (kw: {core_words[:5]})")
        print(f"  url: {link}")
        print(f"  match_count: {match_count}")

print(f"\nTotal FRESH candidates: {fresh_count}")
