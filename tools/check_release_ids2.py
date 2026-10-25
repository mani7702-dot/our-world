#!/usr/bin/env python3
"""Check release ID format in ScienceDaily URLs."""
import re, html, os, subprocess

os.chdir("/home/ubuntu/our-world")
url = "https://www.sciencedaily.com/rss/top.xml"
UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
p = subprocess.run(["curl", "-s", "-A", UA, url], capture_output=True)
data = p.stdout
idx = data.rfind(b"</rss>")
data = data[:idx + 6]

items = re.findall(rb"<item>(.*?)</item>", data, re.DOTALL)
for it in items[:3]:
    l = re.search(rb"<link>(.*?)</link>", it, re.DOTALL)
    if l:
        link = html.unescape(l.group(1).decode("utf-8", errors="replace").strip())
        print(f"Link: {link}")
        # Try to extract release ID
        m = re.search(r"/(\d{4}/\d{2}/\d{8})\.htm", link)
        if m:
            print(f"  Release path: {m.group(1)}")
