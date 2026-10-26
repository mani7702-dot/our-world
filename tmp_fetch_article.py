#!/usr/bin/env python3
"""Fetch an article URL and extract readable text."""
import sys
import urllib.request
import re
import html

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "OurWorldBot/1.0 (educational)", "Accept": "text/html"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")

def extract(raw):
    text = re.sub(r'<script[^>]*>.*?</script>', '', raw, flags=re.S)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.S)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

if __name__ == "__main__":
    url = sys.argv[1]
    raw = fetch(url)
    text = extract(raw)
    # Print a chunk around relevant content
    print(text[:3000])
