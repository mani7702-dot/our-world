#!/usr/bin/env python3
import subprocess

UA = "Mozilla/5.0 (OurWorldSite crosscheck; contact andugulamani722@gmail.com)"

# Try the journal page - but it's likely paywalled. Instead, let's save the SD article HTML
# and search for any embedded journal/2nd source links

p = subprocess.run(["curl","-s","--compressed","--max-time","25","-A",UA,
    "https://www.ncbi.nlm.nih.gov/doi/10.1016/j.jnha.2026.100958"],
    capture_output=True)
import os
with open("/tmp/journal-page.html","wb") as f:
    f.write(p.stdout)
print("journal page size:", len(p.stdout))

# Check if journal page is accessible
if len(p.stdout) > 500:
    import re
    text = re.sub(r'<[^>]+>', ' ', p.stdout.decode("utf-8","ignore"))
    text = re.sub(r'\s+', ' ', text).lower()
    for kw in ["blueberry","gut microbiome","depress","mood","dietary flavonoid","placebo","randomized","controlled"]:
        idx = text.find(kw)
        if idx >= 0:
            print(f"\n[{kw}] ...{text[max(0,idx-50):idx+150]}...")
