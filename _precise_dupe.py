import os, re

SEARCH = "blueberries every day may have a surprising effect on your mood"
stable_tokens = ["blueber", "mood", "depress", "older adults", "three months", "gut microbi"]

# Check all .md files in both content dirs
for d in ("content/blog", "content/news"):
    if not os.path.isdir(d):
        continue
    for f in sorted(os.listdir(d)):
        if not f.endswith(".md"):
            continue
        path = os.path.join(d, f)
        txt = open(path, encoding="utf-8", errors="ignore").read().lower()
        matches = []
        for tok in stable_tokens:
            if tok in txt:
                matches.append(tok)
        if len(matches) >= 3:
            print(f"DUP? {path} matches={matches}")
        elif matches:
            print(f"PARTIAL {path} matches={matches}")

# Also check the exact title
print("\n--- Exact title grep ---")
for d in ("content/blog", "content/news"):
    if not os.path.isdir(d):
        continue
    for f in sorted(os.listdir(d)):
        if not f.endswith(".md"):
            continue
        path = os.path.join(d, f)
        txt = open(path, encoding="utf-8", errors="ignore").read().lower()
        if "blueberr" in txt and ("mood" in txt or "depress" in txt):
            print(f"EXACT-MATCH: {path}")
