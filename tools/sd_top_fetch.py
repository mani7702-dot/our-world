#!/usr/bin/env python3
import subprocess, xml.etree.ElementTree as ET, gzip
UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
URL = "https://www.sciencedaily.com/rss/top.xml"
p = subprocess.run(["curl","-s","--max-time","30","-A",UA,URL], capture_output=True)
data = p.stdout
if data[:2] == b"\x1f\x8b":
    data = gzip.decompress(data)
# strip trailing html comment
idx = data.rfind(b"</rss>")
if idx != -1:
    data = data[:idx+6]
try:
    root = ET.fromstring(data)
except Exception as e:
    print("PARSE ERROR:", e)
    print("RAW (first 500):", data[:500])
    raise SystemExit

BLOCK = ("covid","pandemic","cancer","alzheimer","depression","anxiety","ptsd","surgery","tumor","stroke","heart disease","diabetes","blood pressure","vaccine","drug","treatment","therapy","mental health","covid-19","coronavirus","death","dying","mortality","fatal","dead","autopsy","obituary","casualty","epidemic","infection","outbreak","virus","dementia","schizophrenia","bipolar","addiction","overdose","opioid","cholesterol")
KID_TOPIC_NEG = ("war","attack","bomb","shooting","killed","murder","death","court","lawsuit","terror","politic","election","protest","riot","riot","disaster","hurricane","cyclone","tsunami","flood","wildfire","landslide","massacre","genocide","crisis","refugee","displaced","conflict","battle","military")

out = []
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    link = (it.findtext("link") or "").strip()
    desc = (it.findtext("description") or "").strip()[:300]
    tl = t.lower()
    if len(t) < 25: continue
    blocked = any(b in tl for b in BLOCK) or any(k in tl for k in KID_TOPIC_NEG)
    out.append({"title":t,"link":link,"desc":desc,"blocked":blocked})

for r in out:
    tag = "BLOCKED" if r["blocked"] else "ok"
    print(f"[{tag}] {r['title']}")
    print(f"  url: {r['link']}")
    if r["desc"]:
        print(f"  desc: {r['desc']}")
    print()
