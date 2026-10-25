#!/usr/bin/env python3
"""Fetch ScienceDaily article body via direct urllib (Jina blocked for ScienceDaily)."""
import urllib.request, sys, re

url = sys.argv[1]
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
req = urllib.request.Request(url, headers={"User-Agent": UA})
resp = urllib.request.urlopen(req, timeout=25)
data = resp.read().decode("utf-8", errors="replace")

# Extract the article body from <div id="text"> tag
match = re.search(r'<div[^>]*id="text"[^>]*>(.*?)</div>\s*<div[^>]*id="sources"', data, re.DOTALL)
if not match:
    # Try alternate: find the story body between id="text" and the next major div
    match = re.search(r'id="text"[^>]*>(.*?)(?:<div[^>]*id="sources"|<aside|<footer)', data, re.DOTALL)
if not match:
    match = re.search(r'<article[^>]*>(.*?)</article>', data, re.DOTALL)
if not match:
    print("WARNING: Could not find article body tag")
    print("=" * 60)
    text = data
else:
    body = match.group(1)
    text = re.sub(r'<[^>]+>', ' ', body)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&#039;', "'", text)
    text = re.sub(r'&quot;', '"', text)
    text = re.sub(r'&#8211;', '–', text)
    text = re.sub(r'&#8217;', "'", text)
    text = re.sub(r'&ndash;', '–', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()

print(text[:6000])
