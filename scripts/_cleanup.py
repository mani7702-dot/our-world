#!/usr/bin/env python3
"""Clean up scratch scripts from this aborted run. File-based (Tirith-safe)."""
import os
ROOT = "/home/ubuntu/our-world"
SCRIPTS = [
    "scripts/check-candidates2.py",
    "scripts/check-wiki-facts.py",
    "scripts/fetch-wiki-summaries.py",
    "scripts/factcheck-lakes.py",
    "scripts/parse-lakes.py",
]
for s in SCRIPTS:
    p = os.path.join(ROOT, s)
    if os.path.exists(p):
        os.remove(p)
        print(f"removed {s}")
    else:
        print(f"already gone {s}")
print("done")
