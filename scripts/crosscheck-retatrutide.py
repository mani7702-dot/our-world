#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
crosscheck-retatrutide.py — Find a second source for the retatrutide AI study.
"""
import urllib.request, re, json

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Search DuckDuckGo HTML for the study
queries = [
    "retatrutide AI Reddit JAMA Network Open study",
    "retatrutide unapproved AI Reddit symptom",
]

for q in queries:
    url = f"https://html.duckduckgo.com/html/?q={urllib.request.quote(q)}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")
        # Extract result links and snippets
        links = re.findall(r'<a[^>]+href="(https?://[^"]+)"[^>]*class="result__a"[^>]*>(.*?)</a>', html, re.DOTALL)
        snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</span>', html, re.DOTALL)
        print(f"=== Query: {q} ===")
        for i, (link, title) in enumerate(links[:8]):
            title_clean = re.sub(r'<[^>]+>', '', title).strip()
            snip = ""
            if i < len(snippets):
                snip = re.sub(r'<[^>]+>', '', snippets[i]).strip()[:200]
            print(f"  {i}: {title_clean}")
            print(f"     URL: {link}")
            print(f"     Snippet: {snip}")
            print()
        if not links:
            # try alternate pattern
            all_links = re.findall(r'href="(https?://[^"]+)"', html)
            sd_links = [l for l in all_links if 'sciencedaily' in l or 'jamanetwork' in l or 'pubmed' in l or 'nih' in l or 'upenn' in l]
            print(f"  Raw links found: {len(all_links)}, relevant: {len(sd_links)}")
            for l in sd_links[:10]:
                print(f"    {l}")
    except Exception as e:
        print(f"ERROR for {q}: {e}")
    print()
