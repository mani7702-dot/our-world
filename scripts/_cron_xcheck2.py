import subprocess, re, sys
UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
# Real 2nd-source candidates: IPCC / Nature / Science on aerosol cooling trend
urls = sys.argv[1:] if len(sys.argv) > 1 else [
  "https://www.nature.com/articles/s41558-026-01856-3",
  "https://www.science.org/doi/10.1126/science.admc1234",
  "https://www.ipcc.ch/report/ar6/wg1/",
  "https://www.bbc.co.uk/news/articles/c20917w25n4o",
]
for u in urls:
    try:
        h = subprocess.run(["curl","-s","--compressed","--max-time","20","-A",UA,u],
                          capture_output=True, text=True, timeout=25).stdout
    except Exception as e:
        print(u, "ERR", e); continue
    print("URL:", u, "BYTES:", len(h))
    t = re.search(r"<title>(.*?)</title>", h, re.S|re.I)
    print("TITLE:", (t.group(1).strip()[:160] if t else "(none)"))
    md = re.search(r'<meta name="description" content="([^"]*)"', h, re.I)
    if md: print("DESC:", md.group(1).strip()[:260])
    text = re.sub(r"<[^>]+>", " ", h)
    for kw in ["aerosol", "sulphate", "ETH Zurich", "Knutti", "IPCC", "cooling effect", "cleaning the air", "2027"]:
        if re.search(re.escape(kw), text, re.I):
            idx = text.lower().find(kw.lower())
            print(f"  [{kw}]: ...{text[max(0,idx-50):idx+90].strip()}...")
    print()
