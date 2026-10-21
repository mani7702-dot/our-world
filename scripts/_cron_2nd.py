import subprocess
# Use a tiny file-based fetch of a web_search-like candidate: the ETH/Cicero aerosol-cooling study
# Try Nature news + a direct search-engine snippet for the cooling-aerosol unmasking narrative
UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
cands = [
  "https://www.nature.com/news/2026/10/261019-how-cleaning-the-air-unmasked-global-warming",
  "https://www.science.org/news/2026/10/cleaning-air-removes-aerosol-cooling-speeds-warming",
  "https://www.ft.com/content/aerosol-warming-cleaning-air",
  "https://climate.nasa.gov/news/cleaning-air-global-warming/",
]
import re
for u in cands:
    try:
        h = subprocess.run(["curl","-s","--compressed","--max-time","18","-A",UA,"-L","-o","/tmp/xc.html",u],
                          capture_output=True, text=True, timeout=22)
        import os
        sz = os.path.getsize("/tmp/xc.html") if os.path.exists("/tmp/xc.html") else 0
        print(u, "-> bytes:", sz)
        if sz > 1500:
            txt = open("/tmp/xc.html", encoding="utf-8", errors="replace").read()
            t = re.search(r"<title>(.*?)</title>", txt, re.S|re.I)
            print("  TITLE:", (t.group(1).strip()[:140] if t else "(none)"))
            for kw in ["aerosol","sulphate","ETH Zurich","Knutti","IPCC","warming"]:
                if re.search(kw, txt, re.I):
                    idx=txt.lower().find(kw.lower()); print(f"  [{kw}] ...{txt[max(0,idx-40):idx+70]}...")
    except Exception as e:
        print(u,"ERR",e)
    print()
