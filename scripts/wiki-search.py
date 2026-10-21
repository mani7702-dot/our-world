#!/usr/bin/env python3
"""Search Wikipedia Perseverance rover article for AutoNav/drive/distance confirmation."""
import re, sys
html = open(sys.argv[1]).read()
text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.S)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.S)
text = re.sub(r'<[^>]+>', ' ', text)
text = re.sub(r'\s+', ' ', text)
for term in ['AutoNav', 'autonomous navigation', 'autonomous', 'record', 'distance', 'Guinness', 'radiation-hardened']:
    idx = text.lower().find(term.lower())
    if idx >= 0:
        print(f"=== {term} found at {idx} ===")
        print(text[idx-150:idx+250].strip())
        print()
