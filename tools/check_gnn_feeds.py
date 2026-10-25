#!/usr/bin/env python3
"""Try Good News Network and other kid-safe trending sources."""
import urllib.request, re, os

UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"

existing_files = []
for f in os.listdir("/home/ubuntu/our-world/content/news"):
    if f.endswith(".md"):
        path = os.path.join("/home/ubuntu/our-world/content/news", f)
        with open(path) as fh:
            existing_files.append(fh.read().lower())

BLOCK = ("cancer", "alzheimer", "diabetes", "ptsd", "parkinson", "surgery",
         "covid", "death", "killed", "murder", "bomb", "shooting", "war",
         "attack", "tumor", "disease", "stroke", "heart attack", "risk")

# Try GNN feed
url = "https://www.goodnewsnetwork.org/feed/"
try:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    import xml.etree.ElementTree as ET
    raw = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
    idx = raw.rfind("</rss>")
    if idx != -1:
        raw = raw[:idx + 6]
    root = ET.fromstring(raw)
    items = list(root.iter("item"))
    print(f"=== Good News Network ({len(items)} items) ===")
    for it in items[:15]:
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
        print(f"[{tag}] {t}")
        print(f"  url: {link}")
except Exception as e:
    print(f"GNN ERR: {e}")

# Also try Mental Floss and Listverse for trending/science topics
for label, url in [
    ("Mental Floss", "https://mentalfloss.com/feeds/latest"),
    ("Listverse", "https://listverse.com/feed/"),
]:
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
        for it in items[:10]:
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
            print(f"[{tag}] {t}")
            print(f"  url: {link}")
    except Exception as e:
        print(f"  {label}: ERR: {e}")
