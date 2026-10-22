#!/usr/bin/env python3
import os, glob, re

# Check Mars mission launch details - the BBC article might be about a NEW launch
# The existing articles are about JAXA MMX (2024 launch). BBC article date is Oct 2026.
# Let me check the existing MMX article dates
for f in ['content/news/japan-mmx-mars-phobos-sample-mission-launches.md', 
          'content/news/mmx-mars-phobos-sample.md']:
    with open(f) as fh:
        for line in fh:
            if line.startswith('date:') or line.startswith('title:'):
                print(f"{f}: {line.strip()}")

# Check if BBC article "Mission blasts off for Mars" is about a different mission
print("\n=== Mars mission articles in content ===")
for f in glob.glob('content/news/*.md') + glob.glob('content/blog/*.md'):
    with open(f) as fh:
        content = fh.read()
    if re.search(r'mmx|phobos|mars.*moon|martian moon', content, re.IGNORECASE):
        for line in content.split('\n')[:5]:
            if line.startswith('title:') or line.startswith('date:'):
                print(f"  {os.path.basename(f)}: {line.strip()}")

# Check for any article about Oct 2026 Mars mission launches
print("\n=== Articles with date 2026-10-22 ===")
for f in glob.glob('content/news/*.md') + glob.glob('content/blog/*.md'):
    with open(f) as fh:
        for line in fh:
            if 'date: 2026-10-22' in line:
                print(f"  {os.path.basename(f)}")

# Check cleaning air / global warming articles
print("\n=== Air cleanup / global warming articles ===")
for f in glob.glob('content/news/*.md') + glob.glob('content/blog/*.md'):
    with open(f) as fh:
        content = fh.read().lower()
    if 'cleaning up the air' in content or 'global warming' in content and 'aerosol' in content:
        for line in content.split('\n')[:5]:
            if line.startswith('title:'):
                print(f"  {os.path.basename(f)}: {line.strip()}")
                break
