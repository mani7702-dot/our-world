#!/usr/bin/env python3
import os, glob, re

# Dupe check NASA main feed candidates against existing content
candidates = {
    'rs-25 engine test artemis': ['rs-25', 'rs25', 'artemis engine', 'engine test.*artemis'],
    'casals 3d maps earth': ['casals', '3d map.*earth', 'earth.*3d map', 'surface map'],
    'cassiopeia ghosts': ['cassiopeia', 'ghost.*cassiopeia', 'new ghost.*cassiopeia'],
    'extratropical cyclone iceland': ['extratropical cyclone', 'cyclone.*iceland', 'whips past iceland'],
    'nasa texas farmland flights': ['texas farmland', 'low.altitude.*flight', 'farmland.*flight'],
    'ncaa flyover alabama': ['ncaa.*flyover', 'flyover.*university', 'alabama.*nasa'],
    'faster to science letter': ['faster to science', 'letter.*science community'],
    'jpl 90 years': ['jpl.*90', '90 years.*jpl'],
}

for d in ['content/news', 'content/blog']:
    for f in glob.glob(f'{d}/*.md'):
        with open(f) as fh:
            content = fh.read().lower()
        fname = os.path.basename(f)
        for key, patterns in candidates.items():
            for pat in patterns:
                if re.search(pat, content):
                    print(f"EXISTS: {key} -> found '{pat}' match in {d}/{fname}")
                    break

# Check also for the science.nasa.gov blog URLs
print("\n=== Check for science.nasa.gov articles ===")
for f in glob.glob('content/news/*.md') + glob.glob('content/blog/*.md'):
    with open(f) as fh:
        content = fh.read()
    if 'science.nasa.gov' in content:
        for line in content.split('\n')[:5]:
            if line.startswith('title:'):
                print(f"  {os.path.basename(f)}: {line.strip()}")
                break

# Check if the "longest drive on another world" is already written (Perseverance)
print("\n=== Check for longest drive / tracks ===")
for f in glob.glob('content/news/*.md') + glob.glob('content/blog/*.md'):
    with open(f) as fh:
        content = fh.read().lower()
    if 'longest drive' in content or 'tracks along' in content or 'drive on another world':
        for line in content.split('\n')[:5]:
            if line.startswith('title:'):
                print(f"  {os.path.basename(f)}: {line.strip()}")
                break
