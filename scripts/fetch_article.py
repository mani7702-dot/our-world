#!/usr/bin/env python3
"""Fetch article content via urllib with browser UA."""
import sys
import re
from urllib.request import Request, urlopen

def fetch_article(url):
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })
    resp = urlopen(req, timeout=30)
    html = resp.read().decode('utf-8', errors='replace')

    # Try <article> tag first
    article = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL | re.IGNORECASE)
    if article:
        text = re.sub(r'<[^>]+>', ' ', article.group(1))
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    # Fall back to main content
    main = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL | re.IGNORECASE)
    if main:
        text = re.sub(r'<[^>]+>', ' ', main.group(1))
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    return "NO ARTICLE FOUND"

if __name__ == '__main__':
    url = sys.argv[1]
    print(fetch_article(url)[:5000])
