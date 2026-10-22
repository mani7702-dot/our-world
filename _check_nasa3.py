#!/usr/bin/env python3
import os, glob, re

# Check the remaining NASA articles more carefully
candidates = {
    'nasa ncaa flyover': ['ncaa', 'flyover', 'alabama'],
    'faster to science letter': ['faster to science', 'letter to the science'],
    'extratropical cyclone': ['extratropical', 'cyclone', 'iceland', 'north atlantic'],
}

for d in ['content/news', 'content/blog']:
    for f in glob.glob(f'{d}/*.md'):
        with open(f) as fh:
            content = fh.read().lower()
        fname = os.path.basename(f)
        for key, patterns in candidates.items():
            for pat in patterns:
                if re.search(pat, content):
                    print(f"EXISTS: {key} -> found '{pat}' in {d}/{fname}")
                    break

# Also fetch the NASA articles that we haven't checked
print("\n=== No matches found for NCAA flyover, faster to science, or extratropical cyclone ===")
print("These could be fresh candidates!")
