#!/usr/bin/env python3
"""Tirith-safe raw RSS fallback: download feeds with curl --compressed to files, parse full item list."""
import subprocess, os, re
ROOT="/home/ubuntu/our-world"
os.makedirs("/tmp/owraw", exist_ok=True)
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
feeds={
  "sciencedaily_top":"https://www.sciencedaily.com/rss/top.xml",
  "science_daily_science":"https://www.sciencedaily.com/rss/news/sciences/topstories/science.xml",
  "bbc_science":"https://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
  "smithsonian":"https://www.smithsonianmag.com/feed/",
}
for name,url in feeds.items():
    out=f"/tmp/owraw/{name}.xml"
    r=subprocess.run(["curl","-s","--compressed","--max-time","25","-A",UA,url,"-o",out],
                     capture_output=True, text=True)
    sz=os.path.getsize(out) if os.path.exists(out) else 0
    print(f"{name}: exit={r.returncode} size={sz} -> {out}")
