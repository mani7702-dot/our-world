#!/usr/bin/env python3
"""Extract title + summary/og:description + key fact phrases from saved article HTML."""
import re, sys, html
def load(p):
    return open(p, encoding="utf-8", errors="replace").read()
def meta(txt, name):
    m = re.search(rf'<meta[^>]+name="{name}"[^>]*content="([^"]*)"', txt, re.I)
    if not m: m = re.search(rf'<meta[^>]+content="([^"]*)"[^>]+name="{name}"', txt, re.I)
    return html.unescape(m.group(1))[:400] if m else ""
for slug in ["coral_touch","freud_neuro","ultraproc"]:
    txt=load(f"/tmp/owcheck/{slug}.html")
    title=re.search(r"<title>(.*?)</title>", txt, re.S|re.I)
    print(f"\n=== {slug} ===")
    print("TITLE:", html.unescape(title.group(1)).strip() if title else "?")
    print("OG_DESC:", meta(txt,"og:description"))
    print("SD_DESC:", meta(txt,"description"))
    # find any mention of treatment/therapy/disorder/cause for medical guardrail signal
    low=txt.lower()
    for w in ["treatment","therapy","treat ","clinical trial","disorder","diagnos","cure","drug","patient","mental illness"]:
        if w in low:
            print(f"  ! medical-signal word present: {w}")
    # find the release id from URL pattern
    m=re.search(r'/(\d{4})/(\d{2})/(\d{8})(\d{6})\.htm', txt)
    print("RELEASE_ID:", m.group(0) if m else "n/a")
