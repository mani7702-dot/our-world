#!/usr/bin/env python3
import re, os
existing_ids = set()
for d in ["content/blog", "content/news"]:
    if os.path.isdir(d):
        for f in os.listdir(d):
            if f.endswith(".md"):
                t = open(os.path.join(d, f), encoding="utf-8", errors="ignore").read()
                found = re.findall(r"releases/\d{4}/\d{2}/(\d{12})\.htm", t)
                if found:
                    existing_ids.update(found)
                    print(f"  {f}: {found}")
print("TOTAL existing IDs:", len(existing_ids))
print(sorted(existing_ids))
