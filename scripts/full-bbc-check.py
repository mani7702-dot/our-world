#!/usr/bin/env python3
"""Exhaustive dupe check on ALL non-blocked BBC Science candidates with precise stable tokens."""
import re, os

# All FRESH-flagged BBC candidates from the earlier scan, EXCEPT the ones already confirmed as dups
candidates = {
    "peat-fire-indonesia-bbc": {
        "title": "Why is a peat fire so bad? BBC is in Indonesia to find out",
        "tokens": ["peat", "kalimantan", "indonesia fire", "torched", "carbon sink", "drain.*swamp"],
    },
    "jackdaw-energy-bills": {
        "title": "Will Jackdaw cut your energy bills?",
        "tokens": ["jackdaw", "energy bill", "oil field", "north sea", "gas"],
    },
    "windermere-sewage-tunnel": {
        "title": "Giant tunnel proposed to clean up Windermere's sewage problem",
        "tokens": ["windermere", "sewage", "tunnel", "sewage.*clean"],
    },
    "extreme-heat-uk-aircon": {
        "title": "How the UK's extreme heat is shifting the conversation about air-con",
        "tokens": ["extreme heat", "air.*con", "heat wave", "cooling"],
    },
    "night-shift-hidden-cost": {
        "title": "The hidden cost of the night shift and how to sleep it off",
        "tokens": ["night shift", "sleep", "circadian", "shift work"],
    },
    "atlantic-heat-britain": {
        "title": "After record heat, could the Atlantic make Britain's weather even more extreme?",
        "tokens": ["atlantic", "heat dom", "gulf stream", "jet stream"],
    },
    "cheap-power-net-zero": {
        "title": "Why cheap power could matter more than clean power in the push for net zero",
        "tokens": ["net zero", "cheap power", "energy", "electricity"],
    },
    "new-lab-uplands": {
        "title": "New lab to become centre for investigating uplands",
        "tokens": ["upland", "lab", "moorland", "hill"],
    },
    "australian-fires-peats": {
        "title": "How Jackdaw ignites row over climate and costs",
        "tokens": ["jackdaw"],
    },
}

# Already confirmed as published/dup
confirmed_dups = ["webb-brown-dwarf-weather", "silverpit-crater-asteroid-tsunami", 
                   "alaska-landslide-tsunami-trcy-arm", "worlds-oldest-shipwreck-kekova",
                   "dinosaur-antarctica-fossil-drawer", "el-nino-global-weather-impacts",
                   "pupils-space-badge-meet-astronaut", "japan-mmx-mars-phobos-sample",
                   "borneo-fires-peat-smoke-haze-science", "fin-whale-lunge-feeding-pembrokeshire"]

for slug, c in candidates.items():
    title, tokens = c["title"], c["tokens"]
    hits = []
    for d in ("content/blog", "content/news"):
        if not os.path.isdir(d): continue
        for f in os.listdir(d):
            if not f.endswith(".md"): continue
            fp = os.path.join(d, f)
            txt = open(fp, encoding="utf-8", errors="ignore").read().lower()
            head = txt[:500].lower()
            # literal title in frontmatter
            if title.lower()[:45] in head:
                hits.append(f"{d}/{f} (literal-title)")
                continue
            for kw in tokens:
                if re.search(kw, txt):
                    hits.append(f"{d}/{f} (token:'{kw}')")
                    break
    status = "DUP" if hits else "FRESH"
    print(f"[{status}] {title}")
    if hits:
        for h in hits:
            print(f"   -> {h}")
    print()
