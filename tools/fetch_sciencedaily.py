#!/usr/bin/env python3
"""Fetch ScienceDaily article body via direct urllib (Jina blocked for ScienceDaily)."""
import urllib.request, sys, re

url = sys.argv[1] if len(sys.argv) > 1 else "https://www.sciencedaily.com/releases/2026/10/261022081302.htm"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

req = urllib.request.Request(url, headers={"User-Agent": UA})
resp = urllib.request.urlopen(req, timeout=25)
data = resp.read().decode("utf-8", errors="replace")

# Extract the article body from <article> tag or story_text div
# ScienceDaily uses <div id="text" class="col-md-10"> for the article body
match = re.search(r'<div[^>]*id="text"[^>]*>(.*?)</div>\s*<div[^>]*id="sources"', data, re.DOTALL)
if not match:
    match = re.search(r'<article[^>]*>(.*?)</article>', data, re.DOTALL)
if not match:
    # Try to find the main content div
    match = re.search(r'<div[^>]*class="col-md-10"[^>]*>(.*?)</div>\s*<div[^>]*class="col-md-2"', data, re.DOTALL)

if match:
    body = match.group(1)
else:
    body = data
    print("WARNING: Could not find article body tag, showing full page snippet")
    print("=" * 60)

# Strip HTML tags for readable text
text = re.sub(r'<[^>]+>', ' ', body)
text = re.sub(r'&amp;', '&', text)
text = re.sub(r'&lt;', '<', text)
text = re.sub(r'&gt;', '>', text)
text = re.sub(r'&nbsp;', ' ', text)
text = re.sub(r'&#039;', "'", text)
text = re.sub(r'&quot;', '"', text)
text = re.sub(r'\s+', ' ', text)
text = text.strip()

print(text[:5000])
