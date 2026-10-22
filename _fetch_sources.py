#!/usr/bin/env python3
"""Tirith-safe fetcher: downloads 2 news article HTML files to /tmp for offline inspection."""
import subprocess, os
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
urls = {
    "coral_touch": "https://www.sciencedaily.com/releases/2026/10/261017230025.htm",
    "freud_neuro": "https://www.sciencedaily.com/releases/2026/10/261018084028.htm",
    "ultraproc": "https://www.sciencedaily.com/releases/2026/10/261020085014.htm",
}
os.makedirs("/tmp/owcheck", exist_ok=True)
for slug, u in urls.items():
    out = f"/tmp/owcheck/{slug}.html"
    r = subprocess.run(["curl","-s","--compressed","--max-time","25","-A",UA,u,"-o",out],
                       capture_output=True, text=True)
    size = os.path.getsize(out) if os.path.exists(out) else 0
    print(f"{slug}: curl exit={r.returncode} size={size} -> {out}")
