#!/usr/bin/env python3
"""Try DOI resolver and alternative URLs for the paper."""
import subprocess, re

UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
urls = [
    'https://doi.org/10.3390/galaxies12030030',
    'https://www.mdpi.com/2075-5391/12/3/30',
    'https://www.mdpi.com/2075-5391/12/3/30/pdf',
    'https://www.mdpi.com/2075-5391/12/3/30/html',
]
for u in urls:
    r = subprocess.run(['curl', '-s', '--compressed', '--max-time', '25', '-A', UA, '-L', u],
                       capture_output=True, text=True)
    title = re.search(r'<title>(.*?)</title>', r.stdout, re.I|re.S)
    t = title.group(1).strip()[:80] if title else "???"
    print(f'{u} -> {t} ({len(r.stdout)} bytes)')
