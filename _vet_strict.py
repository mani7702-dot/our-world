#!/usr/bin/env python3
"""Re-vet all raw RSS titles with STRICT kid-safe guardrails + strict dupe grep.
MED-BLOCK if: treatment/therapy/disorder/diagnos/cure/ drug /patient/mental/health/disease/alzheimer/cancer/depression/therapy/medici (medical field words)
POL-BLOCK if: trump/biden/govern/minist/parliament/coup/war/conflict/terroris/military/election/terror/border/ban/lawmaker/politic/illegal/traffick
Then dupe-grep survivors against content/ with stable tokens.
"""
import os, re, html
from xml.etree import ElementTree as ET
ROOT="/home/ubuntu/our-world"
def load(p): return open(p,encoding="utf-8",errors="replace").read()
content_text={}
for d in ["content/blog","content/news"]:
    p=os.path.join(ROOT,d)
    if not os.path.isdir(p): continue
    for fn in os.listdir(p):
        if fn.endswith(".md"):
            fp=os.path.join(p,fn)
            content_text[fp.replace(ROOT+"/","")]=load(fp).lower()

files={"sciencedaily_top":"/tmp/owraw/sciencedaily_top.xml","bbc_science":"/tmp/owraw/bbc_science.xml"}
items=[]
for fn,p in files.items():
    tree=ET.parse(p)
    for it in tree.getroot().iter("item"):
        t=html.unescape(it.findtext("title","")).strip()
        l=it.findtext("link","")
        if t and l: items.append((fn,t,l))

MED=re.compile(r'\b(treatment|therap|disord|diagnos|cure\b|drug |patient|mental \w+|disease|alzheimer|cancer|depress|psych|neuro[d]?|clinical|trial|illness|symptom|brain damage|brain disease|mental disorder|therapy|treat )',re.I)
POL=re.compile(r'\b(trump|biden|govern|minister|parliament|coup|war\b|conflict|terroris|military|election|terror|border |ban\b|lawmak|politic|illegal|traffick|brexit|jackdaw|energy bill|oil and gas|net zero|climate change|courage|leadership)',re.I)

print(f"# Raw items to vet: {len(items)}")
survivors=[]
for fn,t,l in items:
    tl=t.lower()
    if MED.search(tl): continue
    if POL.search(tl): continue
    # dupe grep: literal phrase + stable tokens
    is_dup=False; dup_hit=""
    strong=re.findall(r'[a-z]+', tl)
    strong=[w for w in strong if len(w)>=5]
    for f,txt in content_text.items():
        if tl[:28] in txt[:3000]:
            is_dup=True; dup_hit=f; break
        if len(strong)>=2 and strong[0] in txt and strong[1] in txt:
            is_dup=True; dup_hit=f; break
    if is_dup: continue
    survivors.append((t,l))
print(f"# Kid-safe + fresh survivors: {len(survivors)}")
for t,l in survivors:
    print(f"  - {t}\n      {l}")
