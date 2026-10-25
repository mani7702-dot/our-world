#!/usr/bin/env python3
"""Try additional trending sources: NPR, Reddit, other feeds."""
import urllib.request, re, os

UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"

BLOCK = ("cancer", "alzheimer", "diabetes", "ptsd", "parkinson", "surgery",
         "covid", "death", "killed", "murder", "bomb", "shooting", "war",
         "attack", "tumor", "disease", "stroke", "heart attack", "risk",
         "depression", "anxiety", "autism", "inflammation", "arthritis",
         "opioid", "addiction", "overdose", "casualty", "fatal",
         "brain cancer", "lung cancer", "colorectal")

existing_files = []
for f in os.listdir("/home/ubuntu/our-world/content/news"):
    if f.endswith(".md"):
        path = os.path.join("/home/ubuntu/our-world/content/news", f)
        with open(path) as fh:
            existing_files.append(fh.read().lower())

# Try other RSS feeds that might have trending science
other_feeds = [
    ("ScienceDaily Plants & Animals", "https://www.sciencedaily.com/rss/plants_animals.xml"),
    ("ScienceDaily Matter & Energy", "https://www.sciencedaily.com/rss/matter_energy.xml"),
    ("ScienceDaily Space & Time", "https://www.sciencedaily.com/rss/space_time.xml"),
    ("ScienceDaily Computers & Math", "https://www.sciencedaily.com/rss/computers_math.xml"),
    ("ScienceDaily Environment", "https://www.sciencedaily.com/rss/environment.xml"),
]

for label, url in other_feeds:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        raw = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")
        idx = raw.rfind("</rss>")
        if idx != -1:
            raw = raw[:idx + 6]
        import xml.etree.ElementTree as ET
        root = ET.fromstring(raw)
        items = list(root.iter("item"))
        print(f"\n=== {label} ({len(items)} items) ===")
        for it in items[:8]:
            t = (it.findtext("title") or "").strip()
            link = (it.findtext("link") or "").strip()
            low = t.lower()
            blocked = any(b in low for b in BLOCK)
            words = re.findall(r'\b[a-zA-Z]{4,}\b', low)
            core_words = [w for w in words if w not in ("the", "and", "that", "this", "with", "for", "scientists", "new", "how", "why", "what", "study", "research", "discovery", "found", "reveal", "could")][:8]
            match = False
            for existing in existing_files:
                cnt = sum(1 for w in core_words if w in existing)
                if cnt >= 3:
                    match = True
                    break
            tag = "PUBLISHED" if match else ("BLOCKED" if blocked else "FRESH")
            if tag != "PUBLISHED":
                print(f"[{tag}] {t}")
                print(f"  url: {link}")
    except Exception as e:
        print(f"  {label}: ERR: {e}")
