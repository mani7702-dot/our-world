#!/usr/bin/env python3
"""Check which trending candidates from top.xml are NOT already published."""
import urllib.request, xml.etree.ElementTree as ET, re, os

UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
URL = "https://www.sciencedaily.com/rss/top.xml"

BLOCK = ("cancer", "alzheimer", "diabetes", "ptsd", "parkinson", "surgery",
         "covid", "death", "killed", "murder", "bomb", "shooting", "war",
         "attack", "tumor", "disease", "stroke", "heart attack", "risk",
         "depression", "anxiety", "autism", "inflammation", "arthritis",
         "opioid", "addiction", "obese", "overdose", "casualty", "fatal",
         "alzheimer", "lung cancer", "colorectal", "vitamin C.*cancer")

# Get all existing article content
existing_files = []
for f in os.listdir("/home/ubuntu/our-world/content/news"):
    if f.endswith(".md"):
        path = os.path.join("/home/ubuntu/our-world/content/news", f)
        with open(path) as fh:
            existing_files.append(fh.read().lower())

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
    if blocked:
        continue
    # Extract 3-4 core keywords for topic dedup
    words = re.findall(r'\b[a-zA-Z]{4,}\b', low)
    core_words = [w for w in words if w not in ("the", "and", "that", "this", "with", "for", "scientists", "scientists'", "new", "how", "why", "what")]
    # Check if topic keywords match existing articles
    match = False
    for existing in existing_files:
        # Check for 3+ core word matches
        matches = sum(1 for w in core_words[:6] if w in existing)
        if matches >= 3:
            match = True
            break
    tag = "PUBLISHED" if match else "FRESH"
    print(f"[{tag}] {t}")
    print(f"  url: {link}")
    if tag == "FRESH":
        print(f"  keywords: {core_words[:6]}")
