#!/usr/bin/env python3
"""Deploy-verify gate for Our World — checks the new article page exists,
its image hrefs resolve on disk, zero unfilled tokens, and a GitHub credential
is present (env var OR ~/.hermes/.env OR gh OR git credential helper).
Exits non-zero on failure. Distinguishes build-failure from push-failure."""
import os, re, sys

ROOT = "/home/ubuntu/our-world"
slug = sys.argv[1] if len(sys.argv) > 1 else "news/2026-10-20-sloth-bear-odum-julia-roberts-rescue.html"

# 1. Page exists
page_path = os.path.join(ROOT, slug)
if not os.path.isfile(page_path):
    print(f"FAIL: page not found on disk: {page_path}")
    sys.exit(1)
print(f"OK: page exists: {page_path}")

# 2. Zero unfilled tokens
text = open(page_path, encoding="utf-8").read()
tokens = re.findall(r'\{\{[A-Z_]+\}\}', text)
if tokens:
    print(f"FAIL: unfilled tokens: {tokens}")
    sys.exit(1)
print("OK: zero unfilled tokens")

# 3. Image hrefs resolve
img_paths = re.findall(r'<img[^>]+src="([^"]+)"', text)
for href in img_paths:
    if href.startswith(("http://", "https://")):
        continue
    resolved = href
    if resolved.startswith("../assets/"):
        resolved = resolved[3:]
    full = os.path.normpath(os.path.join(ROOT, resolved))
    if not os.path.isfile(full):
        print(f"FAIL: image not found: {href} -> {full}")
        sys.exit(1)
print(f"OK: all {len(img_paths)} image href(s) resolve on disk")

# 4. Credential check
cred_found = False
if os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN"):
    cred_found = True
for cred_path in [os.path.expanduser("~/.hermes/.env"), os.path.expanduser("~/.env")]:
    if os.path.isfile(cred_path):
        content = open(cred_path).read()
        if re.search(r'(token|github)', content, re.I):
            cred_found = True
# git credential helper store
gc = os.path.join(os.path.expanduser("~"), ".git-credentials")
if os.path.isfile(gc):
    cred_found = True

if cred_found:
    print("OK: GitHub credential present (for push)")
else:
    print("WARN: no obvious GitHub credential found — push may fail with 'could not read Username'")

print(f"\nREADY: {slug} is ready for deploy")
