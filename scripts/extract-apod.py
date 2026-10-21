#!/usr/bin/env python3
"""Extract the real APOD article body from saved NASA HTML."""
from html.parser import HTMLParser
import re

html = open("/tmp/cassiopeia-apod.html", encoding="utf-8", errors="ignore").read()

# APOD image articles: find the description block. NASA image-article pages
# have an <h1> with the title, then a description div.
# Strip scripts/styles first.
clean = re.sub(r"<script.*?</script>", " ", html, flags=re.S|re.I)
clean = re.sub(r"<style.*?</style>", " ", clean, flags=re.S|re.I)
# Find the article body: NASA image-article has class "node-content" or article body
# Search for the title then capture following text until footer
m = re.search(r"<h1[^>]*>(.*?)</h1>", clean, re.S|re.I)
title = re.sub(r"<[^>]+>", " ", m.group(1)).strip() if m else "??"
print("TITLE:", title)

# The description text in APOD lives in <p> blocks after the image.
# Capture all <p> text and dedupe, looking for the long description.
paras = re.findall(r"<p[^>]*>(.*?)</p>", clean, re.S|re.I)
seen=set()
for p in paras:
    t = re.sub(r"<[^>]+>", " ", p).strip()
    t = re.sub(r"\s+", " ", t)
    if t and len(t) > 60 and t not in seen:
        seen.add(t)
        if any(k in t.lower() for k in ["ghost","cassiopeia","nebula","hydrogen","image","space","telescope","red","filter","light","star","region","cloud","emission","reflection"]):
            print("\n--- PARA ---")
            print(t[:600])
