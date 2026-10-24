#!/usr/bin/env python3
# Print full Jina text for the article (no truncation).
import subprocess, sys
UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
def jina(url):
    proxy = "https://r.jina.ai/" + url
    r = subprocess.run(["curl", "-s", "--max-time", "60", "-A", UA, proxy],
                       capture_output=True, text=True)
    return r.stdout
for url in sys.argv[1:]:
    txt = jina(url)
    print("URL:", url, "len:", len(txt))
    print(txt)
