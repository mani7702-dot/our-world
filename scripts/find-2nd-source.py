#!/usr/bin/env python3
"""Look for inline 2nd source links inside the ScienceDaily article body, and grep Wikipedia for SIMP 0136."""
import re
html = open("/tmp/wild-weather-primary.html", encoding="utf-8", errors="ignore").read()
# Find links mentioning astronomy/astro/A&A / DOI / research / paper
links = re.findall(r'href="(https?://[^"]*(?:aanda|doi\.org|arxiv|researchgate|nature|science|trinity|astronomy)[^"]*)"', html, re.IGNORECASE)
print("=== inline research links in ScienceDaily ===")
for l in dict.fromkeys(links):
    print(l)
# Also check for DOI
dois = re.findall(r'(?:doi\.org/10\.[\w/.-]+|A&A\b|10\.\d{4,}/[\w/.-]+)', html)
print("=== DOIs / journal refs ===")
for d in dict.fromkeys(dois):
    print(d)
