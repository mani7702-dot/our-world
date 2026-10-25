#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
find-paper-retatrutide.py — Search for the retatrutide AI study paper.
"""
import urllib.request, re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Try searching PubMed
url = "https://pubmed.ncbi.nlm.nih.gov/?term=retatrutide+AI+reddit+social+media&format=html"
req = urllib.request.Request(url, headers={"User-Agent": UA})
try:
    html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")
    # Extract PMIDs/links
    links = re.findall(r'/ PMC .*?pubmed\.ncbi\.nlm\.nih\.gov/(\d+)', html)
    if not links:
        links = re.findall(r'/pubmed\.ncbi\.nih\.gov/(\d+)', html)
    print(f"PubMed links found: {len(links)}")
    for l in links[:10]:
        print(f"  PMID: {l}")
    # Also print page title
    title = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    if title:
        print(f"Page title: {title.group(1).strip()[:200]}")
except Exception as e:
    print(f"PubMed ERROR: {e}")

# Try searching Google Scholar via a different approach
# Try the JAMA Network search directly
print()
url2 = "https://jamanetwork.com/"
req2 = urllib.request.Request(url2, headers={"User-Agent": UA})
try:
    html2 = urllib.request.urlopen(req2, timeout=20).read().decode("utf-8", "replace")
    title2 = re.search(r'<title>(.*?)</title>', html2, re.DOTALL)
    if title2:
        print(f"JAMA Network title: {title2.group(1).strip()[:200]}")
except Exception as e:
    print(f"JAMA Network ERROR: {e}")

# Try a broader approach: search via Wikipedia for retatrutide
print()
url3 = "https://en.wikipedia.org/wiki/Retatrutide"
req3 = urllib.request.Request(url3, headers={"User-Agent": UA})
try:
    html3 = urllib.request.urlopen(req3, timeout=20).read().decode("utf-8", "replace")
    # Extract first few paragraphs of the article body
    paras = re.findall(r'<p[^>]*>(.*?)</p>', html3, re.DOTALL)
    print("Wikipedia Retatrutide article paragraphs:")
    count = 0
    for p in paras:
        clean = re.sub(r'<[^>]+>', '', p).strip()
        clean = re.sub(r'\s+', ' ', clean)
        if len(clean) > 50 and 'retatrutide' in clean.lower():
            print(f"  {clean[:300]}")
            print()
            count += 1
            if count >= 5:
                break
    if count == 0:
        # Try any paragraph
        for p in paras:
            clean = re.sub(r'<[^>]+>', '', p).strip()
            if len(clean) > 100:
                print(f"  {clean[:300]}")
                print()
                count += 1
                if count >= 3:
                    break
except Exception as e:
    print(f"Wikipedia ERROR: {e}")
