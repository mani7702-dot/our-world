# Tirith-safe dupe guard: file-based ElementTree + grep across both content dirs.
# Usage: python3 scripts/scan-dupes.py <slug> <core-phrase>
# Prints FRESH-KID-SAFE / DUP / MED-BLOCK / POL-BLOCK for the phrase.
import re, sys

PHRASE = sys.argv[2]
hits = []
for dp in ['content/blog', 'content/news']:
    import os
    if not os.path.isdir(dp):
        continue
    for f in os.listdir(dp):
        if not f.endswith('.md'):
            continue
        try:
            txt = open(os.path.join(dp, f), encoding='utf-8', errors='ignore').read()
        except Exception:
            continue
        if re.search(PHRASE, txt, re.I):
            hits.append(os.path.join(dp, f))

# guardrails
lower = PHRASE.lower()
MED = ('treatment', 'therapy', 'diagnos', 'mental disorder', 'cure', 'patients with', 'condition')
POL = ('politic', 'election', 'court ', 'lawsuit', 'terror', 'bomb', 'shooting', 'war ', 'attack')
if hits:
    print('DUP', hits)
elif any(b in lower for b in MED):
    print('MED-BLOCK')
elif any(b in lower for b in POL):
    print('POL-BLOCK')
else:
    print('FRESH-KID-SAFE')
