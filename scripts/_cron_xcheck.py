#!/usr/bin/env python3
# 2nd-source cross-check: pull Met Office / Science on aerosol cooling removal
import subprocess, re
UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
urls = [
  "https://www.metoffice.gov.uk/news/press-and-news/news/2026/world-likely-to-warm-as-aerosol-cooling-removed",
  "https://www.science.org/doi/10.1126/science.admc1234",
]
def fetch(u):
    return subprocess.run(["curl","-s","--compressed","--max-time","20","-A",UA,u],
                          capture_output=True, text=True).stdout
for u in urls:
    h = fetch(u)
    print("URL:", u, "BYTES:", len(h))
    if len(h) > 500:
        t = re.search(r"<title>(.*?)</title>", h, re.S|re.I)
        print("TITLE:", (t.group(1).strip() if t else "(none)")[:160])
        md = re.search(r'<meta name="description" content="([^"]*)"', h, re.I)
        if md:
            print("DESC:", md.group(1).strip()[:300])
        # Look for aerosol / sulphate / warming mentions
        text = re.sub(r"<[^>]+>", " ", h)
        for kw in ["aerosol", "sulphate", "sulfate", "cooling", "ETH Zurich", "Knutti", "IPCC"]:
            if re.search(kw, text, re.I):
                idx = text.lower().find(kw.lower())
                print(f"  HIT {kw}: ...{text[max(0,idx-40):idx+80].strip()}...")
        print()
    else:
        print("  (too small / error)")
        print()
