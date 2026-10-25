#!/usr/bin/env python3
"""Try to find truly fresh trending content from other ScienceDaily feeds and other sources."""
import urllib.request, xml.etree.ElementTree as ET, re, os

UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"

# Try a few different ScienceDaily topic feeds that might have fresh content
feeds = [
    ("ScienceDaily Animals", "https://www.sciencedaily.com/news/plants_animals/animals/rss.xml"),
    ("ScienceDaily Environment", "https://www.sciencedaily.com/news/earth_climate/rss.xml"),
    ("ScienceDaily Technology", "https://www.sciencedaily.com/news/matter_energy/rss.xml"),
    ("ScienceDaily Health", "https://www.sciencedaily.com/news/health_medicine/rss.xml"),
]

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
         "brain cancer", "lung cancer", "colorectal", "vitamin C.*cancer")

for label, url in feeds:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        raw = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
        idx = raw.rfind("</rss>")
        if idx != -1:
            raw = raw[:idx + 6]
        root = ET.fromstring(raw)
        items = list(root.iter("item"))
        print(f"\n=== {label} ({len(items)} items) ===")
        for it in items[:10]:
            t = (it.findtext("title") or "").strip()
            link = (it.findtext("link") or "").strip()
            low = t.lower()
            blocked = any(b in low for b in BLOCK)
            # Check dedup
            words = re.findall(r'\b[a-zA-Z]{4,}\b', low)
            core_words = [w for w in words if w not in ("the", "and", "that", "this", "with", "for", "scientists", "scientists'", "new", "how", "why", "what", "study", "research", "discovery")]
            match = False
            for existing in existing_files:
                matches = sum(1 for w in core_words[:6] if w in existing)
                if matches >= 3:
                    match = True
                    break
            tag = "PUBLISHED" if match else ("BLOCKED" if blocked else "FRESH")
            print(f"[{tag}] {t}")
            print(f"  url: {link}")
    except Exception as e:
        print(f"  {label}: ERR: {e}")
