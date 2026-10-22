#!/usr/bin/env python3
"""Find NASA + Wikipedia 2nd sources for SpaceX CRS-35 facts (launch Oct 13, dock Oct 15)."""
import subprocess, os, re, html
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
os.makedirs("/tmp/owcheck", exist_ok=True)
def load(p): return open(p,encoding="utf-8",errors="replace").read()
urls={
  "wiki_crs35":"https://en.wikipedia.org/wiki/SpaceX_CRS-35",
  "nasa_iss2":"https://www.nasa.gov/internationalscience/iss-crs35",
  "nasa_launch":"https://www.nasa.gov/launchschedule/",
  "nasa_media2":"https://www.nasa.gov/multimedia/nasatv/iss_crs35.html",
  "spacex_crs":"https://www.spacex.com/vehicles/crewed-dragon/",
}
for name,u in urls.items():
    out=f"/tmp/owcheck/{name}.html"
    r=subprocess.run(["curl","-s","--compressed","--max-time","25","-A",UA,u,"-o",out],
                     capture_output=True, text=True)
    sz=os.path.getsize(out) if os.path.exists(out) else 0
    # check if it's a NASA 404 (195039 bytes is the NASA 404 stub)
    stub=False
    if sz==195039 and "Page Not Found" in load(out):
        stub=True
    print(f"{name}: exit={r.returncode} size={sz} 404stub={stub} -> {out}")

print("\n=== Wikipedia CRS-35 content ===")
w=load("/tmp/owcheck/wiki_crs35.html")
print("LEN:", len(w))
if "Page not found" not in w[:2000] and len(w)>5000:
    # extract first paragraphs
    mw=re.search(r'<title>(.*?)</title>', w, re.I)
    print("TITLE:", html.unescape(mw.group(1)).strip() if mw else "?")
    paras=re.findall(r'<p[^>]*>(.*?)</p>', w, re.S|re.I)
    body=[html.unescape(re.sub(r'<[^>]+>','',p)).strip() for p in paras if len(html.unescape(re.sub(r'<[^>]+>','',p)).strip())>50]
    for b in body[:6]:
        print("  -", b[:250])
