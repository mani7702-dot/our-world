#!/usr/bin/env python3
import re
from html import unescape

html = open("/tmp/journal-page.html", encoding="utf-8", errors="ignore").read()
text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.S|re.I)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.S|re.I)
text = re.sub(r'<[^>]+>', ' ', text)
text = unescape(text)
text = re.sub(r'\s+', ' ', text)

# Find relevant sections
for kw in ["blueberry", "gut microbiome", "depress", "mood", "placebo", "randomized", "controlled trial", "flavonoid", "13", "participant"]:
    idx = text.lower().find(kw.lower())
    if idx >= 0:
        start = max(0, idx-80)
        end = min(len(text), idx+250)
        print(f"\n[{kw}] ...{text[start:end]}...")
