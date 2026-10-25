#!/usr/bin/env python3
"""Fetch titles from ALL ScienceDaily top page articles and check for freshness."""
import urllib.request, re, html, os

os.chdir("/home/ubuntu/our-world")

URL = "https://www.sciencedaily.com/news/top/"
UA = "Mozilla/5.0 (compatible: OurWorldBot; contact andugulamani722@gmail.com)"

req = urllib.request.Request(URL, headers={"User-Agent": UA})
data = urllib.request.urlopen(req, timeout=25).read().decode("utf-8", errors="replace")

# Get all release links - broader pattern to catch different URL formats
all_href = re.findall(r'href="([^"]*releases/\d{4}/\d{2}/\d{8}\.htm[^"]*)"', data)
all_href = list(dict.fromkeys(all_href))

UA_BROWSER = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

items = []
for link in all_href[:50]:
    full_url = "https://www.sciencedaily.com" + link if not link.startswith("http") else link
    try:
        req2 = urllib.request.Request(full_url, headers={"User-Agent": UA_BROWSER})
        page = urllib.request.urlopen(req2, timeout=20).read().decode("utf-8", errors="replace")
        # Extract title
        t_match = re.search(r"<title>(.*?)</title>", page)
        title = html.unescape(t_match.group(1).strip()).replace(" -- ScienceDaily", "") if t_match else "No title"
        # Extract summary
        s_match = re.search(r'<meta name="description" content="(.*?)"', page)
        summary = html.unescape(s_match.group(1).strip()) if s_match else ""
        items.append({"title": title, "url": full_url, "summary": summary[:300]})
        print(f"\n--- {title}")
        print(f"  url: {full_url}")
        print(f"  summary: {summary[:200]}")
    except Exception as e:
        print(f"\n--- FAILED: {full_url} — {e}")

# Save to file for analysis
import json
with open("_sd_titles.json", "w") as f:
    json.dump(items, f, indent=2)
print(f"\n\nTotal fetched: {len(items)}")
