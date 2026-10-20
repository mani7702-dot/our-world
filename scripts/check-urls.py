#!/usr/bin/env python3
"""Tirith-safe extractor for arXiv search + ESA/Hubble pages."""
import re, subprocess, sys

def fetch(url, timeout=20):
    r = subprocess.run(['curl', '-s', '--compressed', '--max-time', str(timeout),
                        '-A', 'Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)', url],
                       capture_output=True, text=True)
    return r.stdout

def check_urls(urls):
    for u in urls:
        html = fetch(u)
        title = re.search(r'<title>(.*?)</title>', html, re.I|re.S)
        print(f'{u} -> {title.group(1).strip() if title else "??"} ({len(html)} bytes)')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: check-urls.py <url1> [url2 ...]")
        sys.exit(2)
    check_urls(sys.argv[1:])
