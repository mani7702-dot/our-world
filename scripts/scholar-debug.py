#!/usr/bin/env python3
"""Fetch Semantic Scholar info for the paper - debug version."""
import subprocess, json

UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
url = 'https://api.semanticscholar.org/graph/v1/paper/DOI:10.3390/galaxies12030030?fields=title,abstract,year,external_ids,authors,publication_venue'
r = subprocess.run(['curl', '-s', '--compressed', '--max-time', '25', '-A', UA, '-L', url],
                   capture_output=True, text=True)
print(f"stdout: [{r.stdout[:300]}]")
print(f"stderr: [{r.stderr[:300]}]")
print(f"returncode: {r.returncode}")
