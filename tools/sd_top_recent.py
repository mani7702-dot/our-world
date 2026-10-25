#!/usr/bin/env python3
"""Fetch ScienceDaily top.xml and list ALL items with dates, showing most recent first."""
import urllib.request, xml.etree.ElementTree as ET, re, html

os_chdir = True
import os
os.chdir("/home/ubuntu/our-world")

URL = "https://www.sciencedaily.com/rss/top.xml"
UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"

req = urllib.request.Request(URL, headers={"User-Agent": UA})
data = urllib.request.urlopen(req, timeout=25).read()
idx = data.rfind(b"</rss>")
data = data[:idx + 6]
root = ET.fromstring(data)

items = []
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    l = (it.findtext("link") or "").strip()
    d = (it.findtext("description") or "").strip()
    d = re.sub(r"<[^>]+>", "", d).strip()
    d = html.unescape(d)
    pd = it.findtext("pubDate") or ""
    items.append({"title": t, "link": l, "desc": d[:300], "date": pd})

items.sort(key=lambda x: x["date"], reverse=True)
print(f"Total items: {len(items)}")
for i, it in enumerate(items[:20]):
    print(f"\n[{i}] {it['title']}")
    print(f"    date: {it['date']}")
    print(f"    url:  {it['link']}")
    print(f"    desc: {it['desc'][:200]}")
