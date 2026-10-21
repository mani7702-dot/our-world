#!/usr/bin/env python3
"""Search Wikipedia and NASA for AutoNav confirmation - second source check."""
import re, sys
paths = [p for p in sys.argv[1:]]
terms = ['AutoNav', 'autonomous navigation', 'guinness', 'tilt limit', 'cross-slope', 'ingenuity base station', 'bit flip']
for path in paths:
    print(f"=== {path} ===")
    html = open(path).read()
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.S)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.S)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    for term in terms:
        idx = text.lower().find(term.lower())
        if idx >= 0:
            print(f"  '{term}' at {idx}: ...{text[idx-100:idx+200].strip()}...")
        else:
            print(f"  '{term}': NOT FOUND")
