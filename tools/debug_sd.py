#!/usr/bin/env python3
"""Debug: Check ScienceDaily homepage access."""
import urllib.request, re, html, os

os.chdir("/home/ubuntu/our-world")

URL = "https://www.sciencedaily.com/news/top/"
UA = "Mozilla/5.0 (compatible: OurWorldBot; contact andugulamani722@gmail.com)"

req = urllib.request.Request(URL, headers={"User-Agent": UA})
data = urllib.request.urlopen(req, timeout=25).read().decode("utf-8", errors="replace")

print("Page length:", len(data))
title_match = re.search(r"<title>(.*?)</title>", data)
if title_match:
    print("Title:", html.unescape(title_match.group(1)))

if "challenge" in data.lower() or "cloudflare" in data.lower():
    print("Page appears to be Cloudflare-challenged")
else:
    # Find all links with 'releases' pattern
    links = re.findall(r'href="([^"]*releases/\d{4}/\d{2}/\d{8}\.htm[^"]*)"', data)
    links = list(dict.fromkeys(links))
    print(f"Found {len(links)} release links")
    for l in links[:20]:
        print(l)
