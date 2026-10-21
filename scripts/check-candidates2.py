#!/usr/bin/env python3
"""Re-check --category all candidates with STABLE specific tokens only.
Per runbook: match on 3+ stable tokens (specific noun phrases), not generic words.
Tirith-safe file-based approach."""
import re, os

ROOT = "/home/ubuntu/our-world"
BLOG = os.path.join(ROOT, "content", "blog")
NEWS = os.path.join(ROOT, "content", "news")

# (url, title, [stable_tokens], block_reasons, category_tag)
CANDIDATES = [
    ("https://www.sciencedaily.com/releases/2026/10/261020085014.htm",
     "Massive study of 460,000 people challenges ultra-processed food cancer fears",
     ["ultra-processed food", "colorectal cancer", "460,000"],
     ["MED-BLOCK: cancer/treatment"],
     "science"),
    ("https://www.sciencedaily.com/releases/2026/10/261018205039.htm",
     "Something strange is happening beneath a volcano near 2 million people",
     ["masaya", "volcano", "nicaragua", "magma"],
     [],
     "science"),
    ("https://www.sciencedaily.com/releases/2026/10/261018084028.htm",
     "Modern neuroscience is rediscovering a surprising idea freud had 130 years ago",
     ["freud", "neuroscience", "mental disorder", "prediction"],
     ["MED-BLOCK: mental disorder/Freud therapy"],
     "science"),
    ("https://www.sciencedaily.com/releases/2026/10/261017230025.htm",
     "A simple touch can bring dying corals back to life in just 7 weeks",
     ["coral", "bleaching", "recovery", "7 weeks"],
     [],
     "science"),
    ("https://www.bbc.co.uk/news/articles/cxzd6j5q0g7eo",
     "Northern Ireland needs courage and leadership to tackle climate change",
     ["northern ireland", "climate change", "leadership"],
     ["POL-BLOCK: political leadership"],
     "world"),
    ("https://www.bbc.co.uk/news/videos/c6n9r7gvngx8o",
     "How Jackdaw ignites row over climate and costs",
     ["jackdaw", "climate", "wind"],
     ["POL-BLOCK: climate politics/energy"],
     "world"),
    ("https://www.goodnewsnetwork.org/north-americas-largest-wildlife-overpass-is-working-animal-collisions-on-i-25-down-91/",
     "North America's Largest Wildlife Overpass Is Working",
     ["wildlife overpass", "i-25", "colorado", "larkspur"],
     [],
     "animals"),
    ("https://www.bbc.co.uk/news/articles/ckx2qpw4rjd7o",
     "Ex-prosecutor charged with treason in Mexico over US drug raid",
     ["treason", "mexico", "drug raid", "prosecutor"],
     ["POL-BLOCK: treason/drug raid"],
     "world"),
    ("https://www.bbc.co.uk/news/articles/cqm2dzwdmmywo",
     "Borneo burning: Life on the frontline of SE Asia toxic haze",
     ["borneo", "haze", "peat fire", "toxic"],
     [],
     "world"),
    ("https://listverse.com/2026/10/20/10-movie-antagonists-who-deserved-more-sympathy/",
     "10 Movie Antagonists Who Deserved More Sympathy",
     ["movie antagonist", "sympathy"],
     [],
     "listicles"),
    ("https://listverse.com/2026/10/19/10-rare-lakes-that-took-weirdness-to-the-next-level/",
     "10 Lakes Where Nature Gets Seriously Weird",
     ["weird lake", "strange lake"],
     [],
     "listicles"),
    ("https://listverse.com/2026/10/16/10-of-the-biggest-music-careers-launched-by-sitcoms/",
     "10 of the Biggest Music Careers Launched by Sitcoms",
     ["music career", "sitcom", "launched"],
     [],
     "listicles"),
    ("https://listverse.com/2026/10/15/10-sunken-villages-that-mysteriously-reappear/",
     "Sunken Villages That Mysteriously Reappear",
     ["sunken village", "reappear"],
     [],
     "listicles"),
    ("https://listverse.com/2026/10/14/10-wild-facts-you-might-not-know-about-bears/",
     "10 Wild Facts You Might Not Know About Bears",
     ["wild fact bear"],
     [],
     "listicles"),
    ("https://listverse.com/2026/10/13/10-terrifying-medical-mysteries-that-turned-out-to-be-poisoning/",
     "10 Terrifying Medical Mysteries That Turned Out to Be Poisoning",
     ["medical mystery", "poisoning"],
     ["MED-BLOCK: medical mysteries/poisoning"],
     "listicles"),
]

def all_text():
    out = []
    for d in (BLOG, NEWS):
        if os.path.isdir(d):
            for f in os.listdir(d):
                if f.endswith(".md"):
                    p = os.path.join(d, f)
                    try:
                        out.append((os.path.basename(p), open(p, encoding="utf-8").read().lower()))
                    except Exception:
                        pass
    return out

TEXTS = all_text()

for url, title, tokens, reasons, cat in CANDIDATES:
    slug_match = re.search(r'/([^/]+)(?:\.md)?$', url.replace('?at',''))
    tlow = title.lower()
    dup_hits = []
    for bn, txt in TEXTS:
        # require 2+ stable tokens to match in same file (reduces false positives)
        matched = [w for w in tokens if w in txt]
        if len(matched) >= 2:
            dup_hits.append((bn, matched))
    if reasons:
        verdict = "BLOCKED: " + " | ".join(reasons)
    elif dup_hits:
        verdict = "DUP"
    else:
        verdict = "FRESH-KID-SAFE *** CANDIDATE ***"
    print(f"[{verdict}] ({cat}) {title[:65]}")
    print(f"   url: {url}")
    if dup_hits:
        for bn, m in dup_hits[:4]:
            print(f"   dup: {bn} (tokens: {m})")
    print()
