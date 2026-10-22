#!/usr/bin/env python3
import re, os, glob

# SD release URL format: sciencedaily.com/releases/2026/10/2610XXXXXXX.htm
# The ID after /10/ is YYMMDDHHMMSS = 12 digits, NOT 14
sd_url_re = re.compile(r'sciencedaily\.com/releases/\d{4}/\d{2}/(\d{12})\.htm')

existing = {}
for fp in glob.glob("content/blog/*.md") + glob.glob("content/news/*.md"):
    txt = open(fp, encoding="utf-8", errors="ignore").read()
    for m in sd_url_re.finditer(txt):
        existing.setdefault(m.group(1), []).append(os.path.basename(fp))

print(f"Unique SD release IDs cited in content source blocks: {len(existing)}")
print("\n=== All cited SD IDs (sorted) ===")
for rid in sorted(existing):
    print(f"  {rid}: {existing[rid][0][:60]}")

# The candidates to verify
fresh_ids = {
    "261019093353": "kill dangerous gut bacteria (C diff)",
    "261018205047": "Alaska monster tsunami 1580 feet",
    "261017230035": "third form of magnetism (altermagnetism)",
    "261017230028": "blueberries mood",
    "261017230025": "corals back to life touch",
    "261017230018": "ghostly green star",
    "261016081103": "39 sweeteners gut",
    "261016080912": "drug reverses fatty liver",
}
# But wait - my candidate IDs are 14 digits. Let me check what format the raw RSS uses.
