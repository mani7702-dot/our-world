#!/usr/bin/env python3
"""Dedup check for ScienceDaily top.xml against existing Our World content."""
import os, re, xml.etree.ElementTree as ET

# Parse the cached feed
tree = ET.parse("/tmp/sd_top_check.xml")
root = tree.getroot()

# Collect already-cited ScienceDaily release IDs from content
already_ids = set()
content_dirs = ["content/news", "content/blog"]
all_text = []

for cdir in content_dirs:
    if not os.path.isdir(cdir):
        continue
    for fn in os.listdir(cdir):
        if not fn.endswith(".md"):
            continue
        filepath = os.path.join(cdir, fn)
        txt = open(filepath, encoding="utf-8", errors="ignore").read()
        all_text.append(txt[:2000])  # first 2000 chars enough for dedup
        for m in re.findall(r"sciencedaily\.com/releases/(\d{14})\.htm", txt):
            already_ids.add(m)

BLOCK = ("war", "attack", "death", "killed", "murder", "court", "lawsuit", "covid",
         "pandemic", "election", "politic", "terror", "bomb", "shooting", "deadly",
         "crash", "fatal", "suicide", "arthritis", "alzheim", "cancer", "statin",
         "brain damage", "alzheimer", "hurricane", "tsunami", "volcano")

print("=== ALREADY PUBLISHED SD IDs ===")
for sd_id in sorted(already_ids):
    print(f"  {sd_id}")

print(f"\n=== FEED CANDIDATES ({len(list(root.iter('item')))} items) ===")

for it in root.iter("item"):
    title = (it.findtext("title") or "").strip()
    link = (it.findtext("link") or "").strip()
    m = re.search(r"sciencedaily\.com/releases/(\d{14})\.htm", link)
    sd_id = m.group(1) if m else ""
    tt = title.lower()
    blocked = any(b in tt for b in BLOCK)
    fresh = True
    if sd_id and sd_id in already_ids:
        fresh = False

    # Also check topic overlap with existing content
    # Extract key 3-word n-grams from title
    words = re.findall(r'\w+', title.lower())
    topic_match = False
    for existing_text in all_text:
        existing_text_lower = existing_text.lower()
        # Check if 2+ meaningful words from title appear in existing content
        meaningful_words = [w for w in words if len(w) > 3 and w not in ("scientists", "discover", "scientists'", "the", "and", "for", "with", "have", "just", "new")]
        match_count = sum(1 for w in meaningful_words if w in existing_text_lower)
        if len(meaningful_words) > 0 and match_count >= len(meaningful_words) * 0.6:
            topic_match = True
            break

    status = "FRESH" if fresh else "DUP(by-id)"
    ks = "UNSAFE" if blocked else "KID-SAFE"
    tm = "TOPIC-OVERLAP" if topic_match else ""

    print(f"\n[{status}/{ks}] {title}")
    print(f"  url: {link}")
    print(f"  id:  {sd_id or '(none)'}")
    if tm:
        print(f"  ** {tm} - may already be covered")
