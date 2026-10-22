#!/usr/bin/env python3
"""FINAL VERIFICATION: extract ALL SD release IDs from candidate articles (raw RSS)
and check each against existing content by grepping the ID string in every content file."""
import re, os, csv

# Collect every SD URL from content files (both formats)
sd_url_re = re.compile(r'https?://(?:www\.)?sciencedaily\.com/releases/(\d{14})\.htm')
existing_ids = set()
id_to_file = {}
for d in ("content/blog", "content/news"):
    if not os.path.isdir(d): continue
    for f in sorted(os.listdir(d)):
        if not f.endswith(".md"): continue
        fp = os.path.join(d, f)
        txt = open(fp, encoding="utf-8", errors="ignore").read()
        for m in sd_url_re.finditer(txt):
            existing_ids.add(m.group(1))
            id_to_file.setdefault(m.group(1), []).append(f)

print(f"Existing SD release IDs found in content: {len(existing_ids)}")
for rid in sorted(existing_ids):
    print(f"  {rid}: {id_to_file[rid][0]}")

# Now extract candidate IDs from raw-candidates.tsv
print("\n=== Candidate SD IDs vs existing content ===")
lines = open("/tmp/raw-candidates.tsv", encoding="utf-8").read().split("\n")
for ln in lines:
    if not ln.strip() or ln.startswith("status\t") or ln.startswith("  ->"):
        continue
    parts = ln.split("\t")
    if len(parts) < 3:
        continue
    status = parts[0]; title = parts[1]; link = parts[2]
    if "sciencedaily.com" not in link:
        continue
    m = re.search(r'(\d{14})', link)
    if m:
        cid = m.group(1)
        if cid in existing_ids:
            print(f"  DUP (SD-ID {cid}): {title[:70]}")
        # else: ID not in content -> potentially fresh
