#!/usr/bin/env bash
# One-shot deploy for Our World cron agents: build, link-check, commit, push, verify.
# Usage: bash tools/ow-deploy.sh "<commit message>" "<article-slug>"
# Exit 0 = deployed+verified; nonzero = failed.
set -uo pipefail
MSG="${1:-publish}"; SLUG="${2:-}"

echo "fetch first"
git fetch origin
git pull --rebase origin main || { echo "ERROR: pull failed"; exit 2; }

echo "build"
python3 build.py >/tmp/ow-build.log 2>&1 || { echo "ERROR: build failed"; tail -5 /tmp/ow-build.log; exit 3; }

echo "link check"
breaks=$(python3 - <<'EOF'
import os, re
for dp,_,fs in os.walk('.'):
    if any(p in dp for p in ('/content','/templates','/tools','.git')): continue
    for f in fs:
        if not f.endswith('.html'): continue
        s=open(os.path.join(dp,f),encoding='utf-8',errors='ignore').read()
        for m in re.findall(r'(?:href|src)="([^"]+)"', s):
            u=m.replace('\\','/')
            if u.startswith(('http','//','data:','#','mailto:')) or '{{' in u: continue
            if not os.path.exists(os.path.normpath(os.path.join(dp,u))): print(f"{f}->{u}")
EOF
)
if [ -n "$breaks" ]; then echo "ERROR: broken links:"; echo "$breaks"; exit 4; fi

echo "commit+push"
git add -A
git commit -q -m "$MSG" || { echo "WARN: nothing to commit"; }
git push origin main || { echo "ERROR: push failed"; exit 6; }

if [ -n "$SLUG" ]; then
  sleep 75
  # explainers land in blog/; news finds land in news/ — check both
  bcode=$(curl -s -o /dev/null -w "%{http_code}" "https://mani7702-dot.github.io/our-world/blog/${SLUG}.html")
  ncode=$(curl -s -o /dev/null -w "%{http_code}" "https://mani7702-dot.github.io/our-world/news/${SLUG}.html")
  echo "live: blog=$bcode news=$ncode"
  [ "$bcode" = "200" -o "$ncode" = "200" ] || { echo "ERROR: live not 200"; exit 7; }
fi
echo "DONE"
