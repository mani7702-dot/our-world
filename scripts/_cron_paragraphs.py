#!/usr/bin/env python3
"""Extract paragraph text from saved HTML (Tirith-safe, file-based). Handles
both <p> and <article> blocks."""
import sys, re

def clean(html):
    html = re.sub(r'<script.*?</script>', '', html, flags=re.I|re.S)
    html = re.sub(r'<style.*?</style>', '', html, flags=re.I|re.S)
    return html

def main():
    h = clean(open(sys.argv[1], errors='replace').read())
    # grab the article body region if present, else whole
    am = re.search(r'<article[^>]*>(.*?)</article>', h, re.I|re.S)
    body = am.group(1) if am else h
    parts = []
    for m in re.finditer(r'<p[^>]*>(.*?)</p>', body, re.I|re.S):
        p = re.sub(r'<[^>]+>', '', m.group(1))
        p = re.sub(r'\s+', ' ', p).strip()
        if len(p) > 40:
            print(p)
    print("---KEYWORD HITS---")
    low = body.lower()
    for term in ["joseph bell", "conan doyle", "sherlock holmes", "edinburgh", "royal infirmary",
                 "surgical", "surgeon", "deduction", "1887", "1892", "1850", "forensic",
                 "born", "died", "1819", "1916"]:
        if term in low:
            idx = low.find(term)
            s = max(0, idx-50); e = min(len(low), idx+120)
            print(f"  [{term}] ...{low[s:e].replace(chr(10), ' ')}...")

if __name__ == "__main__":
    main()
