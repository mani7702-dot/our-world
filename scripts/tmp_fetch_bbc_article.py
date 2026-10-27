#!/usr/bin/env python3
"""Check if the Mars moon mission BBC article is the same as the Japan MMX one."""
import urllib.request, re

# Fetch the BBC article
url = 'https://www.bbc.co.uk/news/articles/cmvgxvkv54w1o'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})
raw = urllib.request.urlopen(req, timeout=25).read().decode('utf-8', errors='ignore')

# Extract article text
# Find the body content
body_match = re.search(r'<article[^>]*>(.*?)</article>', raw, re.S)
if body_match:
    body = re.sub(r'<[^>]+>', ' ', body_match.group(1))
    body = re.sub(r'\s+', ' ', body).strip()
    print(body[:2000])
else:
    # Try main content
    main_match = re.search(r'<main[^>]*>(.*?)</main>', raw, re.S)
    if main_match:
        body = re.sub(r'<[^>]+>', ' ', main_match.group(1))
        body = re.sub(r'\s+', ' ', body).strip()
        print(body[:2000])
    else:
        print("Could not find article body")
        # Print some text
        text = re.sub(r'<[^>]+>', ' ', raw)
        text = re.sub(r'\s+', ' ', text).strip()
        # Find relevant part
        idx = text.lower().find('mars')
        if idx > 0:
            print(text[max(0,idx-200):idx+2000])
        else:
            print(text[:2000])
