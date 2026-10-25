#!/usr/bin/env python3
"""Fetch recent ScienceDaily release articles to find truly fresh topics.
Check articles with release IDs we haven't seen published."""
import urllib.request, re, html, os

os.chdir("/home/ubuntu/our-world")
UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"

# Fetch the RSS feed
req = urllib.request.Request("https://www.sciencedaily.com/rss/top.xml", headers={"User-Agent": UA})
data = urllib.request.urlopen(req, timeout=25).read()
idx = data.rfind(b"</rss>")
data = data[:idx + 6]

items = re.findall(rb"<item>(.*?)</item>", data, re.DOTALL)
print(f"Total RSS items: {len(items)}")

# Check which release IDs are NOT in our published articles
existing_files = set(os.listdir("content/news"))
existing_slugs = set()
for f in existing_files:
    if f.endswith(".md"):
        existing_slugs.add(f.lower().replace(".md", ""))

# Get all release URLs from the feed
release_urls = []
for it in items:
    l = re.search(rb"<link>(.*?)</link>", it, re.DOTALL)
    if l:
        url = html.unescape(l.group(1).decode("utf-8", errors="replace").strip())
        release_urls.append(url)

# Extract release IDs (like 261021231238)
release_ids = []
for url in release_urls:
    m = re.search(r"(\d{14})\.htm", url)
    if m:
        release_ids.append(m.group(1))

print(f"\nRelease IDs in RSS: {release_ids}")

# Now check which release IDs appear in the existing content (in sources URLs)
all_content = ""
for f in os.listdir("content/news"):
    if f.endswith(".md"):
        with open(f"content/news/{f}", "r", errors="replace") as fh:
            all_content += fh.read() + "\n"

# Check each release ID against existing content
for rid in release_ids:
    if rid in all_content:
        print(f"  {rid} - ALREADY in content")
    else:
        print(f"  {rid} - NOT in content sources")
