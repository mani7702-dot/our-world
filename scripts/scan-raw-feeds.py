#!/usr/bin/env python3
"""Tirith-safe: parse a saved RSS XML file and print all titles/links/descs."""
import sys, re

xml = open(sys.argv[1], encoding="utf-8", errors="replace").read()
items = re.findall(r"<item[^>]*>(.*?)</item>", xml, re.S | re.I)
for it in items:
    t = re.search(r"<title[^>]*>(.*?)</title>", it, re.S | re.I)
    l = re.search(r"<link[^>]*>(.*?)</link>", it, re.S | re.I)
    d = re.search(r"<description[^>]*>(.*?)</description>", it, re.S | re.I)
    title = t.group(1).strip() if t else ""
    link = l.group(1).strip() if l else ""
    desc = d.group(1).strip()[:200] if d else ""
    if len(title) >= 25:
        print(f"TITLE: {title}")
        print(f"URL: {link}")
        print(f"DESC: {desc}")
        print("---")
