#!/usr/bin/env python3
"""Check which ScienceDaily release IDs are truly fresh."""
import urllib.request, re, html, os, subprocess

os.chdir("/home/ubuntu/our-world")
UA = "Mozilla/5.0 (compatible: OurWorldBot; contact andugulamani722@gmail.com)"

all_content = ""
for f in os.listdir("content/news"):
    if f.endswith(".md"):
        with open(f"content/news/{f}", "r", errors="replace") as fh:
            all_content += fh.read().lower() + "\n"

existing_sd_ids = set(re.findall(r"releases/\d{4}/\d{2}/(\d{14})\.htm", all_content))
print(f"Existing ScienceDaily release IDs in content: {len(existing_sd_ids)}")

p = subprocess.run(["curl", "-s", "-A", UA, "https://www.sciencedaily.com/rss/top.xml"], capture_output=True)
data = p.stdout
idx = data.rfind(b"</rss>")
data = data[:idx + 6]

items = re.findall(rb"<item>(.*?)</item>", data, re.DOTALL)

BLOCK = ("cancer", "alzheimer", "covid", "pandemic", "stroke", "depression",
         "anxiety", "ptsd", "parkinson", "arthritis", "diabetes", "blood pressure",
         "statin", "colorectal", "cardiovascular", "heart disease", "glioblastoma",)

fresh_items = []
for it in items:
    t = re.search(rb"<title>(.*?)</title>", it, re.DOTALL)
    l = re.search(rb"<link>(.*?)</link>", it, re.DOTALL)
    if t and l:
        title = html.unescape(t.group(1).decode("utf-8", errors="replace")).strip()
        link = html.unescape(l.group(1).decode("utf-8", errors="replace")).strip()
        m = re.search(r"(\d{4}/\d{2}/(\d{14}))\.htm", link)
        rid = m.group(2) if m else ""
        if rid in existing_sd_ids:
            continue
        if any(b in title.lower() for b in BLOCK):
            continue
        fresh_items.append((title, link, rid))

print(f"Fresh items (by release ID not in content): {len(fresh_items)}")
for t, l, rid in fresh_items:
    print(f"\n  {t}")
    print(f"  URL: {l}")
    print(f"  RID: {rid}")
