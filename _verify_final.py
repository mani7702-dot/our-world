#!/usr/bin/env python3
"""Fetch BBC Antarctica dinosaur story + Wikipedia 2nd sources for cross-check."""
import subprocess, os, re, html
from xml.etree import ElementTree as ElementTree
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
os.makedirs("/tmp/owcheck", exist_ok=True)
def load(p): return open(p,encoding="utf-8",errors="replace").read()
# find the bbc link for the antarctica dinosaur title
tree=ElementTree.parse("/tmp/owraw/bbc_science.xml")
bbc_link=""
for it in tree.getroot().iter("item"):
    t=it.findtext("title","")
    if "antarctica" in t.lower() and "dinosaur" in t.lower():
        bbc_link=it.findtext("link")
        print("BBC TITLE:", html.unescape(t).strip())
        print("BBC LINK:", bbc_link)
        # get description for fact hints
        d=it.findtext("description","")
        print("BBC DESC:", html.unescape(d).strip()[:400])
        break
# download the BBC article
if bbc_link:
    r=subprocess.run(["curl","-s","--compressed","--max-time","25","-A",UA,bbc_link,"-o","/tmp/owcheck/antar_dino_bbc.html"],
                     capture_output=True, text=True)
    print("BBC dl exit:",r.returncode,"size:",os.path.getsize("/tmp/owcheck/antar_dino_bbc.html"))
    t=load("/tmp/owcheck/antar_dino_bbc.html")
    mt=re.search(r"<title>(.*?)<",t,re.S|re.I)
    print("BBC PAGE TITLE:", html.unescape(mt.group(1)).strip() if mt else "?")
    md=re.search(r'<meta[^>]+name="description"[^>]*content="([^"]*)"',t,re.I)
    print("BBC META:", html.unescape(md.group(1)).strip()[:400] if md else "?")
    # body paragraphs
    paras=re.findall(r'<p[^>]*>(.*?)</p>',t,re.S|re.I)
    body=[html.unescape(re.sub(r'<[^>]+>','',p)).strip() for p in paras if len(html.unescape(re.sub(r'<[^>]+>','',p)).strip())>60]
    print("BBC BODY (first 12):")
    for b in body[:12]: print("  -",b[:280])
# Wikipedia 2nd source candidates for Antarctic dinosaurs
import subprocess as sp
for name,u in [("wiki_antarctopetra","https://en.wikipedia.org/wiki/Dinosaur")]:
    out=f"/tmp/owcheck/{name}.html"
    r=sp.run(["curl","-s","--compressed","--max-time","25","-A",UA,u,"-o",out],capture_output=True,text=True)
    w=load(out)
    idxs=[m.start() for m in re.finditer(r'antarctica|amulet|jameson|crystal',w[:500000],re.I)]
    print(f"\n=== Wikipedia Dinosaur: 'antarctica/amulet/jameson/crystal' hits in first 500KB: {len(idxs)} (positions {idxs[:3]})")
    if idxs:
        seg=w[max(0,idxs[0]-200):idxs[0]+600]
        print("SNIPPET:", html.unescape(re.sub(r'<[^>]+>',' ',seg)).strip()[:500])
