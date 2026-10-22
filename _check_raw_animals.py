#!/usr/bin/env python3
"""Parse raw animals RSS feeds, run abort pass: dup grep (literal + stable tokens) + MED/POL/BLOCK guardrails."""
import xml.etree.ElementTree as ET, os, re

FEEDS = {
    "GNN": "/tmp/gnn.xml",
    "SD-animals": "/tmp/sd_animals.xml",
    "BBC-earth": "/tmp/bbc_earth.xml",
}

BLOCKWORDS = ("war", "attack", "death toll", "killed", "murder", "court", "lawsuit", "covid",
              "pandemic", "election", "politic", "terror", "bomb", "shooting",
              "military", "conflict", "invasion", "terrorism", "siege", "strike dead")

# Content dirs for dup check
DIRS = ["content/blog", "content/news"]

def grep_dup(title):
    hits = []
    safe = re.sub(r'[^a-zA-Z0-9 ]', ' ', title.lower())
    words = [w for w in safe.split() if len(w) >= 5]
    for d in DIRS:
        if not os.path.isdir(d):
            continue
        for f in os.listdir(d):
            if not f.endswith(".md"):
                continue
            fp = os.path.join(d, f)
            try:
                txt = open(fp, encoding="utf-8", errors="ignore").read()
                tl = txt.lower()
            except Exception:
                continue
            # literal title match
            if title.lower() in tl[:500]:
                hits.append((fp, "TITLE-MATCH"))
                continue
            # stable token grep (3+ stable tokens)
            mc = sum(1 for w in words if w in tl)
            if mc >= 3:
                hits.append((fp, f"tokens={mc}"))
    return hits

def parse(path):
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError:
        return []
    items = []
    for it in root.iter("item"):
        t = (it.findtext("title") or "").strip()
        if len(t) < 25:
            continue
        items.append({"title": t,
                      "link": (it.findtext("link") or "").strip(),
                      "desc": (it.findtext("description") or "").strip()[:220]})
    return items

def main():
    all_items = []
    for label, path in FEEDS.items():
        if not os.path.exists(path) or os.path.getsize(path) < 500:
            print(f"  SKIP {label}: too small or error")
            continue
        items = parse(path)
        print(f"  {label}: {len(items)} items")
        all_items += items

    # Dedupe across feeds
    seen = set()
    uniq = []
    for it in all_items:
        key = it["title"].lower()
        if key in seen:
            continue
        seen.add(key)
        uniq.append(it)

    print(f"\nUnique items: {len(uniq)}")
    fresh = []
    for it in uniq:
        t = it["title"]
        tl = t.lower()
        # BLOCK guardrail
        if any(b in tl for b in BLOCKWORDS):
            print(f"  BLOCK: {t}")
            continue
        # MED guardrail
        if any(m in tl for m in ["cancer", "disease", "treatment", "therapy", "diagnos", "mental disorder", "depression", "anxiety", "poisoning", "medical mystery", "patient"]):
            print(f"  MED-BLOCK: {t}")
            continue
        # POL guardrail
        if any(p in tl for p in ["trump", "biden", "election", "government", "politic", "leadership", "court", "lawsuit", "treason", "charged", "prosecutor", "minister"]):
            print(f"  POL-BLOCK: {t}")
            continue
        # dup check
        d = grep_dup(t)
        if d:
            print(f"  DUP: {t} -> {d[:2]}")
            continue
        fresh.append(it)

    print(f"\n=== FRESH candidates: {len(fresh)} ===")
    for it in fresh:
        print(f"  {it['title']}")
        print(f"    url: {it['link']}")
        print(f"    desc: {it['desc']}")
        print()

if __name__ == "__main__":
    main()
