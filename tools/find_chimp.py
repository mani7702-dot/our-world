#!/usr/bin/env python3
"""Find chimpanzee fishhooks article URL from ScienceDaily."""
import urllib.request

UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
# Search for chimpanzee fishhooks
url = "https://www.sciencedaily.com/search/?query=chimpanzee+fishhook&category=sciencemath"
req = urllib.request.Request(url, headers={"User-Agent": UA})
try:
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
    # Search for science daily release links
    import re
    links = re.findall(r'https://www\.sciencedaily\.com/releases/2026/\d+/[^\s"<>]+', html)
    for l in set(links):
        print(l)
    # Also search for chimpanzee mentions
    if "chimp" in html.lower():
        print("FOUND chimp mention in page")
    else:
        print("NO chimp mention found")
except Exception as e:
    print(f"ERR: {e}")
