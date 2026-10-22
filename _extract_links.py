#!/usr/bin/env python3
"""Extract relevant links from search results."""
import re

# Check Google search results
with open("/tmp/search_www_8039.html", errors="replace") as f:
    html = f.read()
# Find links with plant armor or strawberry in them
links = re.findall(r'href="([^"]*)"[^>]*>([^<]*(?:plant armor|strawberry|Strawberry|Plant Armor)[^<]*)', html, re.I)
for url, text in links[:20]:
    clean_url = url
    if '&url=' in url:
        clean_url = url.split('&url=')[1].split('&')[0]
    if 'google.com' not in clean_url and 'gstatic' not in clean_url:
        print(f"LINK: {clean_url}")
        print(f"  TEXT: {text[:100]}")
        print()

# Also check NC State news search
with open("/tmp/news.ncsu.edu_148074.html", errors="replace") as f:
    html2 = f.read()
# Find article links
links2 = re.findall(r'href="(https://news\.ncsu\.edu/[^"]*)"', html2)
for url in links2[:20]:
    print(f"NCSU: {url}")
