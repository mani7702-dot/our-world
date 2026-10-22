#!/usr/bin/env python3
import subprocess, re, sys
from html import unescape

URL = "https://www.sciencedaily.com/releases/2026/10/261017230028.htm"
UA = "Mozilla/5.0 (OurWorldSite crosscheck; contact andugulamani722@gmail.com)"

p = subprocess.run(["curl","-s","--compressed","--max-time","25","-A",UA,URL,"-o","/tmp/blueberry-article.html"],
                   capture_output=True)
print("downloaded, size:", p.stdout or "ok")

# Read and parse
html = open("/tmp/blueberry-article.html", encoding="utf-8", errors="ignore").read()
text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.S|re.I)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.S|re.I)
text = re.sub(r'<[^>]+>', ' ', text)
text = unescape(text)
text = re.sub(r'\s+', ' ', text)
# Find the article body - look for key phrases
# Print context around "blueberr" and "mood" and "depress"
for kw in ["blueberries", "mood", "depress", "older adult", "gut microbi", "placebo", "study", "doi", "journal", "university"]:
    idx = text.lower().find(kw)
    if idx >= 0:
        start = max(0, idx-100)
        end = min(len(text), idx+300)
        print(f"\n[{kw}] ...{text[start:end]}...")
