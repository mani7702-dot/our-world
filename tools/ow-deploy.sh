#!/usr/bin/env bash
# One-shot deploy for Our World cron agents: sync, build, link-check, commit, push, verify.
# Usage: bash tools/ow-deploy.sh "<commit message>" "<article-slug>"
# Exit 0 = deployed+verified; nonzero = failed.
#
# WHY THIS ORDER: the previous version ran `git pull --rebase` FIRST. Git refuses to
# rebase with unstaged changes, so any leftover edit (e.g. tools/fetch-images.py) made
# every run die at step 1 with "cannot pull with rebase" and nothing ever shipped.
# We now commit local work BEFORE syncing, and autostash build artifacts.
set -uo pipefail
MSG="${1:-publish}"; SLUG="${2:-}"

echo "[1/6] commit local work"
git add -A
git commit -q -m "$MSG" 2>/dev/null && echo "  committed" || echo "  (nothing new to commit)"

echo "[2/6] sync with origin"
if ! git pull --rebase --autostash origin main; then
  # A conflict in a *generated* file is expected when two agents publish at once.
  # Content sources (content/, tools/) are the real work — keep those, drop generated HTML.
  echo "  WARN: rebase conflict; keeping content/ + tools/, regenerating the rest"
  git rebase --abort 2>/dev/null || true
  git stash push -u -m ow-deploy-keep -- content tools 2>/dev/null || true
  git reset --hard origin/main
  git stash pop 2>/dev/null || echo "  (kept nothing from the conflicted run)"
fi

echo "[3/6] build"
python3 build.py >/tmp/ow-build.log 2>&1 || { echo "ERROR: build failed"; tail -5 /tmp/ow-build.log; exit 3; }

echo "[4/6] link check"
breaks=$(python3 - <<'EOF'
import os, re
for dp, _, fs in os.walk('.'):
    if any(p in dp for p in ('/content', '/templates', '/tools', '.git')):
        continue
    for f in fs:
        if not f.endswith('.html') or f.startswith('.tmp'):
            continue
        s = open(os.path.join(dp, f), encoding='utf-8', errors='ignore').read()
        for m in re.findall(r'(?:href|src)="([^"]+)"', s):
            u = m.replace('\\', '/')
            if u.startswith(('http', '//', 'data:', '#', 'mailto:')) or '{{' in u or '?' in u:
                continue
            if not os.path.exists(os.path.normpath(os.path.join(dp, u))):
                print("%s->%s" % (f, u))
EOF
)
if [ -n "$breaks" ]; then echo "ERROR: broken links:"; echo "$breaks"; exit 4; fi

echo "[5/6] commit build output + push"
git add -A
git commit -q -m "$MSG (build)" 2>/dev/null || echo "  (build produced no diff)"
if ! git push origin main; then
  echo "  push rejected — re-syncing once"
  git pull --rebase --autostash origin main && git push origin main \
    || { echo "ERROR: push failed"; exit 6; }
fi

echo "[6/6] verify live"
if [ -n "$SLUG" ]; then
  sleep 75
  for section in news blog; do
    url="https://mani7702-dot.github.io/our-world/${section}/${SLUG}.html"
    code=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    echo "  live: $code  $url"
    if [ "$code" = "200" ]; then
      # Tell indexers immediately (IndexNow is free, no account; Bing/Yandex within hours).
      curl -s -o /dev/null -w "  indexnow: %{http_code}\n" -X POST \
        -H "Content-Type: application/json; charset=utf-8" \
        -d "{\"host\":\"mani7702-dot.github.io\",\"key\":\"afd35788d7f52e6d423daf2f10f0a1c1\",\"keyLocation\":\"https://mani7702-dot.github.io/our-world/afd35788d7f52e6d423daf2f10f0a1c1.txt\",\"urlList\":[\"$url\"]}" \
        https://api.indexnow.org/indexnow
      echo "DONE"
      exit 0
    fi
  done
  echo "ERROR: article not live after 75s"
  exit 7
fi
echo "DONE"
