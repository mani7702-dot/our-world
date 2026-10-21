#!/usr/bin/env python3
"""Tirith-safe: download the NASA Webb mysterious world story + look for 2nd sources on the planet."""
import subprocess, os
UA = "Mozilla/5.0 (OurWorld; contact andugulamani722@gmail.com)"
primary = "https://www.sciencedaily.com/releases/2026/10/261015073215.htm"
out_primary = "/tmp/wild-weather-primary.html"
# ScienceDaily primary
r = subprocess.run(["curl", "-s", "--compressed", "--max-time", "25", "-A", UA, primary, "-o", out_primary], capture_output=True)
print(f"primary downloaded: {os.path.getsize(out_primary)} bytes")
