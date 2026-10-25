#!/usr/bin/env python3
"""Dedup checker - compare ScienceDaily top.xml items against existing content/news"""
import html, re, os, subprocess, sys

os.chdir("/home/ubuntu/our-world")

url = "https://www.sciencedaily.com/rss/top.xml"
UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
data = p.stdout
idx = data.rfind(b"</rss>")
data = data[:idx + 6]
items = re.findall(rb"<item>(.*?)</item>", data, re.DOTALL)

titles = []
for it in items:
    t = re.search(rb"<title>(.*?)</title>", it, re.DOTALL)
    l = re.search(rb"<link>(.*?)</link>", it, re.DOTALL)
    if t and l:
        title = html.unescape(t.group(1).decode("utf-8", errors="replace").strip())
        link = html.unescape(l.group(1).decode("utf-8", errors="replace").strip())
        slug = re.sub(r"[^a-zA-Z0-9]+", "-", title.lower()).strip("-")
        titles.append((title, slug, link))

# Get all existing article filenames
existing_files = os.listdir("content/news")

# Build content corpus from ALL existing articles
all_content = ""
for f in existing_files:
    filepath = f"content/news/{f}"
    if os.path.isfile(filepath):
        with open(filepath, "r", errors="replace") as fh:
            all_content += fh.read().lower() + "\n"

# Blocked keywords (medical/scary)
BLOCK = (
    "cancer", "alzheimer", "covid", "pandemic", "stroke", "depression",
    "anxiety", "ptsd", "parkinson", "arthritis", "diabetes", "blood pressure",
    "statin", "colorectal", "inflammatory bowel", "cardiovascular",
    "heart disease", "glioblastoma", "rheumatoid", "weight-loss drug",
    "blood thinner", "brain cancer", "lung cancer", "breast cancer",
    "surgery", "treatment", "therapy", "clinical trial", "disease",
)

fresh = []
filtered_out = []
for title, slug, link in titles:
    low_title = title.lower()

    # Skip blocked items
    if any(b in low_title for b in BLOCK):
        filtered_out.append((title, "blocked medical/scary"))
        continue

    # Check slug match against filenames
    slug_found = any(slug in f.lower() for f in existing_files)
    if slug_found:
        filtered_out.append((title, "slug match"))
        continue

    # Check keywords against all content for dedup
    kws = [w for w in re.findall(r"\b\w{5,}\b", low_title)]
    matches = sum(1 for kw in kws[:8] if kw in all_content)
    if matches >= 3:
        filtered_out.append((title, f"keyword dedup ({matches} matches)"))
        continue

    fresh.append((title, slug, link))

print("=== POTENTIALLY FRESH (after kid-safety + dedup) ===")
for t, s, l in fresh:
    print(f"  {t}")
    print(f"    slug: {s}")
    print(f"    url:  {l}")
    print()

print(f"\nTotal items: {len(titles)}")
print(f"Fresh candidates: {len(fresh)}")

print("\n=== FILTERED OUT ===")
for t, reason in filtered_out:
    print(f"  [{reason}] {t}")
