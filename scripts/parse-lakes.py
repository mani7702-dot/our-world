#!/usr/bin/env python3
"""Parse lake names from saved Listverse HTML. File-based (Tirith-safe)."""
import re
html = open("/tmp/lakes-article.html", encoding="utf-8").read()
headers = re.findall(r'<h[23][^>]*>(.*?)</h[23]>', html, re.S)
for h in headers:
    t = re.sub(r'<[^>]+>', '', h).strip()
    if t and len(t) < 80:
        print(t)
print("=== PARAGRAPHS ===")
paras = re.findall(r'<p[^>]*>(.*?)</p>', html, re.S)
for i, p in enumerate(paras):
    t = re.sub(r'<[^>]+>', '', p).strip()
    t = re.sub(r'\s+', ' ', t)
    if t and len(t) > 40:
        print(f"[{i}] {t[:300]}")
