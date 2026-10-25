#!/usr/bin/env python3
"""Cross-check the Amazon biodiversity ScienceDaily article and verify dedup."""
import subprocess, urllib.request, re, os

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

url = "https://www.sciencedaily.com/releases/2026/09/260920222356.htm"

# Fetch the page
req = urllib.request.Request(url, headers={"User-Agent": UA})
resp = urllib.request.urlopen(req, timeout=30)
html = resp.read().decode("utf-8", errors="replace")
print(f"Page size: {len(html)} bytes")

# Extract title
title_match = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
if title_match:
    print(f"Title: {title_match.group(1).strip()}")

# Extract meta description
desc_match = re.search(r'<meta name="description" content="(.*?)"', html, re.DOTALL)
if desc_match:
    print(f"Description: {desc_match.group(1).strip()[:500]}")

# Try to extract article body - look for <p> tags in article
# ScienceDaily article body is typically in a div with class
paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
print(f"\n=== Paragraphs found: {len(paragraphs)} ===")
for i, p in enumerate(paragraphs[:15]):
    clean = re.sub(r'<[^>]+>', '', p).strip()
    if len(clean) > 40:
        print(f"\n[{i}] {clean[:300]}")

# Check for Amazon/biodiversity keywords in existing content
print("\n=== DEDUP CHECK: 'Amazon biodiversity' ===")
keywords = ["amazon", "biodiversity", "carbon"]
for fname in sorted(os.listdir("content/news/")):
    if not fname.endswith(".md"): continue
    path = os.path.join("content/news/", fname)
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read().lower()
            title = open(path, encoding="utf-8").readline()
        matched = [k for k in keywords if k in text]
        if len(matched) >= 2:
            print(f"  POTENTIAL MATCH: {fname} (matched: {matched})")
    except:
        pass
