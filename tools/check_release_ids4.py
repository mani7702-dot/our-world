#!/usr/bin/env python3
"""Check which ScienceDaily release IDs appear in existing content articles' source URLs."""
import re, html, os, subprocess

os.chdir("/home/ubuntu/our-world")

# Extract release IDs from all source URLs in existing content
all_content = ""
for f in os.listdir("content/news"):
    if f.endswith(".md"):
        with open(f"content/news/{f}", "r", errors="replace") as fh:
            all_content += fh.read() + "\n"

# Find all sciencedaily release IDs (format: 261021231238 etc - 14 digits)
existing_ids = set(re.findall(r"sciencedaily\.com/releases/\d{4}/\d{2}/(\d{14})\.htm", all_content))
existing_ids2 = set(re.findall(r"2610\d{12}", all_content))
print(f"Existing sciencedaily release IDs (pattern 1): {len(existing_ids)}")
print(f"Existing sciencedaily release IDs (pattern 2): {len(existing_ids2)}")

# Now check RSS items
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
        m = re.search(r"(\d{4}/\d{2}/(\d{14}))\.htm", link)
        rid = m.group(2) if m else ""
        in_content = rid in existing_ids2 if rid else False
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        slug_match = any(slug[:15] in f.lower() for f in os.listdir("content/news"))
        if in_content or slug_match:
            status = "ALREADY PUBLISHED"
        else:
            status = "*** FRESH? ***"
        print(f"{status}: {title}")
        print(f"  RID: {rid} | in_content: {in_content} | slug_match: {slug_match}")
