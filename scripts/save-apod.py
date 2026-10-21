#!/usr/bin/env python3
"""Download NASA APOD Cassiopeia article for cross-checking. Tirith-safe: arg-list subprocess."""
import subprocess
url = "https://science.nasa.gov/image-article/apod-2026-october-21-new-ghosts-revealed-in-cassiopeia/"
out = "/tmp/cassiopeia-apod.html"
subprocess.run(["curl", "-sS", "--compressed", "--max-time", "30",
                "-A", "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)",
                url, "-o", out], check=True)
print("WROTE", out, "bytes:", len(open(out, errors='ignore').read()))
