#!/usr/bin/env python3
"""Try different ScienceDaily category feed URLs."""
import urllib.request, xml.etree.ElementTree as ET, re, html, os

os.chdir("/home/ubuntu/our-world")
UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"

# Try various ScienceDaily category RSS URLs
urls = [
    "https://www.sciencedaily.com/news/space_telecom/",
    "https://www.sciencedaily.com/rss/space_telecom/index.xml",
    "https://www.sciencedaily.com/rss/top.xml",
    # Try Nature/Animals via different path
    "https://www.sciencedaily.com/rss/top_plants_animals.xml",
    # Try Earth/Environment
    "https://www.sciencedaily.com/rss/top_earth_climate.xml",
    # Try Space
    "https://www.sciencedaily.com/rss/top_space_telecom.xml",
    # Try Matter/Energy
    "https://www.sciencedaily.com/rss/top_matter_energy.xml",
    # Try Technology
    "https://www.sciencedaily.com/rss/top_technology.xml",
    # Try Computers
    "https://www.sciencedaily.com/rss/top_computers.xml",
    # Try Environment
    "https://www.sciencedaily.com/rss/top_environment.xml",
]

for url in urls:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        data = urllib.request.urlopen(req, timeout=20).read()
        # Check if it's XML
        if data[:5] == b"<?xml" or b"<rss" in data[:200]:
            idx = data.rfind(b"</rss>")
            if idx > 0:
                data = data[:idx + 6]
            root = ET.fromstring(data)
            count = len(list(root.iter("item")))
            print(f"\n{url}: {count} items")
            for it in root.iter("item"):
                t = (it.findtext("title") or "").strip()
                l = (it.findtext("link") or "").strip()
                print(f"  - {t}")
                print(f"    {l}")
        else:
            print(f"\n{url}: Not XML (HTML) - {len(data)} bytes")
    except Exception as e:
        print(f"\n{url}: ERROR - {e}")
