#!/usr/bin/env python3
import os, glob, re

results = []
for d in ['content/news', 'content/blog']:
    for f in glob.glob(f'{d}/*.md'):
        date = ''
        slug = os.path.splitext(os.path.basename(f))[0]
        with open(f) as fh:
            for line in fh:
                if line.startswith('date:'):
                    date = line.split(':',1)[1].strip()
                if line.startswith('time:'):
                    t = line.split(':',1)[1].strip()
                    break
        results.append((date, slug, d))

results.sort(reverse=True)
for date, slug, d in results[:30]:
    print(f"{date} {d}/{slug}")
