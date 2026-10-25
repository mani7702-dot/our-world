#!/usr/bin/env python3
"""Fetch articles from the ScienceDaily RSS article pages directly.
Try fetching the full article content from a few promising ScienceDaily URLs.
Also extract author/source info from each article."""
import urllib.request, re, html, os

os.chdir("/home/ubuntu/our-world")
UA_BROWSER = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Let's check the actual ScienceDaily article pages for their full content
# and see what topics are truly fresh
urls_to_check = [
    "https://www.sciencedaily.com/releases/2026/10/261020085021.htm",  # A train was delayed by a solar storm
    "https://www.sciencedaily.com/releases/2026/10/261016070633.htm",   # might be different
    "https://www.sciencedaily.com/releases/2026/10/261015073207.htm",   # might be different
    "https://www.sciencedaily.com/releases/2026/10/261014015457.htm",
    "https://www.sciencedaily.com/releases/2026/10/261016070628.htm",
]

for url in urls_to_check:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA_BROWSER})
        data = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", errors="replace")
        
        # Extract title
        t = re.search(r"<title>(.*?)</title>", data)
        title = html.unescape(t.group(1).strip()).replace(" -- ScienceDaily", "") if t else "No title"
        
        # Extract meta description
        d = re.search(r'<meta name="description" content="(.*?)"', data)
        desc = html.unescape(d.group(1).strip()) if d else ""
        
        # Extract source
        s = re.search(r'<meta name="author" content="(.*?)"', data)
        author = html.unescape(s.group(1).strip()) if s else ""
        
        print(f"\n=== {title}")
        print(f"URL: {url}")
        print(f"Desc: {desc[:300]}")
        print(f"Author: {author}")
        
    except Exception as e:
        print(f"\n=== FAILED: {url} — {e}")
