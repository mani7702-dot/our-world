#!/usr/bin/env python3
"""Full abort pass on raw RSS candidates: dupe grep (both dirs, stable tokens) + MED/POL guards."""
import os, re, html
from xml.etree import ElementTree as ET
ROOT="/home/ubuntu/our-world"
# collect existing content text
content_text={}
for d in ["content/blog","content/news"]:
    p=os.path.join(ROOT,d)
    if not os.path.isdir(p): continue
    for fn in os.listdir(p):
        if fn.endswith(".md"):
            fpath=os.path.join(p,fn)
            try:
                content_text[fpath.replace(ROOT+"/","")]=open(fpath,encoding="utf-8",errors="replace").read().lower()
            except: pass

files={"sciencedaily_top":"/tmp/owraw/sciencedaily_top.xml","bbc_science":"/tmp/owraw/bbc_science.xml"}
items=[]
for fn,p in files.items():
    tree=ET.parse(p); root=tree.getroot()
    for it in root.iter("item"):
        t=it.findtext("title")
        if t: items.append(html.unescape(t).strip())

# stable-token candidates: pick titles likely fresh + kid-safe, then triage
# We check every title: dupe (literal phrase) + stable-token overlap + MED/POL signal
MED=re.compile(r'treatment|therapy|therapy|disorder|diagnos|cure|drug |patient|mental illness|alzheimer|autism|tumor|cancer|disease|drug trial|clinical|psycho', re.I)
POL=re.compile(r'trump|biden|politic|government|parliament|minister|coup|war |conflict|terroris|military|border|election|republican|democrat|policy|climate change debate|energy bill|oil and gas licen', re.I)
# note: "climate" alone is fine (environmental mechanism); political phrasing is blocked

# stable tokens per title for cross-check
results=[]
for t in items:
    title_l=t.lower()
    # dupe check: literal phrase in any existing file
    literal_hit=[f for f,txt in content_text.items() if title_l[:25] in txt[:2000]]
    # stable-token check: pick 2-3 strong nouns from title
    strong=re.findall(r'[a-z]+', title_l)
    strong=[w for w in strong if len(w)>=5]
    token_hit=[]
    if len(strong)>=2:
        for f,txt in content_text.items():
            if strong[0] in txt and strong[1] in txt:
                token_hit.append(f)
    is_med=bool(MED.search(t))
    is_pol=bool(POL.search(t))
    # status: DUP if literal or token hit; MED-BLOCK; POL-BLOCK; FRESH
    if literal_hit or token_hit:
        status="DUP"
    elif is_med:
        status="MED-BLOCK"
    elif is_pol:
        status="POL-BLOCK"
    else:
        status="FRESH"
    results.append((status,t,title_l,literal_hit[:1],token_hit[:1],is_med,is_pol))

# print summary
fresh=[r for r in results if r[0]=="FRESH"]
print(f"# Total: {len(results)}  FRESH: {len(fresh)}  DUP: {len([r for r in results if r[0]=='DUP'])}  MED-BLOCK: {len([r for r in results if r[0]=='MED-BLOCK'])}  POL-BLOCK: {len([r for r in results if r[0]=='POL-BLOCK'])}")
print("\n=== FRESH candidates (need 2nd-source + kid-safe review) ===")
for s,t,tl,lh,th,_,_ in fresh:
    print(f"  - {t}")
print("\n=== ALL MED-BLOCK ===")
for s,t,tl,_,_ ,_,_ in results:
    if s=="MED-BLOCK": print(f"  - {t}")
print("\n=== ALL POL-BLOCK ===")
for s,t,tl,_,_ ,is_m,is_p in results:
    if s=="POL-BLOCK": print(f"  - {t} [med={is_m}]")
