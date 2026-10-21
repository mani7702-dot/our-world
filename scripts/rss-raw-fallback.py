# Tirith-safe raw RSS fallback: download feed to a file, parse with stdlib ElementTree.
# Usage: python3 scripts/rss-raw-fallback.py --category science --out /tmp/raw-candidates.tsv
# Prints all titles; caller applies dupe + guardrails.
import argparse, subprocess, sys, os, xml.etree.ElementTree as ET

UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"

FEEDS = {
    "trending": [
        ("Reddit TIL", "https://old.reddit.com/r/todayilearned/top/.rss"),
        ("NPR Trending", "https://www.npr.com/rss/rss.jsf?id=1001"),
        ("Listverse", "https://listverse.com/feed/"),
        ("Mental Floss", "https://mentalfloss.com/feeds/latest"),
    ],
    "science": [
        ("ScienceDaily top", "https://www.sciencedaily.com/rss/top.xml"),
        ("BBC Science & Env", "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml"),
        ("Smithsonian", "https://www.smithsonianmag.com/feed/"),
    ],
}

def fetch(url):
    p = subprocess.run(["curl", "-s", "--compressed", "--max-time", "25", "-A", UA, url],
                       capture_output=True, text=True)
    return p.stdout

def parse(xml):
    try:
        root = ET.fromstring(xml)
    except ET.ParseError:
        return []
    out = []
    for it in root.iter("item"):
        t = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        desc = (it.findtext("description") or "").strip()[:200]
        if t and len(t) >= 25:
            out.append((t, link, desc))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--category", required=True, choices=list(FEEDS))
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    rows = []
    for label, url in FEEDS[a.category]:
        rows += parse(fetch(url))
    lines = ["\t".join(r) for r in rows]
    text = "\n".join(lines)
    print(text)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(text + "\n")

if __name__ == "__main__":
    main()
