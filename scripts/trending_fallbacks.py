#!/usr/bin/env python3
"""Check additional trending fallback sources and verify medical blocklist."""
import subprocess, gzip, xml.etree.ElementTree as ET, re, os

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

MEDICAL_BLOCK = ("cancer", "dementia", "disease", "alcohol", "aspirin", "blood pressure",
                 "drug", "diabetes", "tumor", "tumour", "surgery", "implant", "immune system",
                 "pills", "medication", "inflammatory", "diagnosis", "died", "death", "risky")

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

def topic_keycheck(title, existing_files, stopwords=None):
    if stopwords is None:
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
        if not fname.endswith(".md"):
            continue
        path = os.path.join("content/news/", fname)
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read().lower()
            matched = sum(1 for k in distinctive if k in text)
            if matched >= 2:
                matches.append(fname)
        except:
            continue
    return distinctive, matches

existing_files = sorted(os.listdir("content/news/"))

# Try earth_science feed
print("=== ScienceDaily earth_science.xml ===")
data = fetch("https://www.sciencedaily.com/rss/earth_climate/earth_science.xml")
print(f"  bytes: {len(data)}")
items = parse(data)
print(f"  items: {len(items)}")
for it in items[:25]:
    medical = is_medical(it["title"])
    distinctive, dups = topic_keycheck(it["title"], existing_files)
    if medical:
        status = "MEDICAL"
    elif dups:
        status = "DUPE"
    else:
        status = "FRESH"
    print(f"  [{status}] {it['title'][:80]} | {it['link'][:90]}")
    if status == "FRESH":
        print(f"    KEYWORDS: {distinctive}")

# Try Reddit TIL (likely blocked)
print("\n=== Reddit TIL RSS ===")
data = fetch("https://old.reddit.com/r/todayilearned/top/.rss")
print(f"  bytes: {len(data)}")
items = parse(data)
print(f"  items: {len(items)}")
for it in items[:15]:
    print(f"  {it['title'][:80]} | {it['link'][:90]}")
