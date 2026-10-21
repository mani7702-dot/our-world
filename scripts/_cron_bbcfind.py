import re
raw = open("/tmp/bbcsci.xml", encoding="utf-8", errors="replace").read()
items = re.findall(r"<item>(.*?)</item>", raw, re.S)
for it in items:
    t = re.search(r"<title>(.*?)</title>", it, re.S)
    l = re.search(r"<link>(.*?)</link>", it, re.S)
    if t and ("cleaning" in t.group(1).lower() or "palm" in t.group(1).lower() or "1,300" in t.group(1) or "1300" in t.group(1) or "wasps" in t.group(1).lower()):
        print("TITLE:", t.group(1).strip()[:160])
        print("URL:", l.group(1).strip()[:200])
        print()
