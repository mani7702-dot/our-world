#!/usr/bin/env python3
# Fallback ScienceDaily top.xml picker for trending lane (Reddit TIL blocked).
import re, sys, ssl
import urllib.request

UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
URL = "https://www.sciencedaily.com/rss/top.xml"

BLOCK = ("cancer", "glioblastoma", "tumor", "carcinoma", "alzheimer",
         "dementia", "parkinson", "arthritis", "diabetes", "blood pressure",
         "cardiovascular", "ptsd", "ibd", "inflammatory bowel", "weight loss",
         "obesity", "fat-burning", "diet", "statin", "cholesterol",
         "dental", "implant", "carpal tunnel", "surgery", "therapy",
         "treatment", "fish oil", "vitamin", "supplement", "vagus nerve",
         "ear stimulation", "nuclear", "radiation", "radioactive",
         "hurricane", "storm", "volcano", "tsunami", "earthquake",
         "chernobyl", "war", "attack", "death toll", "killed", "murder",
         "court", "lawsuit", "covid", "pandemic", "election", "politic",
         "terror", "bomb", "shooting")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
req = urllib.request.Request(URL, headers={"User-Agent": UA, "Accept": "application/xml"})
raw = urllib.request.urlopen(req, timeout=30, context=ctx).read()
# strip trailing HTML comment after </rss> if present
raw = re.sub(rb"<!--.*?-->\s*$", b"", raw, flags=re.DOTALL)
text = raw.decode("utf-8", "ignore")

# crude RSS item extraction
items = []
for m in re.finditer(r"<item>(.*?)</item>", text, re.DOTALL | re.IGNORECASE):
    block = m.group(1)
    tm = re.search(r"<title>(.*?)</title>", block, re.DOTALL | re.IGNORECASE)
    lm = re.search(r"<link>(.*?)</link>", block, re.DOTALL | re.IGNORECASE)
    dm = re.search(r"<description>(.*?)</description>", block, re.DOTALL | re.IGNORECASE)
    t = re.sub(r"<[^>]+>", "", tm.group(1)).strip() if tm else ""
    l = (lm.group(1) if lm else "").strip()
    d = re.sub(r"<[^>]+>", "", dm.group(1)).strip()[:220] if dm else ""
    items.append({"title": t, "link": l, "desc": d})

print("FALLBACK: ScienceDaily top.xml  count=%d" % len(items))
ok = 0
for i, it in enumerate(items):
    tl = it["title"].lower()
    blocked = any(b in tl for b in BLOCK)
    tag = "BLOCKED" if blocked else "ok"
    print("[%s] %s" % (tag, it["title"]))
    print("   url: %s" % it["link"])
    if it["desc"]:
        print("   desc: %s" % it["desc"])
    if not blocked:
        ok += 1
print("non-blocked=%d" % ok)
