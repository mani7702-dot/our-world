#!/usr/bin/env python3
"""Fetch content via Jina Reader proxy."""
import urllib.request
import urllib.parse
import re

def fetch_via_jina(url):
    jina_url = f"https://r.jina.ai/{url}"
    req = urllib.request.Request(jina_url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        "X-Return-Format": "text"
    })
    resp = urllib.request.urlopen(req, timeout=30)
    return resp.read().decode('utf-8', errors='replace')

# Try to fetch via Jina - BBC article
url = "https://www.bbc.co.uk/news/articles/cmz98plpjzplo"
try:
    text = fetch_via_jina(url)
    print(text[:4000])
except Exception as e:
    print(f"Jina error: {e}")

print("\n=== Now checking Wikipedia for Nakumatt ===")
wiki_nakumatt = "https://en.wikipedia.org/wiki/Nakumatt"
try:
    req = urllib.request.Request(wiki_nakumatt, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })
    resp = urllib.request.urlopen(req, timeout=30)
    html = resp.read().decode('utf-8', errors='replace')
    # Extract text from body
    body = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL | re.IGNORECASE)
    if body:
        text = re.sub(r'<[^>]+>', ' ', body.group(1))
        text = re.sub(r'\s+', ' ', text).strip()
        print(text[:3000])
except Exception as e:
    print(f"Wikipedia error: {e}")

print("\n=== Now checking Wikipedia API for Tuskys ===")
try:
    api_url = "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=true&explaintext=true&titles=Tuskys&format=json"
    req = urllib.request.Request(api_url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })
    resp = urllib.request.urlopen(req, timeout=30)
    text = resp.read().decode('utf-8', errors='replace')
    print(text[:2000])
except Exception as e:
    print(f"Wikipedia API error: {e}")
