#!/usr/bin/env python3
import os, glob, re

# Deep check: hurricane Isaias, extratropical cyclone Iceland
keywords = ['isaias', 'extratropical', 'iceland.*cyclone', 'cyclone.*iceland', 
            '205 kilometer', '128 mile.*wind', 'winds.*iceland', 'hurricane.*2026',
            'north atlantic.*cyclone', 'noaa-21.*viirs.*iceland']

for d in ['content/news', 'content/blog']:
    for f in glob.glob(f'{d}/*.md'):
        with open(f) as fh:
            content = fh.read().lower()
        fname = os.path.basename(f)
        for kw in keywords:
            if re.search(kw, content):
                print(f"EXISTS: '{kw}' match in {d}/{fname}")
                # show title
                for line in content.split('\n')[:5]:
                    if line.startswith('title:'):
                        print(f"  TITLE: {line.strip()}")
                break

print("\n=== Done ===")
