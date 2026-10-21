#!/usr/bin/env python3
"""Extract article from saved HTML for cross-check."""
import sys, re

def extract(path):
    with open(path, 'r', errors='replace') as f:
        html = f.read()
    
    # Title
    m = re.search(r'<title>(.*?)</title>', html, re.I | re.S)
    title = m.group(1).strip() if m else "NO TITLE"
    
    # Meta description
    m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.I)
    desc = m.group(1).strip() if m else ""
    
    # Try to find article body
    # Remove scripts, styles
    html2 = re.sub(r'<script.*?</script>', '', html, flags=re.I|re.S)
    html2 = re.sub(r'<style.*?</style>', '', html2, flags=re.I|re.S)
    
    paragraphs = []
    for m in re.finditer(r'<p[^>]*>(.*?)</p>', html2, re.I|re.S):
        p = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if len(p) > 30:
            paragraphs.append(p)
    
    # Also try <article> tag
    art_match = re.search(r'<article[^>]*>(.*?)</article>', html2, re.I|re.S)
    if art_match:
        art_html = re.sub(r'<[^>]+>', ' ', art_match.group(1))
        art_sentences = [s.strip() for s in re.split(r'\.\s+', art_html) if len(s.strip()) > 40]
        paragraphs = art_sentences[:15] if len(art_sentences) > 15 else paragraphs
    
    print(f"TITLE: {title}")
    if desc:
        print(f"DESC: {desc}")
    print(f"PARAGRAPHS ({len(paragraphs)}):")
    for i, p in enumerate(paragraphs[:20]):
        print(f"  [{i}] {p[:300]}")

if __name__ == '__main__':
    extract(sys.argv[1])
