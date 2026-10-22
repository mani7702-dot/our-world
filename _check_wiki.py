#!/usr/bin/env python3
import subprocess, re
from html import unescape

UA = "Mozilla/5.0 (OurWorldSite crosscheck; contact andugulamani722@gmail.com)"

# Try Wikipedia "Gut-brain axis" as concept-level 2nd source
urls = {
    "wikipedia-gut-brain": "https://en.wikipedia.org/wiki/Gut%E2%80%93brain_axis",
    "wikipedia-blueberry": "https://en.wikipedia.org/wiki/Blueberry",
}

for name, url in urls.items():
    p = subprocess.run(["curl","-s","--compressed","--max-time","25","-A",UA,url,"-o",f"/tmp/{name}.html"],
                       capture_output=True)
    html = open(f"/tmp/{name}.html", encoding="utf-8", errors="ignore").read()
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.S|re.I)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.S|re.I)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = unescape(text)
    text = re.sub(r'\s+', ' ', text)

    # Find relevant content
    found = False
    for kw in ["gut-brain", "neurotransmitter", "serotonin", "flavonoid", "antioxidant", "polyphenol", "microbiome"]:
        idx = text.lower().find(kw.lower())
        if idx >= 0:
            start = max(0, idx-80)
            end = min(len(text), idx+300)
            print(f"\n[{name}/{kw}] ...{text[start:end]}...")
            found = True
    if not found:
        print(f"\n[{name}] No matches found, page size: {len(html)}")
