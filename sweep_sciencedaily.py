#!/usr/bin/env python3
"""Tirith-safe standalone sweep of ScienceDaily top.xml for explainers lane."""
import urllib.request, re, os

UA = "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"
url = "https://www.sciencedaily.com/rss/top.xml"

req = urllib.request.Request(url, headers={
    "User-Agent": UA,
    "Accept": "application/xml;q=0.9,*/*;q=0.8",
})
try:
    with urllib.request.urlopen(req, timeout=40) as resp:
        raw = resp.read()
        charset = resp.headers.get_content_charset() or "utf-8"
        text = raw.decode(charset, errors="replace")
except Exception as e:
    print(f"FETCH_ERROR: {e}")
    raise SystemExit(1)

# Strip trailing HTML comment after </rss> if present
text = re.sub(r'</rss>.*$', '</rss>', text, flags=re.DOTALL)

import xml.etree.ElementTree as ET
try:
    root = ET.fromstring(text)
except ET.ParseError as e:
    print(f"PARSE_ERROR: {e}")
    raise SystemExit(1)

items = []
for it in root.iter("item"):
    title = (it.findtext("title") or "").strip()
    link = (it.findtext("link") or "").strip()
    desc = (it.findtext("description") or "").strip()[:200]
    pub = (it.findtext("pubDate") or "").strip()
    if not title or not link or len(title) < 25:
        continue
    items.append({"title": title, "link": link, "desc": desc, "pubDate": pub})

print(f"Total items parsed: {len(items)}")
for i, it in enumerate(items[:30]):
    print(f"  [{i}] {it['pubDate']} | {it['title']}")
    print(f"      url: {it['link']}")
    if it['desc']:
        print(f"      desc: {it['desc'][:160]}")
