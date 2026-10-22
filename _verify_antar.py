#!/usr/bin/env python3
"""Verify Antarctica dinosaur fossil candidate + fetch sources (ScienceDaily + Wikipedia)."""
import subprocess, os, re, html
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
os.makedirs("/tmp/owcheck", exist_ok=True)
def load(p): return open(p,encoding="utf-8",errors="replace").read()
# find the SD URL for the antarctica dinosaur story from the feed
from xml.etree import ElementTree as ET
tree=ET.parse("/tmp/owraw/sciencedaily_top.xml")
sd_link=None; sd_title=""
for it in tree.getroot().iter("item"):
    t=it.findtext("title")
    if t and ("antarctica" in t.lower() and "dinosaur" in t.lower()):
        sd_link=it.findtext("link"); sd_title=html.unescape(t).strip(); break
print("SD title:", sd_title)
print("SD url:", sd_link)
if sd_link:
    r=subprocess.run(["curl","-s","--compressed","--max-time","25","-A",UA,sd_link,"-o","/tmp/owcheck/antar_dino_sd.html"],
                     capture_output=True, text=True)
    print("SD dl exit:",r.returncode,"size:",os.path.getsize("/tmp/owcheck/antar_dino_sd.html"))
    t=load("/tmp/owcheck/antar_dino_sd.html")
    mt=re.search(r"<title>(.*?)<",t,re.S|re.I)
    print("SD TITLE:", html.unescape(mt.group(1)).strip() if mt else "?")
    md=re.search(r'<meta[^>]+name="description"[^>]*content="([^"]*)"',t,re.I)
    print("SD META:", html.unescape(md.group(1)).strip()[:400] if md else "?")
    paras=re.findall(r'<p[^>]*>(.*?)</p>',t,re.S|re.I)
    body=[html.unescape(re.sub(r'<[^>]+>','',p)).strip() for p in paras if len(html.unescape(re.sub(r'<[^>]+>','',p)).strip())>40]
    print("SD BODY (first 10):")
    for b in body[:10]: print("  -",b[:280])
# Wikipedia 2nd source: Amulet (fossil) or Antarctic dinosaurs
for name,u in [("wiki_amulet","https://en.wikipedia.org/wiki/Amulet_(fossil)"),
               ("wiki_antar_dino","https://en.wikipedia.org/wiki/Dinosaur")]:
    out=f"/tmp/owcheck/{name}.html"
    r=subprocess.run(["curl","-s","--compressed","--max-time","25","-A",UA,u,"-o",out],capture_output=True,text=True)
    sz=os.path.getsize(out) if os.path.exists(out) else 0
    print(f"{name}: exit={r.returncode} size={sz} -> {out}")
