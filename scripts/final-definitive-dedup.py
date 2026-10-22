#!/usr/bin/env python3
"""FINAL DEFINITIVE DEDUP: for each SD top candidate, grep its CORE HEADLINE PHRASE
(not generic tokens) against both content/ dirs. Uses phrase-level matching."""
import re, os, csv

# Every SD top candidate (from rss-raw-fallback output), with their title
candidates = [
    ("massive asteroid slammed into the North Sea","261020085727"),
    ("Just 4 minutes a day can dramatically improve strength","261020085025"),
    ("Too much RNA can starve cells of energy","261020085023"),
    ("A train was delayed by a solar storm","261020085021"),
    ("Astronauts hearts just passed a surprising test for Mars","261020085016"),
    ("ultra-processed food cancer fears","261020085014"),
    ("reverse 60 years of aging in human cells","261020085013"),
    ("Perseverance Mars rover shattered the all-time off-world driving record","261020084818"),
    ("statins can cause muscle pain","261019093447"),
    ("ghostly eyeless creature hidden in Chinese cave","261019093445"),
    ("Hurricane warning maps are improving","261019093443"),
    ("Universe first five minutes","261019093442"),
    ("10 different diets linked to slower aging","261019093439"),
    ("vitamin C and cancer survival","261019093437"),
    ("bizarre Jurassic squid","261019093434"),
    ("aging brain may be trading memory","261019093357"),
    ("fight Alzheimer brain damage","261019093355"),
    ("kill dangerous gut bacteria","261019093353"),
    ("asteroid Bennu boulders","261018205101"),
    ("3000 steps Alzheimer","261018205058"),
    ("arthritis return after cancer treatment","261018205055"),
    ("quantum limit on a surface","261018205053"),
    ("16 stunning galaxies hiding cosmic chaos","261018205050"),
    ("Alaska monster tsunami 1580 feet","261018205047"),
    ("escape Alzheimer high-risk gene","261018205044"),
    ("volcano near Nicaragua Masaya","261018205039"),
    ("Nobel Prize brain cells light","261018205037"),
    ("taste food after COVID","261018205033"),
    ("fractional fermi sea","261018084644"),
    ("Alzheimer sleep restored without clearing plaques","261018084421"),
    ("Freud neuroscience","261018084028"),
    ("magic mushroom aggressive fish","261017230036"),
    ("third form of magnetism","261017230035"),
    ("natural compound protect brain salt","261017230032"),
    ("red meat sugar diabetes","261017230031"),
    ("blueberries mood","261017230028"),
    ("corals back to life touch","261017230025"),
    ("Japan volcanic apocalypse","261017230023"),
    ("brain pathways depression relief","261017230021"),
    ("male female skin different rules","261017230020"),
    ("ghostly green star","261017230018"),
    ("deep sleep builds muscle","261016081140"),
    ("39 sweeteners gut","261016081103"),
    ("drug reverses fatty liver","261016080912"),
    ("two monster black holes collide 100 years","261016070650"),
    ("youth protein aging brain cells","261016070646"),
    ("bird flies thousands of miles","261016070624"),
]

# Build content corpus
corpus = {}
for d in ("content/blog", "content/news"):
    if not os.path.isdir(d): continue
    for f in sorted(os.listdir(d)):
        if not f.endswith(".md"): continue
        corpus[f] = open(os.path.join(d,f), encoding="utf-8", errors="ignore").read().lower()

guardword_med = ["alzheimer","statin","cancer","diabetes","liver disease","mental disorder","freud",
                 "depress","covid","stroke","cholesterol","treat","therapy","dementia","parkinson",
                 "autism","symptom","diagnos"]
guardword_pol = ["jackdaw","stormont","badenoch","burnham","elon musk","merger","energy bill",
                 "northern ireland","politic","election","net zero"]

for phrase, sd_id in candidates:
    # normalize: 5+ char tokens in phrase
    tokens = [w for w in re.sub(r'[^a-z0-9 ]',' ',phrase.lower()).split() if len(w)>=5]
    dup_file = None
    for fname, txt in corpus.items():
        # title-phrase match
        if phrase[:40].lower() in txt[:800]:
            dup_file = fname; break
        # 3+ stable token match
        hits = sum(1 for w in tokens if len(w)>=5 and w in txt)
        if hits >= 3:
            dup_file = fname; break
    # guards
    combined = phrase.lower()
    is_med = any(w in combined for w in guardword_med)
    is_pol = any(w in combined for w in guardword_pol)
    
    if is_med or is_pol:
        verdict = "BLOCK"
    elif dup_file:
        verdict = f"DUP({dup_file})"
    else:
        verdict = "*** GENUINELY FRESH ***"
    print(f"[{verdict}] {phrase[:70]} (SD {sd_id})")
