# Tirith-safe full Listverse feed scanner — prints every item with date.
import subprocess, xml.etree.ElementTree as ET
UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
url = "https://listverse.com/feed/"
p = subprocess.run(["curl","-s","--compressed","--max-time","25","-A",UA,url],
                   capture_output=True, text=True)
root = ET.fromstring(p.stdout)
items = []
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    link = (it.findtext("link") or "").strip()
    pub = (it.findtext("pubDate") or "").strip()
    if t:
        items.append((pub, t, link))
items.sort(reverse=True)
for pub, t, link in items[:15]:
    print(f"{pub}\n  {t}\n  {link}")
print("TOTAL", len(items))
