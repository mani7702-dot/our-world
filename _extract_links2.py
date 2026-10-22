#!/usr/bin/env python3
"""Extract relevant links from search results."""
import re

# Check Google search results
with open("/tmp/search_www_6033.html", errors="replace") as f:
    html = f.read()
# Find all hrefs
all_links = re.findall(r'href="([^"]*)"', html)
for url in all_links:
    if any(k in url.lower() for k in ['plant armor', 'strawberry', 'ncsu', 'nc state', 'agricultur', 'horticulture', 'fabric']):
        if 'google.com' not in url and 'gstatic' not in url:
            print(f"LINK: {url}")

print("\n=== NCSU News ===")
with open("/tmp/search_news_7701.html", errors="replace") as f:
    html2 = f.read()
# Extract text content around "plant armor" or "strawberry"
text = re.sub(r'<[^>]+>', ' ', html2)
text = re.sub(r'\s+', ' ', text)
# Find context around "plant armor" or "strawberry"
for kw in ['plant armor', 'Plant Armor', 'strawberry']:
    idx = text.lower().find(kw.lower())
    if idx >= 0:
        print(f"Context for '{kw}':")
        print(text[max(0,idx-100):idx+300])
        print()
