#!/usr/bin/env python3
"""Triage raw science candidates: SD release-ID dupe + stable-token dupe + MED/POL/VIOLENT guardrails."""
import re, os, csv

# 1. Existing SD release IDs from already-written content
existing_ids = set()
existing_text = []
for d in ["content/blog", "content/news"]:
    if os.path.isdir(d):
        for f in os.listdir(d):
            if f.endswith(".md"):
                p = os.path.join(d, f)
                t = open(p, encoding="utf-8", errors="ignore").read()
                existing_text.append((p, t.lower()))
                existing_ids.update(re.findall(r"releases/\d{4}/\d{2}/(\d{12})\.htm", t))

GENERIC = {
    'scientists','discovery','discover','research','study','could','help','first',
    'universe','brain','cells','protein','gene','genes','cancer','light','quantum',
    'space','findings','found','new','a','the','of','and','in','to','for','why',
    'how','some','may','more','show','shows','reveal','reveals','suggests','effect',
    'effects','risk','higher','linked','uncover','uncovered','find','found','team',
    'university','institute','develop','developed','measure','measured','create','created',
    'brain','memory','aging','solar','earth','mars','moon','planet','space','orbit',
    'galaxy','nebula','star','telescope','astronomer','japanese','japan',
}

def tokens(s):
    return set(re.findall(r'[a-z]{5,}', re.sub(r'^(scientists|new study|a )', '', s.lower())))

MED = re.compile(r'\b(statin|cholesterol|alzheimer|dementia|brain damage|tau|amyloid|mental disorder|symptom|treat|therapy|diagnos|patient|inhaler|asthma| covid|infection|vaccine|depress|anxiety|autism|epilepsy|drug|pharma|cancer|stroke)\b', re.I)
POL = re.compile(r'\b(nobel|political|leadership|government|parliament|senate|minister|president|opposition|climate committee|policy|regulation|riot|protest|summit|united nation|arrest|war\b|conflict|doomsday)\b', re.I)
VIOLENT = re.compile(r'\b(massacre|death toll|catastrophic landslide|fatal)\b', re.I)

rows = list(csv.DictReader(open("/tmp/sc-candidates.tsv"), delimiter="\t"))
print("TOTAL candidates:", len(rows))
print("EXISTING SD IDs:", len(existing_ids))
print()

fresh = []
seen_titles = set()
for row in rows:
    title = row["title"]; link = row["link"]; desc = row["description"]
    if title in seen_titles:
        continue
    seen_titles.add(title)
    sd_ids = re.findall(r"releases/\d{4}/\d{2}/(\d{12})\.htm", link)
    nasa_ids = re.findall(r"science\.nasa\.gov/[^\s]*(\d{8})", link)  # nasa article id
    block = []
    if sd_ids and sd_ids[0] in existing_ids:
        block.append("DUP-SDID")
    if sd_ids and sd_ids[0] not in existing_ids and not MED.search(title+desc) and not POL.search(title) and not VIOLENT.search(title+desc):
        tt = tokens(title)
        for path, txt in existing_text:
            common = (tt & tokens(txt)) - GENERIC
            if len(common) >= 3:
                block.append("DUP-TOKEN")
                break
    if MED.search(title + " " + desc):
        block.append("MED")
    if POL.search(title):
        block.append("POL")
    if VIOLENT.search(title + " " + desc):
        block.append("VIOLENT")
    tl = title.lower()
    if any(tl in t2 for _, t2 in existing_text):
        block.append("DUP-LITERAL")
    if not block:
        fresh.append((title, link, sd_ids[0] if sd_ids else "", desc))
        print(f"  [FRESH] id={sd_ids[0] if sd_ids else 'n/a'}  {title}")
        print(f"          {link}")
    else:
        print(f"  [BLOCK:{','.join(block)}] {title}")

print("\n=== FRESH candidates:", len(fresh), "===")
for t,l,i,d in fresh:
    print(f"  {t}\n    id={i} {l}\n    desc={d[:100]}")
