#!/usr/bin/env python3
"""Triage raw ScienceDaily candidates from a headerless TSV (title\tlink\tdesc).
Applies SD release-ID dedup + stable-token dupe + MED/POL/VIOLENT guardrails."""
import re, os, sys, csv

existing_text = []
existing_sd_ids = set()
for d in ["content/blog", "content/news"]:
    if os.path.isdir(d):
        for f in os.listdir(d):
            if f.endswith(".md"):
                p = os.path.join(d, f)
                t = open(p, encoding="utf-8", errors="ignore").read()
                existing_text.append((p, t.lower()))
                # Extract all SD release IDs from existing content
                existing_sd_ids.update(re.findall(r"releases/\d{4}/\d{2}/(\d{12})\.htm", t))
                # Also extract bare 12-digit IDs from SD URLs in content
                existing_sd_ids.update(re.findall(r"sciencedaily\.com/releases/\d{4}/\d{2}/(\d{12})\.htm", t))

GENERIC = {
    'scientists','discovery','discover','research','study','could','help','first',
    'universe','brain','cells','protein','gene','genes','cancer','light','quantum',
    'space','findings','found','new','a','the','of','and','in','to','for','why',
    'how','some','may','more','show','shows','reveal','reveals','suggests','effect',
    'effects','risk','higher','linked','uncover','uncovered','find','found','team',
    'university','institute','develop','developed','measure','measured','create','created',
    'memory','aging','solar','earth','mars','moon','planet','orbit',
    'galaxy','nebula','star','telescope','astronomer','japanese','japan',
    'scientists','find','found','discovered','discover','researchers','study',
}

def word_tokens(s):
    return set(re.findall(r'[a-zA-Z]{5,}', s))

MED = re.compile(r'\b(statin|cholesterol|alzheimer|dementia|brain damage|tau|amyloid|mental disorder|therapy|diagnos|patient|inhaler|asthma|covid|infection|vaccine|depress|anxiety|autism|epilepsy|drug|pharma|doomsday|diabetes|treat|depress|mental)\b', re.I)
POL = re.compile(r'\b(nobel|political|leadership|government|parliament|senate|minister|president|opposition|climate committee|policy|regulation|riot|protest|summit|united nation|arrest|war\b|conflict|merger|tesla|musk)\b', re.I)
VIOLENT = re.compile(r'\b(massacre|death toll|catastrophic landslide|fatal|tsunami)\b', re.I)

rows = list(csv.reader(open("/tmp/sc-candidates.tsv"), delimiter="\t"))
print("TOTAL candidates:", len(rows))
print("EXISTING SD IDs:", len(existing_sd_ids))
print()

fresh = []
for parts in rows:
    if len(parts) < 2:
        continue
    title, link = parts[0].strip(), parts[1].strip()
    desc = parts[2].strip() if len(parts) > 2 else ""
    if not title or not link:
        continue

    sd_ids = re.findall(r"releases/\d{4}/\d{2}/(\d{12})\.htm", link)
    block = []

    # SD release ID duplicate check
    if sd_ids and sd_ids[0] in existing_sd_ids:
        block.append("DUP-SDID")

    # Medical guardrail
    if MED.search(title + " " + desc):
        block.append("MED")
    # Political guardrail
    if POL.search(title):
        block.append("POL")
    # Violent guardrail
    if VIOLENT.search(title + " " + desc):
        block.append("VIOLENT")

    # Stable-token dupe check (3+ non-generic tokens)
    tt = word_tokens(title)
    if tt:
        for path, txt in existing_text:
            common = (tt & word_tokens(txt)) - GENERIC
            if len(common) >= 3:
                block.append("DUP-TOKEN")
                break

    # Literal title duplicate
    tl = title.lower()
    for _, t2 in existing_text:
        if tl in t2:
            block.append("DUP-LITERAL")
            break

    if not block:
        fresh.append((title, link, sd_ids[0] if sd_ids else "", desc))
        print(f"  [FRESH] id={sd_ids[0] if sd_ids else 'n/a'}  {title}")
        print(f"          {link}")
    else:
        print(f"  [BLOCK:{','.join(block)}] {title}")

print(f"\n=== FRESH candidates: {len(fresh)} ===")
for t, l, i, d in fresh:
    print(f"  {t}\n    id={i} {l}\n    desc={d[:120]}")
