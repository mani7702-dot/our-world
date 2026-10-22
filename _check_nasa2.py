#!/usr/bin/env python3
import os, glob, re

candidates = {
    'faster to science letter': ['faster to science', 'letter.*science community'],
    'nasa ncaa flyover alabama': ['ncaa.*flyover', 'flyover.*fan', 'alabama.*nasa'],
    'tracks longest drive another world': ['longest drive', 'tracks along', 'drive on another world', 'road to record'],
    'extratropical cyclone iceland': ['extratropical', 'cyclone.*iceland', 'whips past iceland', 'storms.*north atlantic'],
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

print("\n=== Done ===")
