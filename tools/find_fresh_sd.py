#!/usr/bin/env python3
"""Try to find truly fresh ScienceDaily articles."""
import urllib.request, re, html, os, subprocess, json
import xml.etree.ElementTree as ET

os.chdir("/home/ubuntu/our-world")
UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"

# Check what dates are in the RSS
p = subprocess.run(["curl", "-s", "-A", UA, "https://www.sciencedaily.com/rss/top.xml"], capture_output=True)
data = p.stdout
idx = data.rfind(b"</rss>")
data = data[:idx + 6]
root = ET.fromstring(data)

dates = []
for it in root.iter("item"):
    pd = (it.findtext("pubDate") or "").strip()
    if pd:
        dates.append(pd)

print(f"PubDate range: {min(dates)} to {max(dates)}")
print(f"Total items: {len(dates)}")

# Try fetching ScienceDaily section pages
urls_to_try = [
    "https://www.sciencedaily.com/news/matter_energy/",
    "https://www.sciencedaily.com/news/space_telecom/",
    "https://www.sciencedaily.com/news/earth_climate/",
    "https://www.sciencedaily.com/news/plants_animals/",
    "https://www.sciencedaily.com/news/health_mind/",
    "https://www.sciencedaily.com/news/technology_computing/",
    "https://www.sciencedaily.com/news/earth_climate/earth_science/",
    "https://www.sciencedaily.com/news/matter_energy/electronics/",
]

for url in urls_to_try:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        resp = urllib.request.urlopen(req, timeout=20)
        page_data = resp.read().decode("utf-8", errors="replace")
        links = re.findall(r'href="(/releases/\d{4}/\d{2}/\d{14}\.htm)"', page_data)
        links = list(dict.fromkeys(links))
        if links:
            print(f"\n{url}: {len(links)} article links")
            for l in links[:5]:
                full = "https://www.sciencedaily.com" + l
                # Try to get title
                try:
                    req2 = urllib.request.Request(full, headers={"User-Agent": UA})
                    art = urllib.request.urlopen(req2, timeout=15).read().decode("utf-8", errors="replace")
                    t = re.search(r"<title>(.*?)</title>", art)
                    title = html.unescape(t.group(1).strip()).replace(" -- ScienceDaily", "") if t else "No title"
                    print(f"  {title}")
                    print(f"  {full}")
                except:
                    print(f"  {full}")
        else:
            print(f"\n{url}: No release links found (len={len(page_data)})")
    except Exception as e:
        print(f"\n{url}: ERROR - {e}")
