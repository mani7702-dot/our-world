# -*- coding: utf-8 -*-
# Per-category candidate picker for Our World multi-agent news pipeline.
# Usage: python3 tools/fetch-news.py --category <space|science|animals|world|history|explainers|listicles|trending|all> --count 6
# Pulls headline + URL + snippet per item so each lane agent can pick + cross-check.
# Feeds are trusted first-party outlets; we ONLY read <title>/<link>/<description> text,
# so entity expansion cannot reach any consumer -- stdlib ET is safe here (no defusedxml needed).
import subprocess, argparse, xml.etree.ElementTree as ET

UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"

CATEGORIES = {
    "space": [("NASA Image + Videos", "https://api.nasa.gov/rss/image-of-the-day.rss"),
              ("NASA APOD", "https://apod.nasa.gov/apod.rss"),
              ("Sky & Telescope", "https://skyandtelescope.org/feed/")],
    "science": [("ScienceDaily top", "https://www.sciencedaily.com/rss/top.xml"),
                ("BBC Science & Env", "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml"),
                ("Smithsonian", "https://www.smithsonianmag.com/feed/")],
    "animals": [("Good News Network", "https://www.goodnewsnetwork.org/feed/"),
                ("BBC Earth", "https://www.bbc.co.uk/news/science_env/rss"),
                ("ScienceDaily animals", "https://www.sciencedaily.com/news/plants_animals/animals/")],
    "world": [("BBC Top Stories", "https://feeds.bbci.co.uk/news/world/rss.xml"),
              ("NHK World", "https://www3.nhk.or.jp/rss/news/world.rss"),
              ("NPR World", "https://www.npr.org/rss/rss.php?f=1004")],
    "history": [("Smithsonian", "https://www.smithsonianmag.com/feed/"),
                ("NPR History", "https://www.npr.org/rss/rss.php?f=1026"),
                ("Atlas Obscura", "https://www.atlasobscura.com/articles/rss")],
    "explainers": [("HowStuffWorks", "https://recipes.howstuffworks.com/recipes.rss"),
                   ("ScienceDaily earth", "https://www.sciencedaily.com/news/earth_climate/earth_science/")],
    "listicles": [("Mental Floss", "https://mentalfloss.com/feeds/latest"),
                  ("Listverse", "https://listverse.com/feed/")],
    "trending": [("Reddit TIL (curated)", "https://old.reddit.com/r/todayilearned/top/.rss"),
                 ("NPR Trending", "https://www.npr.org/rss/rss.jsf?id=1001")],
}

LANE_KW = {
    "space": ("space", "nasa", "mars", "moon", "star", "galaxy", "telescope", "planet", "rocket"),
    "science": ("science", "study", "discovery", "research", "climate", "coral", "volcano"),
    "animals": ("animal", "bear", "orangutan", "whale", "shark", "bird", "turtle", "dolphin", "rescue"),
    "world": ("india", "europe", "africa", "asia", "summit", "aid", "recovery", "agreement"),
    "history": ("ancient", "world war", "medieval", "archaeo", "history", "discovered"),
    "explainers": ("how ", "why ", "what is", "does ", "can "),
    "listicles": ("best ", "top ", "reason", "things ", "10", "7", "5"),
    "trending": (),
}

BLOCK = ("war", "attack", "death toll", "killed", "murder", "court", "lawsuit", "covid",
         "pandemic", "election", "politic", "terror", "bomb", "shooting")


def items(url):
    p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url],
                       capture_output=True)
    try:
        data = p.stdout
        if data[:2] == b"\x1f\x8b":
            import gzip; data = gzip.decompress(data)
        root = ET.fromstring(data)
    except (ET.ParseError, TypeError):
        return []
    out = []
    for it in root.iter("item"):
        t = (it.findtext("title") or "").strip()
        if not t or len(t) < 25:
            continue
        out.append({"title": t, "link": (it.findtext("link") or "").strip(),
                    "description": (it.findtext("description") or "").strip()[:200],
                    "blocked": any(b in t.lower() for b in BLOCK)})
    return out


def pick(rows, lane):
    k = LANE_KW.get(lane, ())
    hits = [r for r in rows if not r["blocked"] and (not k or any(s in r["title"].lower() for s in k))]
    return hits or [r for r in rows if not r["blocked"]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--category", required=True, choices=list(CATEGORIES) + ["all"])
    ap.add_argument("--count", type=int, default=6)
    a = ap.parse_args()
    lanes = list(CATEGORIES) if a.category == "all" else [a.category]
    print("category=" + a.category)
    for lane in lanes:
        rows = []
        for _label, url in CATEGORIES[lane]:
            rows += items(url)
        for r in pick(rows, lane)[:a.count]:
            tag = "BLOCKED" if r["blocked"] else "ok"
            print(f"[{lane}/{tag}] {r['title']}\n  url: {r['link']}")
            if r["description"]:
                print(f"  desc: {r['description']}")


if __name__ == "__main__":
    main()
