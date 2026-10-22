#!/usr/bin/env python3
import re
with open('/tmp/nasa_cyclone.html') as f:
    content = f.read()

# Find all paragraphs
paras = re.findall(r'<p[^>]*>(.*?)</p>', content, re.DOTALL)
print(f"Found {len(paras)} paragraphs")
for i, p in enumerate(paras):
    clean = re.sub(r'<[^>]+>', ' ', p)
    clean = re.sub(r'\s+', ' ', clean).strip()
    if len(clean) > 20:
        print(f"[{i}] {clean[:300]}")
        print()
