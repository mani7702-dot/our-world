#!/usr/bin/env python3
"""Fetch a NASA article to a file for cross-checking (Tirith-safe: subprocess curl as arg list)."""
import subprocess, sys
url = sys.argv[1]
out = sys.argv[2]
subprocess.run(["curl", "-sS", "--compressed", "--max-time", "30",
                "-A", "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)",
                url, "-o", out], check=True)
print("WROTE", out)
