#!/usr/bin/env python3
"""Fetch ScienceDaily homepage and extract article links with broader pattern."""
import urllib.request, re, html, os

os.chdir("/home/ubuntu/our-world")

URL = "https://www.sciencedaily.com/news/top/"
UA = "Mozilla/5.0 (compatible: OurWorldBot; contact andugulamani722@gmail.com)"

req = urllib.request.Request(URL, headers={"User-Agent": UA})
data = urllib.request.urlopen(req, timeout=25).read().decode("utf-8", errors="replace")

# Try broader patterns
links1 = re.findall(r'href="(/releases/\d{4}/\d{2}/\d{8}\.htm)"', data)
links2 = re.findall(r'href="(https://www\.sciencedaily\.com/releases/\d{4}/\d{2}/\d{8}\.htm)"', data)
links3 = re.findall(r'href="(/news/\w+/\d+\.html)"', data)
links4 = re.findall(r'href="(/releases/[^"]+)"', data)
links5 = re.findall(r'href="(https://www\.sciencedaily\.com/releases/[^"]+)"', data)

all_links = list(dict.fromkeys(links1 + links2 + links3 + links4 + links5))
print(f"Pattern 1 (releases): {len(links1)}")
print(f"Pattern 3 (news): {len(links3)}")
print(f"Pattern 4 (all releases): {len(links4)}")
print(f"Total unique: {len(all_links)}")

for l in all_links[:50]:
    print(l)

# Show a snippet of the body to understand the HTML structure
print("\n--- Looking for article snippets in body ---")
# Find text between known patterns
body_start = data.find("<body")
body_end = data.find("</body>")
body = data[body_start:body_end] if body_start > 0 else data[:3000]
# Find all href links containing 'releases'
all_href = re.findall(r'href="([^"]*releases[^"]*)"', data)
all_href = list(dict.fromkeys(all_href))
print(f"All href links with 'releases': {len(all_href)}")
for h in all_href[:30]:
    print(h)
