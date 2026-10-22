#!/usr/bin/env python3
"""Commit-step: stage ONLY legitimate changes (article + image + regenerated build output),
NOT the diagnostic scratch scripts (_*.py, _*.txt). Then report git status."""
import subprocess, os
ROOT="/home/ubuntu/our-world"
# Files to stage: the article, the fetched image, and regenerated build outputs
stage=[
  "content/news/dinosaur-antarctica-fossil-drawer-titanosaur.md",
  "assets/images/dinosaur-antarctica-fossil-drawer-titanosaur.jpg",
  "news/dinosaur-antarctica-fossil-drawer-titanosaur.html",
  "index.html",
  "news/index.html",
  "feed.xml",
  "sitemap.xml",
  "search-index.json",
  "robots.txt",
]
def run(args):
    r=subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
    return r.returncode, r.stdout.strip(), r.stderr.strip()

# stage the specific files
staging=[]
for f in stage:
    if os.path.exists(os.path.join(ROOT,f)):
        c,o,e=run(["git","add",f])
        staging.append((f,c==0))
        if c!=0: print("STAGE FAIL:",f,e)
    else:
        print("SKIP (missing):",f)
print("\n=== Staged files (git diff --cached --name-only) ===")
osys=os.system
rc,o,e=run(["git","diff","--cached","--name-only"])
print(o)
print("\n=== Untracked/scratch files (must stay untracked) ===")
rc,o,e=run(["git","status","--short"])
print(o)
