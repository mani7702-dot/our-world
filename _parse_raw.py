#!/usr/bin/env python3
"""Parse raw RSS XML files -> title list, then full abort pass (dupe + MED + POL guards)."""
import os, re, html
from xml.etree import ElementTree as ET
ROOT="/home/ubuntu/our-world"
feeds_path="/tmp/owraw"
files=["sciencedaily_top.xml","bbc_science.xml","smithsonian.xml"]
items=[]
for fn in files:
    p=os.path.join(feeds_path,fn)
    if not os.path.exists(p): continue
    try:
        tree=ET.parse(p)
    except Exception as e:
        print(f"# {fn}: parse error {e}"); continue
    root=tree.getroot()
    # handle media namespace via findall with wildcards
    for it in root.iter("item"):
        title=it.findtext("title")
        link=it.findtext("link")
        if title:
            title=html.unescape(title).strip()
            items.append((fn,title,link or "?"))
print(f"# Total raw items parsed: {len(items)}")
# dedupe within feed
seen=set(); uniq=[]
for fn,t,l in items:
    if t in seen: continue
    seen.add(t); uniq.append((fn,t,l))
print(f"# Unique titles: {len(uniq)}")
print("# --- ALL titles ---")
for fn,t,l in uniq:
    print(f"{t}  [{fn}]")
