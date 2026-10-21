#!/usr/bin/env python3
"""Download remaining CHECK-ME BBC candidates for guardrail verification."""
import subprocess, os
UA = "Mozilla/5.0 (OurWorld; contact andugulamani722@gmail.com)"
urls = {
    "fuel-leak-river-taff": "https://www.bbc.co.uk/news/articles/c6y8lvxzp59vo",
    "kew-palm-house": "https://www.bbc.co.uk/news/videos/c914d43gg2zdo",
}
for slug, url in urls.items():
    out = f"/tmp/bbc-{slug}.html"
    r = subprocess.run(["curl", "-s", "--compressed", "--max-time", "25", "-A", UA, url, "-o", out], capture_output=True)
    sz = os.path.getsize(out) if os.path.exists(out) else 0
    print(f"{slug}: {sz} bytes")
