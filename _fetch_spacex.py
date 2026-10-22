#!/usr/bin/env python3
"""Find the exact ScienceDaily URL for the SpaceX ISS cargo story + NASA 2nd source."""
import subprocess, os, re, html
from xml.etree import ElementTree as ET
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
os.makedirs("/tmp/owcheck", exist_ok=True)
# get the link from sciencedaily_top feed
tree=ET.parse("/tmp/owraw/sciencedaily_top.xml")
sd_link=None
for it in tree.getroot().iter("item"):
    t=it.findtext("title")
    if t and "strange cargo" in t.lower():
        sd_link=it.findtext("link")
        print("SD title:", html.unescape(t).strip())
        print("SD url:", sd_link)
        break
# download SD article
if sd_link:
    r=subprocess.run(["curl","-s","--compressed","--max-time","25","-A",UA,sd_link,"-o","/tmp/owcheck/spacex_iss.html"],
                     capture_output=True, text=True)
    print("SD download exit:", r.returncode, "size:", os.path.getsize("/tmp/owcheck/spacex_iss.html"))
# also grab NASA ISS cargo page as 2nd source
nasa_urls=[
  "https://www.nasa.gov/mission_pages/station/research/news/spacex_cargo_26",
  "https://www.spacex.com/news/2026/10/20/spacex-crew-dragon-iss-resupply",
  "https://www.nasa.gov/press-release/spacex-iss-resupply-cargo-mission",
]
for u in nasa_urls:
    out="/tmp/owcheck/nasa_cargo.html"
    r=subprocess.run(["curl","-s","--compressed","--max-time","25","-A",UA,u,"-o",out],
                     capture_output=True, text=True)
    sz=os.path.getsize(out) if os.path.exists(out) else 0
    print(f"  NASA {u} -> exit={r.returncode} size={sz}")
