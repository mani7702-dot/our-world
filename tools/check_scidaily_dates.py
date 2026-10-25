#!/usr/bin/env python3
"""Try to get truly fresh ScienceDaily articles by checking the top.xml feed again.
Also try the ScienceDaily news/latest page."""
import urllib.request, xml.etree.ElementTree as ET, re, os

UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"

existing_files = []
for f in os.listdir("/home/ubuntu/our-world/content/news"):
    if f.endswith(".md"):
        path = os.path.join("/home/ubuntu/our-world/content/news", f)
        with open(path) as fh:
            existing_files.append(fh.read().lower())

BLOCK = ("cancer", "alzheimer", "diabetes", "ptsd", "parkinson", "surgery",
         "covid", "death", "killed", "murder", "bomb", "shooting", "war",
         "attack", "tumor", "disease", "stroke", "heart attack", "risk",
         "depression", "anxiety", "autism", "inflammation", "arthritis",
         "opioid", "addiction", "overdose", "casualty", "fatal",
         "brain cancer", "lung cancer", "colorectal")

# Try fetching ScienceDaily news page and extract release links
url = "https://www.sciencedaily.com/news/top/"
req = urllib.request.Request(url, headers={"User-Agent": UA})
try:
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
    # Extract all release links
    links = re.findall(r'href="(/releases/2026/\d{2}/\d{8}\.htm)"', html)
    full_urls = set("https://www.sciencedaily.com" + l for l in links)
    print(f"Found {len(full_urls)} release links from top page")
    
    # Extract titles for each
    for fu in sorted(full_urls)[:20]:
        m = re.search(r'/releases/2026/(\d{2})/(\d{8})', fu)
        if m:
            date_str = f"2026-{m.group(1)}-{m.group(2)[6:8]}"
            print(f"  [{date_str}] {fu}")
except Exception as e:
    print(f"ERR: {e}")

# Also try the RSS feed one more time and check all dates
print("\n=== Top.xml item dates ===")
URL = "https://www.sciencedaily.com/rss/top.xml"
req = urllib.request.Request(URL, headers={"User-Agent": UA})
raw = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
idx = raw.rfind("</rss>")
if idx != -1:
    raw = raw[:idx + 6]
root = ET.fromstring(raw)
items = list(root.iter("item"))
for it in items:
    t = (it.findtext("title") or "").strip()
    link = (it.findtext("link") or "").strip()
    m = re.search(r'/releases/2026/(\d{2})/(\d{8})', link)
    if m:
        date_str = f"2026-{m.group(1)}-{m.group(2)[6:8]}"
        print(f"  [{date_str}] {t[:50]}")
