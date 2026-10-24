#!/usr/bin/env python3
"""Find 2nd source for white dwarf color study via Google/ArXiv RSS search."""
import urllib.request, urllib.parse, json, re, gzip

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Search via DuckDuckGo HTML for the study
query = urllib.parse.quote("white dwarf pink yellow purple carbon atmosphere University of Warwick RAS Techniques and Instruments")
url = f"https://html.duckduckgo.com/html/?q={query}"
req = urllib.request.Request(url, headers={"User-Agent": UA})
try:
    with urllib.request.urlopen(req, timeout=25) as resp:
        raw = resp.read()
        if raw[:2] == b'\x1f\x8b':
            raw = gzip.decompress(raw)
        text = raw.decode('utf-8', errors='replace')
    # Extract result snippets
    results = re.findall(r'result__snippet">(.*?)</a>', text, re.DOTALL)
    links = re.findall(r'result__a"[^>]*href="(.*?)"', text, re.DOTALL)
    print(f"Found {len(links)} DuckDuckGo results")
    for i, (l, s) in enumerate(zip(links[:8], results[:8])):
        s = re.sub(r'<[^>]+>', '', s).strip()
        print(f"\n[{i+1}] {l[:120]}")
        print(f"  {s[:300]}")
except Exception as e:
    print(f"DDG error: {e}")

# Also try ArXiv API search
print("\n=== ArXiv API ===")
aq = urllib.parse.quote("white dwarf color carbon atmosphere")
aurl = f"http://export.arxiv.org/api/query?search_query=all:{aq}&max_results=3"
try:
    req2 = urllib.request.Request(aurl, headers={"User-Agent": "OurWorldBot/1.0"})
    with urllib.request.urlopen(req2, timeout=20) as resp:
        atext = resp.read().decode('utf-8', errors='replace')
    titles = re.findall(r'<title>(.*?)</title>', atext)
    summaries = re.findall(r'<summary>(.*?)</summary>', atext, re.DOTALL)
    for t, s in zip(titles[1:4], summaries[:3]):
        print(f"Title: {t[:120]}")
        print(f"Summary: {s[:300]}")
        print()
except Exception as e:
    print(f"ArXiv error: {e}")
