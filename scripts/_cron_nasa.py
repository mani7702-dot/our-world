import re, subprocess
UA="Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
urls = [
  "https://earthobservatory.nasa.gov/features/146884/aerosols",
  "https://earthobservatory.nasa.gov/features/aerosols",
  "https://climate.nasa.gov/news/2992/aerosols-past-present-and-future/",
]
for u in urls:
    h = subprocess.run(["curl","-s","--compressed","--max-time","18","-A",UA,u],
                       capture_output=True,text=True,timeout=22).stdout
    t=re.search(r"<title>(.*?)</title>",h,re.S|re.I)
    print(u, "bytes:", len(h))
    print("  TITLE:", (t.group(1).strip()[:140] if t else "(none)"))
    for kw in ["aerosol","sulphate","sulfate","cooling","reflect","sunlight","dimming","warming"]:
        idx=h.lower().find(kw.lower())
        if idx>=0:
            seg=re.sub(r"<[^>]+>"," ",h)[max(0,idx-60):idx+130].strip()
            print(f"  [{kw}]: {seg[:200]}...")
    print()
