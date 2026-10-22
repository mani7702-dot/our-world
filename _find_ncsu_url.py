#!/usr/bin/env python3
"""Find and download the NC State News article URL."""
import re

# Parse NC State news search page for the article URL
with open("/tmp/search_news_7701.html", errors="replace") as f:
    html = f.read()

# Find all links to news.ncsu.edu
links = re.findall(r'href="(https://news\.ncsu\.edu/[^"]*)"', html)
for url in links:
    print(f"URL: {url}")

# Also try to find the direct link
links2 = re.findall(r'href="([^"]*plant[^"]*|[^"]*strawberry[^"]*)"', html, re.I)
for url in links2:
    if 'ncsu' in url or 'plant' in url.lower() or 'straw' in url.lower():
        print(f"MATCH: {url}")

# Check if there's an article link in the HTML
import re
article_links = re.findall(r'href="([^"]*)"[^>]*>[^<]*(?:Plant Armor|plant armor|strawberry|Strawberry)[^<]*</a>', html)
for url in article_links:
    print(f"ARTICLE: {url}")
