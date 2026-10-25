#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
find-jama-paper.py — Try to find the JAMA Network Open paper on retatrutide AI study.
"""
import urllib.request, re, json

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Try searching via the NCBI PMC search API
urls = [
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term=retatrutide+AI+social+media&retmode=json&retmax=5",
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=retatrutide+reddit+artificial+intelligence&retmode=json&retmax=5",
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=retatrutide+social+media+symptom+AI&retmode=json&retmax=5",
]

for url in urls:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        resp = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")
        data = json.loads(resp)
        print(f"URL: {url}")
        print(f"Result: {json.dumps(data, indent=2)[:500]}")
        print()
    except Exception as e:
        print(f"ERROR for {url}: {e}")
        print()

# Also try to find the paper via Google Scholar-like search
# Try the medRxiv or bioRxiv preprint search
print("=== Trying medRxiv ===")
url4 = "https://www.medrxiv.org/search/retatrutide%20AI%20social%20media"
req4 = urllib.request.Request(url4, headers={"User-Agent": UA})
try:
    html4 = urllib.request.urlopen(req4, timeout=20).read().decode("utf-8", "replace")
    title = re.search(r'<title>(.*?)</title>', html4, re.DOTALL)
    if title:
        print(f"medRxiv title: {title.group(1).strip()[:200]}")
    # Find result links
    links = re.findall(r'/doi/([^"\s]+)', html4)[:5]
    for l in links:
        print(f"  DOI: {l}")
except Exception as e:
    print(f"medRxiv ERROR: {e}")

# Try to find via the Penn study
print()
print("=== Trying UPenn news ===")
url5 = "https://www.google.com/search?q=retatrutide+AI+Reddit+JAMA+Network+Open+study+university+of+pennsylvania"
req5 = urllib.request.Request("https://www.google.com/search?q=retatrutide+AI+Reddit+JAMA+Network+Open+study+university+of+pennsylvania", headers={"User-Agent": UA})
try:
    html5 = urllib.request.urlopen(req5, timeout=20).read().decode("utf-8", "replace")
    title5 = re.search(r'<title>(.*?)</title>', html5, re.DOTALL)
    if title5:
        print(f"Google title: {title5.group(1).strip()[:200]}")
    # Find links
    links = re.findall(r'https?://[^\s"<>|]+\.jamanetwork\.com[^\s"<>|]*', html5)[:5]
    for l in links:
        print(f"  JAMA link: {l}")
    links2 = re.findall(r'https?://[^\s"<>|]+\.nih\.gov[^\s"<>|]*', html5)[:5]
    for l in links2:
        print(f"  NIH link: {l}")
except Exception as e:
    print(f"Google ERROR: {e}")
