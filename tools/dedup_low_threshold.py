#!/usr/bin/env python3
"""Carefully dedup check with lower threshold."""
import re, html, os, subprocess

os.chdir("/home/ubuntu/our-world")

all_content = ""
for f in os.listdir("content/news"):
    if f.endswith(".md"):
        with open(f"content/news/{f}", "r", errors="replace") as fh:
            all_content += fh.read().lower() + "\n"

existing_files = set(os.listdir("content/news"))

url = "https://www.sciencedaily.com/rss/top.xml"
UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
p = subprocess.run(["curl", "-s", "-A", UA, url], capture_output=True)
data = p.stdout
idx = data.rfind(b"</rss>")
data = data[:idx + 6]

items = re.findall(rb"<item>(.*?)</item>", data, re.DOTALL)

BLOCK = (
    "cancer", "alzheimer", "covid", "pandemic", "stroke", "depression",
    "anxiety", "ptsd", "parkinson", "arthritis", "diabetes", "blood pressure",
    "statin", "colorectal", "inflammatory bowel", "cardiovascular",
    "heart disease", "glioblastoma", "rheumatoid", "weight-loss",
    "blood thinner", "lung cancer", "breast cancer", "brain cancer",
    "treatment", "therapy", "clinical trial",
)

safe_items = []
for it in items:
    t = re.search(rb"<title>(.*?)</title>", it, re.DOTALL)
    l = re.search(rb"<link>(.*?)</link>", it, re.DOTALL)
    if t and l:
        title = html.unescape(t.group(1).decode("utf-8", errors="replace")).strip()
        link = html.unescape(l.group(1).decode("utf-8", errors="replace")).strip()
        if any(b in title.lower() for b in BLOCK):
            continue
        words = [w.lower() for w in re.findall(r"\b[a-zA-Z]{5,}\b", title)]
        words = [w for w in words if w not in ("scient", "scientists", "discover", "scientist")]
        matched_words = [w for w in words if w in all_content]
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        slug_match = any(slug[:15] in f.lower() for f in existing_files)
        title_words = [w for w in re.findall(r"\b[a-zA-Z]{6,}\b", title.lower())]
        title_matches = sum(1 for w in title_words[:5] if w in all_content)
        safe_items.append({
            "title": title, "link": link, "slug": slug,
            "matched_words": matched_words, "slug_match": slug_match,
            "title_matches": title_matches,
        })

print("=== POTENTIALLY FRESH (no slug match, <=2 title matches) ===")
for item in safe_items:
    if not item["slug_match"] and item["title_matches"] <= 2:
        print(f"\nTitle: {item['title']}")
        print(f"  Slug: {item['slug']}")
        print(f"  URL: {item['link']}")
        print(f"  Matched keywords: {item['matched_words']}")
        print(f"  Title matches: {item['title_matches']}")

print(f"\n\n=== ALL SAFE ITEMS (sorted by fewest matches) ===")
safe_items.sort(key=lambda x: x["title_matches"])
for item in safe_items:
    print(f"  [{item['title_matches']} matches] {item['title'][:60]}")