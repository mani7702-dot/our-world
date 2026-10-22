#!/usr/bin/env python3
"""Final audit: parse BBC Science & Environment raw feed and list ALL items with dup+guardrail status."""
import re, os
from xml.etree import ElementTree as ET

path = "/tmp/feed-science-1.xml"  # BBC Science from rss-raw-fallback.py
if not os.path.exists(path):
    print("BBC Science feed not found, re-downloading")
    import subprocess
    subprocess.run(["curl","-s","--compressed","--max-time","25",
                    "-A","Mozilla/5.0 (OurWorld raw-fallback; contact andugulamani722@gmail.com)",
                    "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
                    "-o",path], capture_output=True)

raw = open(path, encoding="utf-8", errors="ignore").read()
raw = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', '', raw)
raw = re.sub(r'&(?![a-zA-Z#0-9]+;)', '&amp;', raw)
try:
    root = ET.fromstring(raw)
except ET.ParseError:
    # brute force
    root = ET.fromstring(re.sub(r'<([^>]+)>', lambda m: m.group(0) if not m.group().startswith("</") else m.group(0), raw)[:])

items = []
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    l = (it.findtext("link") or "").strip()
    if len(t) > 15:
        items.append((t, l))

print(f"BBC Science total items: {len(items)}")

# Load ALL content for dup check
all_content = {}
for d in ("content/blog", "content/news"):
    if not os.path.isdir(d): continue
    for f in os.listdir(d):
        if not f.endswith(".md"): continue
        fp = os.path.join(d, f)
        all_content[f] = open(fp, encoding="utf-8", errors="ignore").read().lower()

MED = ("alzheimer","dementia","treat","therapy","cancer","diabetes","statin","drug","prescription","diagnos","symptom","covid","stroke","heart attack","cholesterol","liver disease","blood pressure","freud","mental disorder","mental health","parkinson","depressio","anxiety","autism","epilepsy")
POL = ("jackdaw","stormont","badenoch","burnham","politic","election","parliament","elon musk","merger","energy bill","ni risks","northern ireland","scotland.*energy","oil.*gas","climate change committee","net zero","energy security","brexit","labour","conservative","rishi","sunak")

for i, (t, l) in enumerate(items[:20]):
    tl = t.lower()
    # guardrails
    med = any(re.search(w, tl + " " + l) for w in MED)
    pol = any(re.search(w, tl) for w in POL)
    # dup check: title 35-char substring + stable tokens
    title_dup = any(tl[:35] in v[:700] for v in all_content.values())
    tokens = [w for w in re.sub(r'[^a-z0-9 ]',' ',tl).split() if len(w)>=6]
    tok_dup = any(sum(1 for w in tokens if w in txt) >= 3 for txt in all_content.values())
    verdict = "BLOCK" if (med or pol) else ("DUP" if (title_dup or tok_dup) else "FRESH")
    flags = []
    if med: flags.append("MED")
    if pol: flags.append("POL")
    if title_dup: flags.append("TITLE-DUP")
    if tok_dup and not title_dup: flags.append("TOK-DUP")
    print(f"[{verdict:6s} {'/'.join(flags) if flags else ''}] {t[:80]}")
    print(f"         {l[:100]}")
