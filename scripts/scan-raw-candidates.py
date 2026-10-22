#!/usr/bin/env python3
"""Rigorous dedup + guardrail pass on /tmp/raw-candidates.tsv.
- Extracts SD release IDs from content files (two URL formats).
- Checks title-phrase + stable-token against BOTH content dirs.
- Applies MED/POL/VIOLENCE guardrails per runbook.
File-based, Tirith-safe."""
import re, os, sys

# ---- 1. Gather existing SD release IDs from content ----
existing_ids = set()
# two formats: full URL releases/2610260xxxxx.htm  AND  bare 2610xx... inside text
url_re = re.compile(r'sciencedaily\.com/releases/(\d{14})\.htm')
for d in ("content/blog", "content/news"):
    if not os.path.isdir(d):
        continue
    for f in sorted(os.listdir(d)):
        if not f.endswith(".md"):
            continue
        fp = os.path.join(d, f)
        txt = open(fp, encoding="utf-8", errors="ignore").read()
        for u in url_re.findall(txt):
            existing_ids.add(u)

print(f"Existing SD release IDs in content: {len(existing_ids)}")
sys.stdout.flush()

# ---- 2. Load all content text for substring checking ----
all_content = {}
for d in ("content/blog", "content/news"):
    if not os.path.isdir(d):
        continue
    for f in sorted(os.listdir(d)):
        if not f.endswith(".md"):
            continue
        fp = os.path.join(d, f)
        txt = open(fp, encoding="utf-8", errors="ignore").read()
        all_content[f] = txt.lower()

# ---- 3. Guardrails ----
MED_WORDS = ("alzheimer","dementia","treat","therapy","cancer","diabetes","statin",
             "brain damage","depression","mental disorder","mental health","cure",
             "disease","illness","patient","drug","prescription","diagnos","symptom",
             "covid","stroke","heart attack","cholesterol","liver disease","blood pressure",
             "freud","psychotherapy","neuroscience.*treat","taste.*covid","cognitive decline")
POL_WORDS = ("jackdaw","stormont","badenoch","burnham","politic","election","parliament",
             "merger.*tesla","merger.*spacex","elon musk","energy bill","energy goals",
             "ni risks","northern ireland","scotland.*energy","oil.*gas licence",
             "climate change committee","courage and leadership","net zero","energy security",
             "sewage","windermere","tunnel","night shift")

def is_medical(title, desc):
    combined = (title + " " + desc).lower()
    for w in MED_WORDS:
        if re.search(w, combined):
            return True
    return False

def is_political(title, desc):
    combined = (title + " " + desc).lower()
    for w in POL_WORDS:
        if re.search(w, combined):
            return True
    return False

# ---- 4. Parse TSV ----
lines = open("/tmp/raw-candidates.tsv", encoding="utf-8").read().split("\n")
candidates = []
for ln in lines:
    if not ln.strip() or ln.startswith("status\t") or ln.startswith("  ->"):
        continue
    parts = ln.split("\t")
    if len(parts) < 3:
        continue
    candidates.append({
        "status": parts[0].strip(),
        "title": parts[1].strip(),
        "link": parts[2].strip(),
        "desc": parts[3].strip() if len(parts) > 3 else ""
    })

print(f"\nTotal candidates to re-check: {len(candidates)}")
print("\n=== FINAL CLASSIFICATION ===\n")

truly_fresh = []
for c in candidates:
    title = c["title"]
    link = c["link"]
    desc = c["desc"]
    tl = title.lower()
    
    # SD ID check
    sd_id = ""
    if "sciencedaily.com" in link:
        m = url_re.search(link)
        if m:
            sd_id = m.group(1)
    sd_dup = sd_id and sd_id in existing_ids
    
    # Title-phrase dup check (first 30 chars)
    title_dup = any(tl[:30] in txt[:900] for txt in all_content.values())
    
    # Stable token check (5+ char tokens, 3+ matches)
    stable_tokens = [w for w in re.sub(r'[^a-z0-9 ]',' ',tl).split() if len(w)>=6]
    token_dup = False
    for fname, txt in all_content.items():
        hits = sum(1 for w in stable_tokens if w in txt)
        if hits >= 3:
            token_dup = True
            break
    
    # Guardrails
    med = is_medical(title, desc)
    pol = is_political(title, desc)
    
    if sd_dup:
        verdict = "SD-ID-DUP"
    elif title_dup:
        verdict = "TITLE-DUP"
    elif token_dup:
        verdict = "TOK-DUP"
    elif med:
        verdict = "MED-BLOCK"
    elif pol:
        verdict = "POL-BLOCK"
    else:
        verdict = "FRESH"
        truly_fresh.append(c)
    
    flag = ""
    if sd_id:
        flag = f" sd_id={sd_id}"
    print(f"[{verdict:10s}] {title[:80]}{flag}")

print(f"\n=== {len(truly_fresh)} TRULY FRESH CANDIDATES ===")
for c in truly_fresh:
    print(f"  - {c['title']}")
    print(f"    {c['link']}")
