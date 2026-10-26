#!/usr/bin/env python3
"""Scan ScienceDaily astronomy section feeds for fresh candidates."""
import re, os, glob, json, urllib.request, xml.etree.ElementTree as ET

UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"

FEEDS = {
    "astronomy": "https://www.sciencedaily.com/rss/space_time/astronomy.xml",
    "solar_system": "https://www.sciencedaily.com/rss/space_time/solar_system.xml",
}

BLOCK = ("war", "attack", "death", "killed", "murder", "court", "lawsuit",
         "covid", "pandemic", "election", "politic", "terror", "bomb", "shooting",
         "cancer", "alzheimer", "parkinson", "diabetes", "ptsd",
         "blood pressure", "cannabis", "glioblastoma", "heart disease",
         "cholesterol", "statin", "colorectal", "ultra-processed", "alcohol",
         "fish oil", "clinical trial", "drug", "vaccine", "autism",
         "depression", "mental health", "dental", "implant")

def extract_existing_ids():
    ids = set()
    for f in glob.glob("/home/ubuntu/our-world/content/**/*.md", recursive=True):
        with open(f, errors="ignore") as fh:
            txt = fh.read()
        for m in re.finditer(r'/releases/(\d{4})/(\d{2})/(\d{12})\.htm', txt):
            ids.add(m.group(3))
    return ids

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        raw = urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "ignore")
    except Exception as e:
        print(f"  Fetch error for {url}: {e}")
        return None
    # Strip trailing comments
    raw = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
    return raw

existing_ids = extract_existing_ids()
print(f"Existing release IDs: {len(existing_ids)}\n")

fresh = []
for name, url in FEEDS.items():
    print(f"--- Fetching {name}: {url}")
    raw = fetch(url)
    if not raw:
        continue
    try:
        root = ET.fromstring(raw)
    except Exception as e:
        print(f"  Parse error: {e}")
        continue
    for it in root.iter("item"):
        title = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        desc = (it.findtext("description") or "").strip()[:200]
        m = re.search(r'/releases/(\d{4})/(\d{2})/(\d{12})\.htm', link)
        if not m:
            continue
        rid = m.group(3)
        if rid in existing_ids:
            continue
        low = (title + " " + desc).lower()
        if any(b in low for b in BLOCK):
            continue
        fresh.append({"title": title, "link": link, "desc": desc, "id": rid, "feed": name})

print(f"\n=== ALL fresh kid-safe candidates: {len(fresh)} ===")
for i, f in enumerate(fresh):
    print(f"[{i+1}] {f['title']}")
    print(f"    ID: {f['id']}  Feed: {f['feed']}")
    print(f"    URL: {f['link']}")
    print(f"    Desc: {f['desc']}")
    print()
