import re, subprocess
UA="Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
# climate.gov (NOAA) on aerosol cooling - a 2nd authoritative source
urls = [
  "https://www.climate.gov/news-features/understanding-climate/climate-change-global-temperature-aerosols",
  "https://www.climate.gov/news-features/news/what-are-aerosols-and-how-do-they-affect-climate",
]
for u in urls:
    try:
        h = subprocess.run(["curl","-s","--compressed","--max-time","18","-A",UA,u],
                          capture_output=True,text=True,timeout=22).stdout
        t=re.search(r"<title>(.*?)</title>",h,re.S|re.I)
        print(u, "bytes:", len(h))
        print("  TITLE:", (t.group(1).strip()[:140] if t else "(none)"))
        for kw in ["aerosol","sulphate","cooling","warming","reflect"]:
            idx=h.lower().find(kw.lower())
            if idx>=0:
                seg=re.sub(r"<[^>]+>"," ",h)[max(0,idx-50):idx+100].strip()
                print(f"  [{kw}]: {seg[:160]}...")
        print()
    except Exception as e:
        print(u,"ERR",e)
