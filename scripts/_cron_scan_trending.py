#!/usr/bin/env python3
"""Cron IP safe: file-based ElementTree walk of Smithsonian history RSS + SD top.
Prints every title+URL so we can eyeball fresh, kid-safe, trending-eligible candidates.
Never: curl|python3 -c (Tirith blocks), never backslash-heavy inline bodies."""
import subprocess, sys, os, xml.etree.ElementTree as ET, re

UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
FEEDS = [
    ("Smithsonian history", "https://www.smithsonianmag.com/rss/history/"),
    ("ScienceDaily top", "https://www.sciencedaily.com/rss/top.xml"),
]

def fetch(url):
    p = subprocess.run(["curl","-s","--compressed","--max-time","25","-A",UA,url],
                       capture_output=True)
    data = p.stdout
    if data[:2] == b"\x1f\x8b":
        import gzip; data = gzip.decompress(data)
    return data

def parse(data, label):
    try:
        root = ET.fromstring(data)
    except ET.ParseError:
        print(f"[{label}] parse error"); return
    for it in root.iter("item"):
        t = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        desc = (it.findtext("description") or "").strip()[:200]
        print(f"[{label}] {t}")
        print(f"  url: {link}")
        if desc:
            print(f"  desc: {desc}")

def main():
    for label, url in FEEDS:
        data = fetch(url)
        print(f"=== {label} ({len(data)} bytes) ===")
        parse(data, label)

if __name__ == "__main__":
    main()
