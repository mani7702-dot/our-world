#!/usr/bin/env python3
import os, glob, re

# Check the spacex iss cargo article to see if it covers the same ground
for f in ['content/news/spacex-crs35-jellyfish-launch.md']:
    with open(f) as fh:
        content = fh.read()
    print(f"=== {f} (title + first 600 chars) ===")
    for line in content.split('\n')[:6]:
        print(line)
    print(content[:600])
    print()
