#!/usr/bin/env python3
"""Try to fetch the original scientific paper from A&A using DOI redirect."""
import subprocess, re

UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"

# Try A&A article page - the DOI should resolve
urls = [
    # A&A paper based on the ScienceDaily attribution to Max Planck Institute for Radio Astronomy
    # The paper is likely in A&A 2024 or MNRAS 2024
    'https://www.aanda.org/articles/aa/abs/2024/11/aa50560-24.html',
    'https://www.aanda.org/articles/aa/full_html/2024/11/aa50560-24.html',
    'https://www.aanda.org/articles/aa/abs/2026/01/aa50560-24.html',
    # Try DOI resolver
    'https://doi.org/10.1051/0004-6361/202450560',
    # Try arXiv for the paper
    'https://arxiv.org/abs/2409.15076',
    'https://arxiv.org/abs/2410.12345',
]

for u in urls:
    r = subprocess.run(['curl', '-s', '--compressed', '--max-time', '20', '-A', UA, '-L', u],
                       capture_output=True, text=True)
    title = re.search(r'<title>(.*?)</title>', r.stdout, re.I|re.S)
    t = title.group(1).strip()[:80] if title else "???"
    print(f'{u}')
    print(f'  -> {t} ({len(r.stdout)} bytes)')
