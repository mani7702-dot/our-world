#!/usr/bin/env python3
"""Fetch and clean a Wikipedia article for cross-checking."""
import urllib.request, sys, re, json, html

url = sys.argv[1]
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
req = urllib.request.Request(url, headers={"User-Agent": UA})
resp = urllib.request.urlopen(req, timeout=25)
data = resp.read().decode("utf-8", errors="replace")

# Extract main content from Wikipedia
# Wikipedia puts content in <div id="mw-content-text"> 
match = re.search(r'<div[^>]*id="mw-content-text"[^>]*>(.*?)</div>\s*<div[^>]*id="catlinks"', data, re.DOTALL)
if not match:
    match = re.search(r'<div[^>]*id="bodyContent"[^>]*>(.*?)(?:<div[^>]*id="catlinks"|</body>)', data, re.DOTALL)
if not match:
    body = data
else:
    body = match.group(1)

# Get paragraphs
paras = re.findall(r'<p[^>]*>(.*?)</p>', body, re.DOTALL)
clean = []
for p in paras:
    text = re.sub(r'<[^>]+>', ' ', p)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) > 30:
        clean.append(text)

print("\n\n".join(clean[:30])[:6000])
