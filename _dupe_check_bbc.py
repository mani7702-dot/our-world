#!/usr/bin/env python3
import os, glob

# Dupe check specific candidates against existing content
candidates = {
    'peat fire indonesia': ['peat fire', 'peat.*fire', 'indonesia.*peat'],
    'badge space nasa': ['badge sent to space', 'badge.*space', 'nasa.*astronaut.*pupil', 'pupil.*badge'],
    'orionid meteor': ['orionid', 'meteor shower'],
    'mars moon sample mission': ['mars.*moon.*sample', 'sample.*mars.*moon', 'japanese.*moon', ' MMX', 'martian moon'],
    'shipwreck turkey': ['shipwreck', 'oldest shipwreck', 'kekova', 'amphorae'],
    'dinosaur antarctica': ['dinosaur.*antarctica', 'antarctica.*dinosaur', 'dinosaur.*bone.*antarctica'],
    'fin whale': ['fin whale', 'whale.*engulf', 'fin.*whale'],
}

for d in ['content/news', 'content/blog']:
    for f in glob.glob(f'{d}/*.md'):
        with open(f) as fh:
            content = fh.read().lower()
        fname = os.path.basename(f)
        for key, patterns in candidates.items():
            import re
            for pat in patterns:
                if re.search(pat, content):
                    print(f"EXISTS: {key} -> found '{pat}' match in {d}/{fname}")
                    break

# Now check the Mars mission article specifically
print("\n=== Checking Mars mission articles ===")
for f in glob.glob('content/news/*.md') + glob.glob('content/blog/*.md'):
    with open(f) as fh:
        content = fh.read().lower()
    if 'moon' in content and 'mars' in content:
        # find the title
        for line in content.split('\n')[:5]:
            if line.startswith('title:'):
                print(f"  {f}: {line[:80]}")
                break

# Check for badge space
print("\n=== Checking badge/space articles ===")
for f in glob.glob('content/news/*.md') + glob.glob('content/blog/*.md'):
    with open(f) as fh:
        content = fh.read().lower()
    if 'badge' in content and ('space' in content or 'nasa' in content or 'astronaut' in content):
        for line in content.split('\n')[:5]:
            if line.startswith('title:'):
                print(f"  {f}: {line[:80]}")
                break

print("\n=== Checking peat fire articles ===")
for f in glob.glob('content/news/*.md') + glob.glob('content/blog/*.md'):
    with open(f) as fh:
        content = fh.read().lower()
    if 'peat fire' in content or 'indonesia' in content and 'peat' in content:
        for line in content.split('\n')[:5]:
            if line.startswith('title:'):
                print(f"  {f}: {line[:80]}")
                break
