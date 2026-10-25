#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
find-paper2.py — Better search for the retatrutide AI study.
"""
import urllib.request, re, json

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Try NCBI with broader terms
urls = [
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=Guntuku+retatrutide&retmode=json&retmax=5",
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term= Ungar+retatrutide+reddit&retmode=json&retmax=5",
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=(retatrutide OR semaglutide) AND (reddit OR social media) AND (AI OR machine learning OR LLM)&retmode=json&retmax=5",
]

for url in urls:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        resp = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")
        data = json.loads(resp)
        ids = data.get("esearchresult", {}).get("idlist", [])
        count = data.get("esearchresult", {}).get("count", "0")
        print(f"URL: {url.split('term=')[1][:60]}")
        print(f"Count: {count}, IDs: {ids}")
    except Exception as e:
        print(f"ERROR: {e}")
    print()

# Try fetching one of the PMC IDs
print("=== Fetching PMC article ===")
req = urllib.request.Request("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pmc&id=13670051&retmode=json", headers={"User-Agent": UA})
try:
    resp = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")
    data = json.loads(resp)
    print(json.dumps(data, indent=2)[:500])
except Exception as e:
    print(f"ERROR: {e}")

# Try to find via JAMA Network search API
print("\n=== JAMA Network search ===")
url2 = "https://jamanetwork.com/journals/jamanetworkopen/search?query=retatrutide+reddit+AI"
req2 = urllib.request.Request(url2, headers={"User-Agent": UA})
try:
    html = urllib.request.urlopen(req2, timeout=20).read().decode("utf-8", "replace")
    title = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    if title:
        print(f"JAMA title: {title.group(1).strip()[:200]}")
    # Look for result links
    links = re.findall(r'/doi/(10\.\d+/[^\s"<]+)', html)[:5]
    for l in links:
        print(f"  DOI: {l}")
    if not links:
        links2 = re.findall(r'href="(/journals/[^"]+)"', html)[:5]
        for l in links2:
            print(f"  Path: {l}")
except Exception as e:
    print(f"JAMA ERROR: {e}")
