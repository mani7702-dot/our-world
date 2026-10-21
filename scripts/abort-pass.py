#!/usr/bin/env python3
# Full abort pass on a TSV of candidates.
import sys
# Read TSV, classify each FRESH line through guardrails.
MED = ("medical","disease","cancer","ebola","virus","treatment","therapy","diagnos",
       "mental","disorder","syndrome","illness","drug","fentanyl","opioid","poisoning",
       "hospital","patient","clinical","surgery","autism","depression","anxiety",
       "schizophren","addiction","alcohol","smoking","smoking")
POL = ("trump|zelenesk|zelensky|putin|election|politic|government|politician|parliament",
       "minister","president","senate","congress","lawsuit","court","jail","prison",
       "legal","tariff","diplom","foreign leader","riot","protest","climate change",
       "climate committee","netanyahu","macron","musk","merger","lawsuit","deport")
WAR = ("war","attack","killed","death","murder","bomb","shooting","terror","invasion",
       "siege","battle","military","troop","conflict","violence","assault","attacked")

with open(sys.argv[1]) as f:
    lines = f.readlines()
print("=== FRESH candidates through guardrails ===")
fresh = [l for l in lines if l.startswith("FRESH")]
for l in fresh:
    cols = l.rstrip("\n").split("\t")
    if len(cols) < 2: 
        continue
    title = cols[1].lower()
    flags = []
    if any(m in title for m in MED): flags.append("MED")
    if any(p in title for p in POL): flags.append("POL")
    if any(w in title for w in WAR): flags.append("WAR")
    status = "BLOCK:"+",".join(flags) if flags else "KID-SAFE-SURVIVOR"
    print(f"[{status}] {cols[1]}  | {cols[2]}")
