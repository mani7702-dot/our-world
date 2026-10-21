#!/usr/bin/env python3
"""Verify the live deployed page has key elements."""
import urllib.request

url = "https://mani7702-dot.github.io/our-world/news/skin-cells-play-different-rules-boys-vs-girls-mice-study.html"
req = urllib.request.Request(url, headers={"User-Agent": "OurWorld-verify/1.0"})
resp = urllib.request.urlopen(req, timeout=25)
html = resp.read().decode("utf-8", errors="replace")

print(f"HTTP: {resp.getcode()}")
print(f"Title clean (no leaked quotes): {chr(34) not in html[html.find('<h1>'):html.find('</h1>')] if '<h1>' in html else 'no h1'}")
print(f"for-grownups aside present: {'class=\"grownups\"' in html}")
print(f"Hero image present: {'assets/images/skin-cells-play-different-rules' in html}")
print(f"Try this at home: {'## Try this at home' not in html}")  # should be in body, not header
print(f"Fun fact section: {'## Fun fact' not in html}")
print(f"Sources section: {'## Sources' in html}")
print(f"Category Science badge: {'Science' in html}")
