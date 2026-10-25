#!/usr/bin/env python3
"""Quick check specific fresh candidates for trending lane."""
import urllib.request, xml.etree.ElementTree as ET

UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
URL = "https://www.sciencedaily.com/rss/top.xml"

BLOCK = ("cancer", "alzheimer", "diabetes", "ptsd", "parkinson", "surgery",
         "covid", "death", "killed", "murder", "bomb", "shooting", "war",
         "attack", "tumor", "disease", "stroke", "heart attack", "risk",
         "depression", "anxiety", "autism", "inflammation", "arthritis",
         "opioid", "addiction", "obese", "overdose", "casualty", "fatal")

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
    low = t.lower()
    blocked = any(b in low for b in BLOCK)
    tag = "BLOCKED" if blocked else "ok"
    print(f"[{tag}] {t}")
    print(f"  url: {link}")
