#!/usr/bin/env python3
"""Fetch NASA 2nd source candidates for the SpaceX CRS-35 ISS cargo story."""
import subprocess, os
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
os.makedirs("/tmp/owcheck", exist_ok=True)
urls={
  "nasa_iss_resupply":"https://www.nasa.gov/mission_pages/station/research/news/2026/iss-research-35",
  "nasa_spacex_crs35":"https://www.nasa.gov/content/spacex-crs-35-mission-overviews",
  "nasa_iss_crew":"https://www.nasa.gov/mission_pages/station/main/iss-crew.html",
  "spacex_crs35":"https://www.spacex.com/launches/",
  "wikipedia_iss":"https://en.wikipedia.org/wiki/List_of_International_Space_Station_expeditions",
}
for name,u in urls.items():
    out=f"/tmp/owcheck/{name}.html"
    r=subprocess.run(["curl","-s","--compressed","--max-time","25","-A",UA,u,"-o",out],
                     capture_output=True, text=True)
    sz=os.path.getsize(out) if os.path.exists(out) else 0
    print(f"{name}: exit={r.returncode} size={sz} -> {out}")
