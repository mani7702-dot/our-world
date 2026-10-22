#!/usr/bin/env python3
"""Final candidate triage: verify remaining genuinely-fresh, non-MED, non-POL candidates."""
import re, os, glob

sd_re = re.compile(r'sciencedaily\.com/releases/\d{4}/\d{2}/(\d{12})\.htm')
existing_ids = {}
existing_titles = {}
for fp in glob.glob("content/blog/*.md") + glob.glob("content/news/*.md"):
    txt = open(fp, encoding="utf-8", errors="ignore").read()
    low = txt.lower()
    for m in sd_re.finditer(txt):
        existing_ids[m.group(1)] = os.path.basename(fp)
    t = re.search(r'^title:\s*(.*?)$', txt, re.M)
    if t:
        existing_titles[t.group(1).strip().lower()[:50]] = os.path.basename(fp)

print(f"Content files indexed: {len(existing_ids)} SD-cited + {len(existing_titles)} titles")

# NASA CASALS 3D Earth maps - check if it's a dup
print("\n=== NASA CASALS 3D Earth maps ===")
casals_hits = [f for f in glob.glob("content/news/*.md") + glob.glob("content/blog/*.md")
               if "3d map" in open(f, encoding="utf-8", errors="ignore").read().lower() or "casaLS".lower() in open(f).read().lower()]
print(f"CASALS/3D-map matches: {casals_hits}")

# Tracks longest drive on another world - is it dup of perseverance?
print("\n=== NASA Tracks longest drive ===")
ex = open("content/news/perseverance-mars-rover-driving-record.md", encoding="utf-8", errors="ignore").read().lower()
print(f"Existing: has 'tracks'? {'tracks' in ex}, has 'wheel'? {'wheel' in ex}, has 'drive'? {'drive' in ex}")
# The candidate is about Perseverance tracks in Jezero crater - same rover, possibly same paper

# Astronaut surprise - check topic
print("\n=== Astronaut surprise: same-topic-different-angle ===")
ex_path = "content/news/pupils-space-badge-meet-astronaut-rubio.md"
ex = open(ex_path, encoding="utf-8", errors="ignore").read().lower()
print(f"Existing title: {re.search(r'title: (.+)', ex).group(1)}")
ex_date = re.search(r'date: (.+)', ex)
print(f"Existing date: {ex_date.group(1) if ex_date else 'n/a'}")
print(f"Existing uses 'frank rubio': {'frank rubio' in ex}")
print(f"Existing uses 'tim peake': {'tim peake' in ex}")
print(f"Existing uses 'cruise': {'cruise' in ex}")
print(f"Existing category: {re.search(r'category: (.+)', ex).group(1)}")

print("\n=== Decision matrix ===")
print("1. Astronaut surprise (Tim Peake cruise): same TOPIC as existing pupils-space.")
print("   Different astronaut/event but kids+astronaut outreach theme already covered.")
print("   Per runbook 'same topic under different slug' = potential dup.")
print("   Risk: publishing two 'student meets astronaut' articles in same week.")
print("   Verdict: SKIP (same-topic-same-theme concern)")
print()
print("2. CASALS 3D maps: likely fresh, but is it kid-safe? (NASA Earth tech, not scary)")
print("3. Tracks longest drive: same Perseverance rover story, likely DUP.")
