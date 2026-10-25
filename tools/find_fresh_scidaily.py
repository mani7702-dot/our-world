#!/usr/bin/env python3
"""Try ScienceDaily recent articles pages for fresh trending content."""
import urllib.request, re, os

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

# Try ScienceDaily main news page
urls_to_try = [
    "https://www.sciencedaily.com/news/top/",
    "https://www.sciencedaily.com/news/most_popular/",
]

for url in urls_to_try:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
        # Find article links
        links = re.findall(r'href="(/releases/2026/\d{2}/\d{8}\.htm)"', html)
        titles = re.findall(r'<h[123][^>]*>(.*?)</h[123]>', html, re.DOTALL)
        print(f"\n=== {url} ===")
        print(f"Found {len(links)} release links")
        # Extract full article URLs and titles
        full_urls = set()
        for l in links:
            full_urls.add("https://www.sciencedaily.com" + l)
        for fu in sorted(full_urls)[:15]:
            print(f"  {fu}")
    except Exception as e:
        print(f"  {url}: ERR: {e}")
