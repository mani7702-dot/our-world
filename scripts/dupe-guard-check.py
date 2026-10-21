# Tirith-safe multi-dupe guard: checks a core phrase against content/blog + content/news.
# Usage: python3 scripts/dupe-guard-check.py <core-phrase>
import os, re, sys
PHRASE = sys.argv[1] if len(sys.argv) > 1 else ""
hits = []
for dp in ['content/blog', 'content/news']:
    if not os.path.isdir(dp): continue
    for f in os.listdir(dp):
        if f.endswith('.md'):
            try:
                txt = open(os.path.join(dp, f), encoding='utf-8', errors='ignore').read()
            except Exception: continue
            if re.search(PHRASE, txt, re.I): hits.append(os.path.join(dp, f))
print('DUP' if hits else 'FRESH', hits)
