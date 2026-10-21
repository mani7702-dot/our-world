#!/usr/bin/env python3
"""Tirith-safe dupe guard: checks a list of candidate headlines against content/blog + content/news."""
import xml.etree.ElementTree as ET
import re, os

candidates = [
    "Scientists discover a surprising twist in Japan's 7,300-year-old volcanic apocalypse",
    "NASA\u2019s Webb reveals the wild weather of a mysterious world 20 light-years away",
    "This bird flies thousands of miles, but its wings have a catch",
    "NASA\u2019s SpaceX launch lights up the sky with a giant glowing jellyfish",
    "NASA discovers hidden fires burning beneath the Amazon rainforest",
    "The uranium cubes that exposed Nazi Germany\u2019s nuclear failure",
    "\u201cCrawzilla\u201d was huge. Then scientists found an even bigger crayfish",
    "Scientists win 2026 Nobel Prize for controlling brain cells with light",
    "Scientists discover how deep sleep builds muscle, burns fat, and boosts the brain",
    "Astronomers discover a ghostly green star unlike any known before",
    "Scientists link a strange sugar in red meat to a 63% higher diabetes risk",
]

def grep_dup(title):
    safe = re.sub(r'[^a-zA-Z0-9 ]', ' ', title.lower())
    tokens = [w for w in safe.split() if len(w) >= 5]
    hits = []
    for d in ("content/blog", "content/news"):
        if not os.path.isdir(d):
            continue
        for f in os.listdir(d):
            if not f.endswith(".md"):
                continue
            fp = os.path.join(d, f)
            txt = open(fp, encoding="utf-8", errors="ignore").read().lower()
            if title.lower()[:60] in open(fp, encoding="utf-8", errors="ignore").read()[:600].lower():
                hits.append(f"{d}/{f}")
    return hits

for t in candidates:
    h = grep_dup(t)
    status = "DUP" if h else "FRESH"
    print(f"[{status}] {t} -> {h}")
