#!/usr/bin/env python3
"""Find the Antarctica dinosaur title in the raw SD feed + extract Wikipedia Amulet facts."""
import re, html, os
from xml.etree import ElementTree as ET
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
import subprocess
def load(p): return open(p,encoding="utf-8",errors="replace").read()
tree=ET.parse("/tmp/owraw/sciencedaily_top.xml")
for it in tree.getroot().iter("item"):
    t=html.unescape(it.findtext("title","")).strip()
    if "antarctica" in t.lower() or "fossil" in t.lower() or "amulet" in t.lower():
        print("MATCH:", t)
        print("  url:", it.findtext("link"))
# Wikipedia Amulet
w=load("/tmp/owcheck/wiki_amulet.html")
print("\n=== Wikipedia Amulet (fossil) ===")
mt=re.search(r"<title>(.*?)<",w,re.I)
print("TITLE:", html.unescape(mt.group(1)).strip() if mt else "?")
# first paragraphs
paras=re.findall(r'<p[^>]*>(.*?)</p>',w,re.S|re.I)
body=[html.unescape(re.sub(r'<[^>]+>','',p)).strip() for p in paras if len(html.unescape(re.sub(r'<[^>]+>','',p)).strip())>50]
for b in body[:8]: print("  -", b[:300])
# Wikipedia Dinosaur page - search for Antarctic mentions
d=load("/tmp/owcheck/wiki_antar_dino.html")
idx=[m.start() for m in re.finditer(r'antarctica|amulet|jameson',d[:100000],re.I)]
print("\n=== Wikipedia Dinosaur: Antarctic mentions at positions:", idx[:5])
if idx:
    seg=d[max(0,idx[0]-300):idx[0]+500]
    print("SNIPPET:", html.unescape(re.sub(r'<[^>]+>',' ',seg)).strip()[:500])
