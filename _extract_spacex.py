#!/usr/bin/env python3
"""Extract title/og:desc/body from the SpaceX ISS cargo SD article + NASA 2nd source."""
import re, html, os
def load(p):
    return open(p,encoding="utf-8",errors="replace").read()
def meta(txt,name):
    m=re.search(rf'<meta[^>]+name="{name}"[^>]*content="([^"]*)"',txt,re.I)
    if not m: m=re.search(rf'<meta[^>]+content="([^"]*)"[^>]+name="{name}"',txt,re.I)
    return html.unescape(m.group(1)).strip()[:300] if m else ""
def og(txt,name):
    m=re.search(rf'<meta[^>]+property="{name}"[^>]*content="([^"]*)"',txt,re.I)
    return html.unescape(m.group(1)).strip()[:300] if m else ""
print("=== ScienceDaily SpaceX ISS cargo ===")
t=load("/tmp/owcheck/spacex_iss.html")
mt=re.search(r"<title>(.*?)<",t,re.S|re.I)
print("TITLE:", mt.group(1).strip() if mt else "?")
print("OG_TITLE:", og(t,"og:title"))
print("OG_DESC:", og(t,"og:description"))
print("META_DESC:", meta(t,"description"))
# pull body paragraphs
paras=re.findall(r'<p[^>]*>(.*?)</p>', t, re.S|re.I)
body=[html.unescape(re.sub(r'<[^>]+>','',p)).strip() for p in paras if len(html.unescape(re.sub(r'<[^>]+>','',p)).strip())>40]
print("BODY PARAS (first 12):")
for b in body[:12]:
    print("  -", b[:200])
print("\n=== NASA (mission_pages/station/research/news/spacex_cargo_26) ===")
n=load("/tmp/owcheck/nasa_cargo.html")
print("LEN:", len(n))
nt=re.search(r"<title>(.*?)<",n,re.S|re.I)
print("TITLE:", nt.group(1).strip() if nt else "?")
print("OG_TITLE:", og(n,"og:title"))
print("OG_DESC:", og(n,"og:description"))
nparas=re.findall(r'<p[^>]*>(.*?)</p>', n, re.S|re.I)
nbody=[html.unescape(re.sub(r'<[^>]+>','',p)).strip() for p in nparas if len(html.unescape(re.sub(r'<[^>]+>','',p)).strip())>40]
print("BODY PARAS (first 8):")
for b in nbody[:8]:
    print("  -", b[:200])
