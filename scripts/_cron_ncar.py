import re, subprocess
UA="Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
# NCAR / UCAR authoritative explainer on aerosol cooling
urls = [
  "https://www.acs.org/content/acs/en/climatescience/aerosols/aerosol-cooling-effect.html",
  "https://www.ncar.ucar.edu/education/boreal-aerosols",
  "https://science.nasa.gov/earth-science/climate-change/aerosols",
]
for u in urls:
    try:
        h = subprocess.run(["curl","-s","--compressed","--max-time","18","-A",UA,u],
                           capture_output=True,text=True,timeout=22).stdout
        t=re.search(r"<title>(.*?)</title>",h,re.S|re.I)
        print(u, "bytes:", len(h))
        print("  TITLE:", (t.group(1).strip()[:140] if t else "(none)"))
        for kw in ["aerosol","sulphate","sulfate","cooling","reflect","sunlight","dimming"]:
            idx=h.lower().find(kw.lower())
            if idx>=0:
                seg=re.sub(r"<[^>]+>"," ",h)[max(0,idx-50):idx+110].strip()
                print(f"  [{kw}]: {seg[:170]}...")
        print()
    except Exception as e:
        print(u,"ERR",e)
