#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
get-paper-details.py — Fetch the PubMed abstract and PMC summary for the retatrutide AI study.
"""
import urllib.request, re, json

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# PubMed abstract for PMID 42873503
url1 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=42873503&retmode=json"
req1 = urllib.request.Request(url1, headers={"User-Agent": UA})
try:
    resp1 = urllib.request.urlopen(req1, timeout=20).read().decode("utf-8", "replace")
    data1 = json.loads(resp1)
    print("=== PubMed Abstract ===")
    docsum = data1.get("result", {}).get("42873503", {})
    print(f"Title: {docsum.get('title', 'N/A')}")
    print(f"Full journal: {docsum.get('fulljournalname', 'N/A')}")
    print(f"PubDate: {docsum.get('pubdate', 'N/A')}")
    print(f"Authors: {[a.get('name','') for a in docsum.get('authors',[])]}")
    print(f"DOI: {docsum.get('doi', 'N/A')}")
    print(f"PMC: {docsum.get('pmc', 'N/A')}")
    print(f"PubMed URL: https://pubmed.ncbi.nlm.nih.gov/42873503/")
    print(f"PMC URL: https://www.ncbi.nlm.nih.gov/pmc/articles/{docsum.get('pmc','')}/")
    print()
    # Print the abstract if available
    if "summary" in docsum:
        print(f"Summary: {docsum['summary'][:300]}")
except Exception as e:
    print(f"PubMed ERROR: {e}")

# PMC full text for PMC13670051
print("=== PMC Summary ===")
url2 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pmc&id=13670051&retmode=json"
req2 = urllib.request.Request(url2, headers={"User-Agent": UA})
try:
    resp2 = urllib.request.urlopen(req2, timeout=20).read().decode("utf-8", "replace")
    data2 = json.loads(resp2)
    result = data2.get("result", {}).get("13670051", {})
    print(f"Title: {result.get('title', 'N/A')}")
    print(f"Journal: {result.get('source', 'N/A')}")
    print(f"Authors: {[a.get('name','') for a in result.get('authors',[])]}")
    print()
except Exception as e:
    print(f"PMC ERROR: {e}")

# Try fetching the actual abstract via eutils
print("=== PubMed Abstract (efetch) ===")
url3 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=42873503&retmode=abstract"
req3 = urllib.request.Request(url3, headers={"User-Agent": UA})
try:
    resp3 = urllib.request.urlopen(req3, timeout=20).read().decode("utf-8", "replace")
    # Extract text content
    clean = re.sub(r'<[^>]+>', ' ', resp3)
    clean = re.sub(r'\s+', ' ', clean).strip()
    print(clean[:2000])
except Exception as e:
    print(f"efetch ERROR: {e}")
