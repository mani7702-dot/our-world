import re, subprocess
UA="Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
urls = [
  "https://www.climate.gov/news-features/news",
  "https://www.climate.gov/news-features/expert-atlas/what-are-climate-aerosols",
  "https://www.climate.gov/news-features/understanding-climate",
]
for u in urls:
    h = subprocess.run(["curl","-s","--compressed","--max-time","18","-A",UA,u],
                       capture_output=True,text=True,timeout=22).stdout
    t=re.search(r"<title>(.*?)</title>",h,re.S|re.I)
    print(u, "bytes:", len(h))
    print("  TITLE:", (t.group(1).strip()[:140] if t else "(none)"))
    for kw in ["aerosol","sulphate","cooling","warming","reflect","dimming"]:
        idx=h.lower().find(kw.lower())
        if idx>=0:
            seg=re.sub(r"<[^>]+>"," ",h)[max(0,idx-50):idx+110].strip()
            print(f"  [{kw}]: {seg[:170]}...")
    print()
