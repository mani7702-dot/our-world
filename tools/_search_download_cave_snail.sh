#!/bin/bash
# Search Wikimedia Commons for cave snail images, validate, download, and patch frontmatter.
set -e

SLUG="2026-10-24-ghostly-eyeless-snail-chinese-cave"
FP="content/news/${SLUG}.md"
OUTDIR="assets/images"
mkdir -p "$OUTDIR"

UA="OurWorldSite/1.0 (contact: andugulamani722@gmail.com)"

echo "Searching Commons for: cave snail eyeless freshwater gastropod"
SEARCH_RESP=$(curl -s -L -A "$UA" "https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search&gsrsearch=cave%20snail%20eyeless%20freshwater%20gastropod&gsrnamespace=6&gsrlimit=15")

echo "$SEARCH_RESP" > _tmp_commons_search.json

python3 scripts/_commons_validate_download.py "$SLUG" "$FP" "$OUTDIR" "$UA"
