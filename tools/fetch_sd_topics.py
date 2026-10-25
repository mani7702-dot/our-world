#!/usr/bin/env python3
"""Try topic-specific ScienceDaily feeds for fresh content."""
import urllib.request, xml.etree.ElementTree as ET, re, html, os

os.chdir("/home/ubuntu/our-world")
UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"

feeds = [
    ("Space", "https://www.sciencedaily.com/news/space_telecom/index.xml"),
    ("Earth/Climate", "https://www.sciencedaily.com/news/earth_climate/index.xml"),
    ("Tech/Computers", "https://www.sciencedaily.com/news/matter_energy/computers/index.xml"),
    ("Nature/Animals", "https://www.sciencedaily.com/news/plants_animals/index.xml"),
    ("Health/Medicine", "https://www.sciencedaily.com/news/health_mind/index.xml"),
    ("Plants/Animals", "https://www.sciencedaily.com/news/plants_animals/plants/index.xml"),
]

for name, url in feeds:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        data = urllib.request.urlopen(req, timeout=20).read()
        idx = data.rfind(b"</rss>")
        if idx > 0:
            data = data[:idx + 6]
        root = ET.fromstring(data)
        count = len(list(root.iter("item")))
        print(f"\n{name} ({url}): {count} items")
        for it in root.iter("item"):
            t = (it.findtext("title") or "").strip()
            print(f"  - {t}")
    except Exception as e:
        print(f"\n{name} ({url}): ERROR - {e}")
        # Check if it's an HTML page instead of XML
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            data = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", errors="replace")[:200]
            print(f"  Content: {data[:200]}")
        except:
            pass
