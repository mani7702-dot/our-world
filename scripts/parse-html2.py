#!/usr/bin/env python3
"""Extract text content from a saved HTML file for fact-checking."""
import re, sys, html as htmllib
raw = open(sys.argv[1], encoding='utf-8', errors='ignore').read()
# Get title
title_m = re.search(r'<title>(.*?)</title>', raw, re.I|re.S)
title = title_m.group(1).strip() if title_m else "UNKNOWN"
print(f"TITLE: {title}")
# Remove script/style
text = re.sub(r'<script[^>]*>.*?</script>', '', raw, flags=re.S|re.I)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.S|re.I)
# Get paragraphs and headers
paras = re.findall(r'<(p|h[1-6])[^>]*>(.*?)</\1>', text, re.S|re.I)
for tag, p in paras:
    clean = re.sub(r'<[^>]+>', '', p)
    clean = htmllib.unescape(clean).strip()
    if len(clean) > 30:
        print(f'\n--- {clean[:600]}')
