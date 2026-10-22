#!/usr/bin/env python3
"""Tirith-safe link checker: every href on this page resolves on disk; skip ?query URLs and http(s) external (except svg)."""
import os, re, sys, html
ROOT="/home/ubuntu/our-world"
target="news/dinosaur-antarctica-fossil-drawer-titanosaur.html"
path=os.path.join(ROOT,target)
print("Checking:", target)
txt=open(path,encoding="utf-8",errors="replace").read()
hrefs=re.findall(r'href="([^"]+)"', txt)
# dedupe preserving order
seen=[]; bad=[]
for h in hrefs:
    if h in seen: continue
    seen.append(h)
    if h.startswith("#") or h.startswith("?"): continue
    if h.startswith("http://www.w3.org"): continue
    h=h.strip()
    if h.startswith("mailto:") or h.startswith("tel:"): continue
    if h.startswith("data:"): continue
    # normalize backslashes
    h=h.replace("\\","/")
    # skip query-string routes (client-side JS search)
    if "?" in h: continue
    # external http(s)
    if re.match(r'https?://', h):
        # external is fine for a source link; flag but don't fail
        print(f"  EXTERNAL-OK: {h[:80]}")
        continue
    # resolve relative to the page's directory
    pagedir=os.path.dirname(path)
    resolved=os.path.normpath(os.path.join(pagedir, h))
    rel=resolved[len(ROOT)+1:]
    if not os.path.exists(resolved):
        bad.append(rel)
        print(f"  BAD: {rel}")
    else:
        print(f"  OK: {rel}")
if bad:
    print(f"\nBROKEN ({len(bad)}):", bad)
    sys.exit(1)
else:
    print(f"\nResolved {len([1 for h in seen if not h.startswith('#') and not h.startswith('?') and not h.startswith('mailto')])} hrefs, 0 broken filesystem refs.")
    sys.exit(0)
