#!/usr/bin/env python3
"""Full sweep of earth_science feed + Reddit raw check."""
import subprocess, gzip, xml.etree.ElementTree as ET, re, os

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

MEDICAL_BLOCK = ("cancer", "dementia", "disease", "alcohol", "aspirin", "blood pressure",
                 "drug", "diabetes", "tumor", "tumour", "surgery", "implant", "immune system",
                 "pills", "medication", "inflammatory", "diagnosis", "died", "death", "risky",
                 "hurricane", "tsunami", "earthquake", "volcano", "storm", "wildfire", "fire")

def fetch(url):
    p = subprocess.run(["curl","-sL","--max-time","25","-A",UA,url], capture_output=True)
    data = p.stdout
    if data[:2] == b"\x1f\x8b":
        data = gzip.decompress(data)
    idx = data.rfind(b"</rss>")
    if idx > 0:
        data = data[:idx+7]
    return data

def parse(data):
    try:
        root = ET.fromstring(data)
    except ET.ParseError:
        return []
    out = []
    for it in root.iter("item"):
        t = (it.findtext("title") or "").strip()
        l = (it.findtext("link") or "").strip()
        out.append({"title": t, "link": l})
    return out

def is_medical(title):
    tl = title.lower()
    return any(b in tl for b in MEDICAL_BLOCK)

def topic_keycheck(title, existing_files):
    stopwords = {"the","and","for","with","this","that","from","have","are","was","has",
                 "his","her","their","our","your","a","an","in","on","to","of","at","by",
                 "it","is","as","be","or","not","but","if","when","what","how","why",
                 "which","who","will","may","can","new","study","scientists","research",
                 "discover","reveal","suggest","propose","find","linked","risk","disease",
                 "health","could","first","earth"}
    all_words = re.findall(r'\b[A-Za-z]+\b', title.lower())
    core = [k for k in all_words if len(k) >= 5 and k not in stopwords and not k.isdigit()]
    distinctive = core[:3] if len(core) >= 3 else core
    if not distinctive:
        return [], True
    matches = []
    for fname in existing_files:
        if not fname.endswith(".md"): continue
        path = os.path.join("content/news/", fname)
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read().lower()
            matched = sum(1 for k in distinctive if k in text)
            if matched >= 2:
                matches.append(fname)
        except: continue
    return distinctive, matches

existing_files = sorted(os.listdir("content/news/"))

# Full earth_science sweep
print("=== Earth_science FULL sweep ===")
data = fetch("https://www.sciencedaily.com/rss/earth_climate/earth_science.xml")
items = parse(data)
print(f"Total: {len(items)}")
fresh_nonmedical = []
for it in items:
    medical = is_medical(it["title"])
    distinctive, dups = topic_keycheck(it["title"], existing_files)
    if medical:
        status = "MEDICAL"
    elif dups:
        status = "DUPE"
    else:
        status = "FRESH"
        fresh_nonmedical.append(it)
    if status in ("FRESH", "MEDICAL"):
        print(f"  [{status}] {it['title'][:90]} | {it['link'][:80]}")

print(f"\nFRESH non-medical: {len(fresh_nonmedical)}")

# Check Reddit raw
print("\n=== Reddit TIL raw check ===")
p = subprocess.run(["curl","-sL","--max-time","25","-A",UA,"https://old.reddit.com/r/todayilearned/top/.rss"], capture_output=True)
print(f"  bytes: {len(p.stdout)}")
print(f"  first 500 chars: {p.stdout[:500]}")
