#!/usr/bin/env python3
"""Check which ScienceDaily release IDs are already used in content/news."""
import re, html, os, subprocess

os.chdir("/home/ubuntu/our-world")

# Build content corpus
all_content = ""
for f in os.listdir("content/news"):
    if f.endswith(".md"):
        with open(f"content/news/{f}", "r", errors="replace") as fh:
            all_content += fh.read() + "\n"

# Extract all release IDs from existing content
existing_ids = set(re.findall(r"2610\d{10}", all_content))
print(f"Existing release IDs in content: {len(existing_ids)}")

# Get RSS items
url = "https://www.sciencedaily.com/rss/top.xml"
UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
p = subprocess.run(["curl", "-s", "-A", UA, url], capture_output=True)
data = p.stdout
idx = data.rfind(b"</rss>")
data = data[:idx + 6]

items = re.findall(rb"<item>(.*?)</item>", data, re.DOTALL)
print(f"\nTotal RSS items: {len(items)}")

# Check each item
for it in items:
    t = re.search(rb"<title>(.*?)</title>", it, re.DOTALL)
    l = re.search(rb"<link>(.*?)</link>", it, re.DOTALL)
    if t and l:
        title = html.unescape(t.group(1).decode("utf-8", errors="replace")).strip()
        link = html.unescape(l.group(1).decode("utf-8", errors="replace")).strip()
        # Extract release ID
        m = re.search(r"/(\d{4}/\d{2}/(\d{14}))\.htm", link)
        rid = m.group(2) if m else ""
        
        # Check if this release ID is used in content
        in_content = "IN CONTENT" if (rid and rid in all_content) else "NOT FOUND"
        
        # Check slug match
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        slug_match = any(slug[:20] in f.lower() for f in os.listdir("content/news"))
        
        status = "ALREADY PUBLISHED" if (slug_match or rid in existing_ids) else "FRESH?"
        print(f"\n{status}: {title}")
        print(f"  Release ID: {rid} ({in_content})")
        print(f"  URL: {link}")
