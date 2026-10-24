#!/usr/bin/env python3
"""Verify the two potentially-fresh UT stories against all content with tighter dedup."""
import os, re

stories = [
    ("flare-ribbons", "https://www.universetoday.com/articles/how-flare-ribbons-reveal-hidden-solar-explosions-on-the-sun"),
    ("stellar-nursery-ngc7129-early-stages-life", "https://www.universetoday.com/articles/webb-captures-stars-in-the-early-stages-of-life-in-a-nearby-stellar-nursery"),
]

existing_stems = set()
existing_basenames = set()
all_text = []
for d in ["content/news", "content/blog"]:
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            if f.endswith(".md"):
                stem = f[:-3]
                existing_stems.add(stem)
                existing_basenames.add(f)
                with open(os.path.join(d, f)) as fh:
                    all_text.append(fh.read().lower())

for token, url in stories:
    slug = token
    print(f"--- {slug} ---")
    print(f"  URL: {url}")
    # check slug in existing stems
    exact_match = any(slug in s for s in existing_stems)
    print(f"  slug in existing filename: {any(slug in s for s in existing_stems)}")
    # topic token check
    toks = re.split(r'[-_]', slug)
    for t in toks:
        if len(t) > 4:
            found = any(t in s for s in existing_stems)
            print(f"  topic token '{t}': {'DUP' if found else 'FRESH'}")
    # content keyword check
    for kw in ["flare ribbon", "stellar nursery", "ngc 7129", "hidden solar", "early stage"]:
        hits = [1 for t in all_text if kw in t]
        print(f"  keyword '{kw}' in content: {'DUP' if hits else 'FRESH'}")
    print()
