#!/usr/bin/env python3
"""Fetch article body from Space.com using direct HTML fetch (Jina Reader blocks Space.com)."""
import urllib.request
import re
import sys

def fetch_article(url):
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    resp = urllib.request.urlopen(req, timeout=30)
    html = resp.read().decode("utf-8", errors="replace")
    return html

def extract_article(html):
    # Try to find <article> tag content
    article_match = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL | re.IGNORECASE)
    if article_match:
        article_html = article_match.group(1)
    else:
        # Fallback: find main content area
        article_html = html

    # Extract all <p> tags
    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', article_html, re.DOTALL | re.IGNORECASE)

    # Clean each paragraph
    cleaned = []
    for p in paragraphs:
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', p)
        # Decode HTML entities
        text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace("&#39;", "'").replace('&nbsp;', ' ')
        # Strip whitespace
        text = text.strip()
        # Only keep paragraphs with meaningful content
        if len(text) > 50:
            cleaned.append(text)

    return cleaned

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://www.space.com/space-exploration/on-this-day-in-space-october-23-2026"
    html = fetch_article(url)
    paragraphs = extract_article(html)
    print(f"=== ARTICLE BODY ({len(paragraphs)} paragraphs) ===")
    for i, p in enumerate(paragraphs):
        print(f"\n--- Paragraph {i+1} ---")
        print(p)
