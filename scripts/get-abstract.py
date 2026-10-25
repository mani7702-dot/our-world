#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
get-abstract.py — Get the full abstract from PubMed for PMID 42873503.
"""
import urllib.request, re, json

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Fetch the PMC article page directly
pmcid = "13670051"
url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC13670051/"
req = urllib.request.Request(url, headers={"User-Agent": UA})
try:
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
    # Try to extract the abstract
    # Look for abstract section
    abstract_match = re.search(r'<div class="tsec"[^>]*>.*?<h2[^>]*>Abstract</h2>(.*?)</div>', html, re.DOTALL | re.IGNORECASE)
    if not abstract_match:
        # Try another pattern
        abstract_match = re.search(r'id="abstract".*?>(.*?)(?=<h2|<div class="sec)', html, re.DOTALL | re.IGNORECASE)
    if not abstract_match:
        # Try generic p tags after "Abstract" heading
        abstract_match = re.search(r'Abstract\s*</h2>\s*(.*?)(?=<h2|<div class="sec)', html, re.DOTALL | re.IGNORECASE)
    
    if abstract_match:
        abstract_html = abstract_match.group(1)
        clean = re.sub(r'<[^>]+>', ' ', abstract_html)
        clean = re.sub(r'\s+', ' ', clean).strip()
        print(f"Abstract ({len(clean)} chars):")
        print(clean[:3000])
    else:
        print("Abstract not found via patterns. Trying p extraction...")
        # Get all p tags
        paras = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
        for i, p in enumerate(paras):
            clean = re.sub(r'<[^>]+>', '', p).strip()
            clean = re.sub(r'\s+', ' ', clean)
            if len(clean) > 50 and ('abstract' in clean.lower() or 'background' in clean.lower() or 'objective' in clean.lower() or 'design' in clean.lower() or 'main outcome' in clean.lower() or 'results' in clean.lower() or 'conclusion' in clean.lower() or 'significance' in clean.lower() or 'exposure' in clean.lower() or 'effect' in clean.lower()):
                print(f"[{i}] {clean[:300]}")
    print(f"\nTotal HTML size: {len(html)}")
except Exception as e:
    print(f"ERROR: {e}")

# Also try the PubMed page directly
print("\n=== PubMed page ===")
url2 = "https://pubmed.ncbi.nlm.nih.gov/42873503/"
req2 = urllib.request.Request(url2, headers={"User-Agent": UA})
try:
    html2 = urllib.request.urlopen(req2, timeout=30).read().decode("utf-8", "replace")
    # Extract abstract from meta tag or the page content
    meta = re.search(r'<meta name="citation_abstract" content="([^"]+)"', html2)
    if meta:
        print(f"Meta abstract: {meta.group(1)[:2000]}")
    else:
        # Try to find abstract in the page
        abs_match = re.search(r'Abstract.*?(?=Background|Methods|Results|Conclusion|<h2)', html2, re.DOTALL | re.IGNORECASE)
        if abs_match:
            clean = re.sub(r'<[^>]+>', ' ', abs_match.group(0))
            clean = re.sub(r'\s+', ' ', clean).strip()
            print(f"Page abstract: {clean[:2000]}")
        else:
            # Get og:description
            og = re.search(r'<meta property="og:description" content="([^"]+)"', html2)
            if og:
                print(f"OG description: {og.group(1)[:2000]}")
            else:
                print("No abstract found")
except Exception as e:
    print(f"ERROR: {e}")
