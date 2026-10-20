# Daily news candidate picker for Our World. Prints recent headlines from
# verified genuine-source RSS feeds for a human to hand-pick 1-2 stories.
# Usage: python tools/fetch-news.py
# Feeds are trusted first-party outlets; we only read <title>/<link> text, so
# entity expansion can't reach our output -- skipped defusedxml on purpose.
import subprocess
import xml.etree.ElementTree as ET

UA = "Mozilla/5.0 (OurWorld daily picker; contact andugulamani722@gmail.com)"
FEEDS = [
    ("ScienceDaily", "https://www.sciencedaily.com/rss/top.xml"),
    ("Good News Network", "https://www.goodnewsnetwork.org/feed/"),
    ("BBC Science & Env", "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml"),
    ("Smithsonian Mag", "https://www.smithsonianmag.com/feed/"),
]
KEEP = ("coral", "whale", "dolphin", "turtle", "shark", "octopus", "bear", "orang", "bird",
        "space", "mars", "moon", "nasa", "asteroid", "star", "galaxy", "dinosaur", "fossil",
        "volcano", "insect", "animal", "elephant", "planet", "comet", "ocean", "robot")


def items(url):
    p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url],
                       capture_output=True, text=True)
    try:
        root = ET.fromstring(p.stdout)
    except ET.ParseError:
        return []
    out = []
    for it in root.iter("item"):
        t = (it.findtext("title") or "").strip()
        if not t or len(t) < 30:
            continue
        out.append((t, it.findtext("link") or ""))
    return out


for name, url in FEEDS:
    print(f"\n=== {name} ===")
    rows = items(url)
    picks = [r for r in rows if any(k in r[0].lower() for k in KEEP)]
    for t, link in (picks or rows)[:6]:
        print(f"  - {t}\n    {link}")
