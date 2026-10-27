#!/usr/bin/env python3
"""Fetch the BBC zebra-striped bee article and the Mars mission article for cross-check."""
import urllib.request, re

# Fetch zebra bee article
url = 'https://www.bbc.co.uk/news/articles/c3dxwjx7xpj0o'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})
raw = urllib.request.urlopen(req, timeout=25).read().decode('utf-8', errors='ignore')
text = re.sub(r'<[^>]+>', ' ', raw)
text = re.sub(r'\s+', ' ', text).strip()

# Find the relevant part about bees
idx = text.lower().find('bee')
if idx > 0:
    print("=== Zebra bee article ===")
    print(text[max(0,idx-100):idx+2000])
