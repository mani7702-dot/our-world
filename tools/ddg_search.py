#!/usr/bin/env python3
# Second source for cross-check via DuckDuckGo HTML search -> Jina proxy each result.
import subprocess, re, urllib.parse
UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
q = "Sunrise-III SCIP magnetic fields chromosphere Sun balloon observatory NAOJ 2024"
url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(q)
r = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, url], capture_output=True, text=True)
txt = r.stdout
# links to result articles
for m in re.findall(r'result__a" href="(.*?)"', txt):
    real = m
    if real.startswith("//"):
        real = "https:" + real
    # DDG redirects through /l/?uddg=...
    if "/l/?" in real:
        mm = re.search(r"uddg=([^&]+)", real)
        if mm:
            real = urllib.parse.unquote(mm.group(1))
    print(real)
