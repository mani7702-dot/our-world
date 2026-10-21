#!/usr/bin/env python3
"""Extract title, description, and body paragraphs from an HTML file."""
import re, sys

if len(sys.argv) < 2:
    print("Usage: python3 extract_info.py <file.html>")
    sys.exit(1)

with open(sys.argv[1], encoding="utf-8", errors="replace") as f:
    html = f.read()

title = re.findall(r'<title[^>]*>([^<]+)</title>', html, re.I)
print("TITLE:", title[0].strip() if title else "NONE")

desc = re.findall(r'<meta name="description"[^>]*content="([^"]+)"', html, re.I)
print("DESC:", desc[0][:500] if desc else "NONE")

para = re.findall(r'<p[^>]*>(.*?)</p>', html, re.S | re.I)
for i, p in enumerate(para):
    clean = re.sub(r'<[^>]+>', '', p).strip()
    if len(clean) > 50:
        print(f"PARA {i}:", clean[:300])
