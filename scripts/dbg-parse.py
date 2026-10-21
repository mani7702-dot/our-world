#!/usr/bin/env python3
import re
text = open("/home/ubuntu/our-world/content/news/history-solar-storm-train-delay-typo.md").read()
m = re.match(r'^---\s*\n(.*?)\n---\s*\n?(.*)$', text, re.S)
if not m:
    print("NO FRONTMATTER MATCH")
else:
    print("fm group1 len:", len(m.group(1)))
    for line in m.group(1).split("\n"):
        if ":" in line:
            k = line.split(":",1)[0].strip()
            v = line.split(":",1)[1].strip()[:60]
        else:
            k = "(none-colon)"
            v = line[:60]
        print(f"  {k!r}: {v!r}")
    print("grownups in meta?:", "for-grownups" in m.group(1))
    print("body starts:", repr(m.group(2)[:40]))
