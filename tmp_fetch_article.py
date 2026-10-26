#!/usr/bin/env python3
"""Fetch the ScienceDaily article and cross-check with Wikipedia/JWST info."""
import urllib.request, gzip

url = "https://www.sciencedaily.com/releases/2026/10/261012185021.htm"
req = urllib.request.Request(url, headers={
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
})
try:
    raw = urllib.request.urlopen(req, timeout=30).read()
    if raw[:2] == b'\x1f\x8b':
        raw = gzip.decompress(raw)
    html = raw.decode('utf-8', errors='replace')
    print(f"[fetch] Article fetched: {len(html)} bytes")
    
    # Extract the article body - ScienceDaily articles are in <div id="text"> or similar
    import re
    # Get the title
    title_m = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    if title_m:
        print(f"\n[TITLE] {title_m.group(1).strip()}")
    
    # Extract description/meta
    desc_m = re.search(r'<meta name="description" content="(.*?)"', html)
    if desc_m:
        print(f"\n[DESCRIPTION] {desc_m.group(1).strip()}")
    
    # Extract article text from the main content div
    # ScienceDaily uses <div id="text"> for the article
    article_m = re.search(r'<div id="text">(.*?)</div>\s*<div id="sources"', html, re.DOTALL)
    if not article_m:
        article_m = re.search(r'<div id="text">(.*?)</div>\s*</div>', html, re.DOTALL)
    if not article_m:
        # Try alternative
        article_m = re.search(r'<div[^>]*id="text"[^>]*>(.*?)</div>', html, re.DOTALL)
    if not article_m:
        article_m = re.search(r'<div id="abstract">(.*?)</div>', html, re.DOTALL)
    
    if article_m:
        text = article_m.group(1)
        # Strip HTML tags
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        print(f"\n[ARTICLE BODY]\n{text[:3000]}")
    else:
        # Try to get the full article content
        # Look for the main article content
        main_m = re.search(r'<td[^>]*valign="top"[^>]*>(.*?)</td>', html, re.DOTALL | re.IGNORECASE)
        if main_m:
            text = re.sub(r'<[^>]+>', ' ', main_m.group(1))
            text = re.sub(r'\s+', ' ', text)
            print(f"\n[ARTICLE BODY]\n{text[:3000]}")
        else:
            print("\n[ARTICLE BODY] Could not extract - showing first 2000 chars of text content")
            text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
            text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
            text = re.sub(r'<[^>]+>', ' ', text)
            text = re.sub(r'\s+', ' ', text)
            print(text[:3000])
except Exception as e:
    print(f"[fetch] Error: {e}")
