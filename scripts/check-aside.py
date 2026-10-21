#!/usr/bin/env python3
"""Verify for-grownups aside renders with content."""
import re, sys

with open(sys.argv[1]) as f:
    html = f.read()

m = re.search(r'<aside class="grownups"[^>]*>(.*?)</aside>', html, re.S)
if m:
    content = m.group(1).strip()
    print(f"Aside content length: {len(content)}")
    print(f"Aside content: {content[:300]}")
    if len(content) < 10:
        print("ERROR: Empty aside!")
    else:
        print("OK: aside has content")
else:
    print("ERROR: No aside found")
