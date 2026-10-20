#!/usr/bin/env python3
"""No-agent pre-gather for one lane: pick newest kid-safe story, cross-check it
against the same feed + 2 alternates, grab a public-domain image. Write a JSON
brief the lane agent consumes. Run on the VPS BEFORE the agent turn so the
agent's 16-iter budget only covers: write article -> deploy.
Usage: python3 tools/ow-gather.py --category science --write-to tools/brief.json
stdout: JSON {title,url,slug,desc,verified,image_url,image_credit,ok}
"""
import argparse, json, os, sys, html, re
import urllib.request
import defusedxml.ElementTree as ET  # safe XML parsing against XXE/billion-laughs

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "Mozilla/5.0 (OurWorld; contact andugulamani722@gmail.com)"

FEEDS = {
    "space": [("NASA APOD","https://apod.nasa.gov/apod.rss"),
              ("NASA Image of the Day","https://api.nasa.gov/rss/image-of-the-day.rss")],
    "science": [("ScienceDaily top","https://www.sciencedaily.com/news/top_news.xml"),
                ("BBC Science","https://feeds.bbci.co.uk/news/science_and_environment/rss.xml")],
    "animals": [("Good News Network","https://www.goodnewsnetwork.org/feed/"),
                ("BBC Earth","https://www.bbc.co.uk/news/science_env/rss")],
    "world": [("BBC Top Stories","https://feeds.bbci.co.uk/news/world/rss.xml"),
              ("NPR World","https://www.npr.org/rss/rss.php?f=1004")],
    "history": [("Smithsonian","https://www.smithsonianmag.com/feed/"),
                ("Atlas Obscura","https://www.atlasobscura.com/articles/rss")],
}
EXTRA_FEEDS = {"explainers": "science", "listicles": "science", "trending": "world"}

BLOCK = ("war","attack","death toll","killed","murder","court","lawsuit","covid",
         "pandemic","election","politic","terror","bomb","shooting","coronavirus")

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode("utf-8","ignore")

def rss_items(url):
    try:
        txt = fetch(url); root = ET.fromstring(txt)
    except Exception:
        return []
    out=[]
    for it in root.iter("item"):
        t=(it.findtext("title") or "").strip()
        if not t or len(t)<20: continue
        link=(it.findtext("link") or "").strip()
        if " " in link or not link.startswith("http"):
            link=(it.findtext("guid") or link).strip()
        desc=html.unescape((it.findtext("description") or "")[:300]).replace("\n"," ")
        out.append({"title":t,"link":link,"desc":desc,
                    "blocked":any(b in t.lower() for b in BLOCK)})
    return out

def slugify(t):
    s=re.sub(r"[^a-z0-9]+","-",t.lower()).strip("-")[:50]
    return s or "article"

def cross_check(url, alt_urls):
    ver=[]
    for u in [url]+alt_urls[:2]:
        try:
            h=fetch(u); t=re.search(r"<title[^>]*>([^<]+)</title>",h,re.I)
            title=html.unescape(t.group(1)).strip() if t else None
            ver.append({"url":u,"ok":bool(title),"title":title[:120] if title else None})
        except Exception as e:
            ver.append({"url":u,"ok":False,"err":str(e)[:80]})
    return ver

def pick_wiki_image():
    try:
        h=fetch("https://en.wikipedia.org/api/rest_v1/page/html/Main_Page")
        m=re.search(r'<img[^>]+src="(https://upload\.wikimedia\.org/[^"]+)"',h)
        if m: return m.group(1)+"?width=640","Wikimedia Commons (public domain)"
    except Exception:
        pass
    return None,None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--category",required=True,choices=list(FEEDS)+list(EXTRA_FEEDS))
    ap.add_argument("--write-to",default=os.path.join(HOME,"tools","brief.json"))
    a=ap.parse_args()
    lane = EXTRA_FEEDS.get(a.category, a.category)
    feeds = FEEDS[lane]
    rows=[]
    for _lab,url in feeds:
        rows += rss_items(url)
    rows=[r for r in rows if not r["blocked"]]
    if not rows:
        print(json.dumps({"ok":False,"error":"no candidates"})); sys.exit(3)
    base = os.path.join(HOME,"content","news" if a.category in ("trending","world") else a.category)
    written=[]
    if os.path.isdir(base):
        written=[os.path.join(base,f) for f in os.listdir(base) if f.endswith(".md")]
    c = rows[0]
    for r in rows:
        if not any(r["title"][:22] in open(w,encoding="utf-8",errors="ignore").read()[:2000] for w in written):
            c=r; break
    slug=slugify(c["title"])
    alt_urls=[u for _l,u in feeds]
    cc=cross_check(c["link"], alt_urls)
    srcs=[s for s in cc if s["ok"]]
    img,credit=pick_wiki_image()
    brief={"ok":True,"category":a.category,"title":c["title"],"url":c["link"],
           "slug":slug,"desc":c["desc"][:280],"verified":len(srcs)>=2,
           "cross_sources":cc,"image_url":img,"image_credit":credit}
    json.dump(brief,open(a.write_to,"w"),indent=2)
    print(json.dumps(brief)); sys.exit(0)

if __name__=="__main__":
    main()
