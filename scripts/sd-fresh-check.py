#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sd-fresh-check.py — Fetch the raw ScienceDaily top.xml and dump ALL items
with their URLs (no filtering) so we can see if there are truly fresh stories
or if everything is recirculated.
"""
import subprocess, xml.etree.ElementTree as ET, re, os, sys, json
from datetime import datetime, timezone

UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
FEED = "https://www.sciencedaily.com/rss/top.xml"

def fetch(url):
    p = subprocess.run(["curl", "-s", "-L", "--max-time", "30", "-A", UA, url],
                       capture_output=True)
    data = p.stdout
    if data[:2] == b"\x1f\x8b":
        import gzip
        data = gzip.decompress(data)
    text = data.decode("utf-8", "replace")
    idx = text.find("</rss>")
    if idx != -1:
        text = text[:idx + len("</rss>")]
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    return text

# Get today's date
today = datetime.now().strftime("%Y-%m-%d")
print(f"Today: {today}")

# Check top.xml
text = fetch(FEED)
try:
    root = ET.fromstring(text)
except ET.ParseError as e:
    print(f"PARSE ERROR: {e}")
    sys.exit(1)

items = root.findall(".//item")
print(f"\n=== top.xml: {len(items)} items ===")
for it in items[:40]:
    title = (it.findtext("title") or "").strip()
    link = (it.findtext("link") or "").strip()
    desc = (it.findtext("description") or "").strip()
    desc = re.sub(r"<[^>]+>", "", desc).strip()[:120]
    # extract date from URL
    m = re.search(r'releases/(\d{4})/(\d{2})/(\d{2})', link)
    date_str = f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else "?"
    is_today = "TODAY" if date_str == today else ""
    print(f"  [{date_str}] {is_today} {title[:70]} | {link[:60]}")

# Also check other ScienceDaily RSS feeds for fresh content
print("\n=== Trying ScienceDaily topic feeds ===")
# Try the earth science and environment feeds
for label, feed_url in [
    ("SD earth", "https://www.sciencedaily.com/news/earth_climate/index.xml"),
    ("SD environment", "https://www.sciencedaily.com/news/earth_climate/environment/index.xml"),
    ("SD animals", "https://www.sciencedaily.com/news/plants_animals/animals/index.xml"),
    ("SD plants", "https://www.sciencedaily.com/news/plants_animals/plants/index.xml"),
    ("SD matter energy", "https://www.sciencedaily.com/news/matter_energy/index.xml"),
]:
    try:
        t = fetch(feed_url)
        r = ET.fromstring(t)
        its = r.findall(".//item")
        print(f"\n{label}: {len(its)} items")
        for it in its[:10]:
            title = (it.findtext("title") or "").strip()
            link = (it.findtext("link") or "").strip()
            m = re.search(r'releases/(\d{4})/(\d{2})/(\d{2})', link)
            date_str = f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else "?"
            is_today = "TODAY" if date_str == today else ""
            print(f"  [{date_str}] {is_today} {title[:70]} | {link[:60]}")
    except Exception as e:
        print(f"  {label}: ERROR {e}")
