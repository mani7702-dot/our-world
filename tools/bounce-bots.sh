#!/usr/bin/env bash
set -euo pipefail
export PATH="$HOME/.local/bin:$HOME/.npm-global/bin:$PATH"

echo "=== pull latest template + deploy script ==="
cd $HOME/our-world
git fetch origin
git pull --rebase origin main

TP="$HOME/lane-prompt-template.txt"
cat "$TP" | head -1 >/dev/null && echo "template ok ({{CATEGORY}} present): $(grep -c '{{CATEGORY}}' $TP) refs"

make_job() {
  local lane="$1" sched="$2"
  local prompt
  prompt=$(sed "s/{{CATEGORY}}/$lane/g" "$TP")
  # remove old if exists (idempotent)
  hermes cron remove "news-$lane" >/dev/null 2>&1 || true
  hermes cron create "$sched" "$prompt" \
    --name "news-$lane" --deliver telegram --skill our-world-site \
    --workdir $HOME/our-world >/dev/null 2>&1
  echo "created news-$lane ($sched)"
}

make_job science      "*/30 * * * *"
make_job space        "0 * * * *"
make_job animals      "*/25 * * * *"
make_job world        "*/40 * * * *"
make_job history      "0 8 * * *"
make_job explainers  "30 */2 * * *"
make_job listicles    "0 12 * * *"
make_job trending     "0 */2 * * *"

echo "=== verify ==="
hermes cron list 2>&1 | grep -E 'news-|Name|Schedule' || true
