#!/usr/bin/env python3
"""Fetch ScienceDaily top.xml fallback for science lane."""
import urllib.request, xml.etree.ElementTree as ET, re, json, os

UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
URL = "https://www.sciencedaily.com/rss/top.xml"

os.chdir("/home/ubuntu/our-world")

req = urllib.request.Request(URL, headers={"User-Agent": UA})
with urllib.request.urlopen(req, timeout=25) as resp:
    data = resp.read()

# Strip trailing HTML comment after </rss>
idx = data.rfind(b"</rss>")
if idx >= 0:
    data = data[:idx + len(b"</rss>")]

root = ET.fromstring(data)

BLOCK_KW = ("cancer", "alzheimer", "covid", "pandemic", "surgery", "treatment",
            "disease", "death", "dying", "depression", "anxiety", "autism spectrum",
            "heart attack", "stroke", "opioid", "addiction", "overdose", "brain damage",
            "mental health", "psychological", "suicide", "brain cancer", "lung cancer",
            "breast cancer", "colon cancer", "diabetes", "obesity", "weight loss",
            "diet pill", "blood pressure", "cholesterol", "inflammatory", "immune system",
            "COVID-19", "coronavirus", "vaccine", "vaccination", "clinical trial")

items = []
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    link = (it.findtext("link") or "").strip()
    desc = (it.findtext("description") or "").strip()[:300]
    low = t.lower()
    if any(b in low for b in [b.lower() for b in BLOCK_KW]):
        continue
    if "weather" in low or "storm" in low or "climate" in low:
        continue
    items.append({"title": t, "link": link, "desc": desc})

print(json.dumps(items, indent=2))
