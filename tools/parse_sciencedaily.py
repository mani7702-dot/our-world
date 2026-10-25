#!/usr/bin/env python3
"""Parse ScienceDaily top.xml feed and list all items with title, link, pubDate."""
import urllib.request, xml.etree.ElementTree as ET

URL = "https://www.sciencedaily.com/rss/top.xml"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
req = urllib.request.Request(URL, headers={"User-Agent": UA})
data = urllib.request.urlopen(req, timeout=25).read()

# Strip trailing HTML comment after </rss>
idx = data.rfind(b"</rss>")
if idx >= 0:
    data = data[:idx + len(b"</rss>")]

root = ET.fromstring(data)
for it in root.iter("item"):
    title = (it.findtext("title") or "").strip()
    link = (it.findtext("link") or "").strip()
    pub = (it.findtext("pubDate") or "").strip()
    desc = (it.findtext("description") or "").strip()[:150]
    print(f"TITLE: {title}")
    print(f"  LINK: {link}")
    print(f"  PUB: {pub}")
    print(f"  DESC: {desc}")
    print()
