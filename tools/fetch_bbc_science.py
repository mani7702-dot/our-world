#!/usr/bin/env python3
"""Fetch BBC Science & Environment RSS and list all items."""
import subprocess, re, html, json, os

os.chdir("/home/ubuntu/our-world")

URL = "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml"
UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"

p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, URL], capture_output=True)
data = p.stdout.decode("utf-8", errors="replace")

items = re.findall(r"<item>(.*?)</item>", data, re.DOTALL)
print(f"Total BBC Science items: {len(items)}")

for i, it in enumerate(items):
    t = re.search(r"<title>(.*?)</title>", it, re.DOTALL)
    l = re.search(r"<link>(.*?)</link>", it, re.DOTALL)
    d = re.search(r"<description>(.*?)</description>", it, re.DOTALL)
    pd = re.search(r"<pubDate>(.*?)</pubDate>", it, re.DOTALL)
    if t and l:
        title = html.unescape(t.group(1).strip())
        link = html.unescape(l.group(1).strip())
        desc = html.unescape(re.sub(r"<[^>]+>", "", d.group(1).strip() if d else "")).strip()
        date = html.unescape(pd.group(1).strip() if pd else "")
        print(f"\n[{i}] {title}")
        print(f"    date: {date}")
        print(f"    url:  {link}")
        print(f"    desc: {desc[:250]}")
