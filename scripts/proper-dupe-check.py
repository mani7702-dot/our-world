#!/usr/bin/env python3
"""Proper dupe check: match on title words + slugs of existing posts, NOT body text with common words."""
import re, os

candidates = {
    "peat-fire-indonesia-bbc": {
        "title": "Why is a peat fire so bad? BBC is in Indonesia to find out",
        "slug_tokens": ["peat", "indonesia", "kalimantan", "fire"],
    },
    "jackdaw-energy-bills": {
        "title": "Will Jackdaw cut your energy bills?",
        "slug_tokens": ["jackdaw", "northsea", "north sea", "oilfield", "energy bill"],
    },
    "windermere-sewage-tunnel": {
        "title": "Giant tunnel proposed to clean up Windermere's sewage problem",
        "slug_tokens": ["windermere", "sewage", "tunnel"],
    },
    "extreme-heat-uk-aircon": {
        "title": "How the UK's extreme heat is shifting the conversation about air-con",
        "slug_tokens": ["aircon", "air-con", "extreme heat uk", "cooling"],
    },
    "night-shift-hidden-cost": {
        "title": "The hidden cost of the night shift and how to sleep it off",
        "slug_tokens": ["night shift", "shift.*work", "circadian"],
    },
    "atlantic-heat-britain": {
        "title": "After record heat, could the Atlantic make Britain's weather even more extreme?",
        "slug_tokens": ["atlantic", "gulf stream", "jet stream", "heat dome"],
    },
    "cheap-power-net-zero": {
        "title": "Why cheap power could matter more than clean power in the push for net zero",
        "slug_tokens": ["net zero", "gas field", "north sea", "cheap power"],
    },
    "new-lab-uplands": {
        "title": "New lab to become centre for investigating uplands",
        "slug_tokens": ["upland", "moorland", "moor", "hill", "uk upland"],
    },
    "jackdaw-energy-bills-2": {
        "title": "How Jackdaw ignites row over climate and costs",
        "slug_tokens": ["jackdaw", "energy field", "north sea"],
    },
}

# Get all existing slugs
existing_slugs = []
for d in ("content/blog", "content/news"):
    if not os.path.isdir(d): continue
    for f in os.listdir(d):
        if f.endswith(".md"):
            # strip date prefix if present
            slug = f.replace(".md", "")
            existing_slugs.append((d, slug))

print(f"Total existing posts: {len(existing_slugs)}")
print()

for slug, c in candidates.items():
    title = c["title"]
    tokens = c["slug_tokens"]
    # Check if any existing slug matches title keywords
    title_words = re.sub(r'[^a-z0-9 ]', ' ', title.lower()).split()
    title_words = [w for w in title_words if len(w) >= 4]
    hits = []
    for d, existing_slug in existing_slugs:
        slug_words = re.sub(r'[^a-z0-9 ]', ' ', existing_slug.lower()).split()
        # Check for word overlap in slug
        overlap = set(title_words) & set(slug_words)
        if len(overlap) >= 2:  # 2+ title words appear in the slug
            hits.append(f"{d}/{existing_slug} (slug overlap: {overlap})")
            continue
        # Check stable tokens in slug
        for tok in tokens:
            if re.search(tok, existing_slug.lower()):
                hits.append(f"{d}/{existing_slug} (token:'{tok}')")
                break
    status = "DUP" if hits else "FRESH"
    print(f"[{status}] {title}")
    if hits:
        for h in hits:
            print(f"   -> {h}")
    print()
