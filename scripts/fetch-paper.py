#!/usr/bin/env python3
"""Fetch and extract the original paper from MDPI Galaxies."""
import subprocess, re, html as htmllib

UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
url = 'https://www.mdpi.com/2075-5391/12/3/30'
r = subprocess.run(['curl', '-s', '--compressed', '--max-time', '25', '-A', UA, '-L', url],
                   capture_output=True, text=True)
print(f"Bytes: {len(r.stdout)}")
title = re.search(r'<title>(.*?)</title>', r.stdout, re.I|re.S)
print(f"TITLE: {title.group(1).strip() if title else '???'}")
# Extract abstract
text = re.sub(r'<script[^>]*>.*?</script>', '', r.stdout, flags=re.S|re.I)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.S|re.I)
# Look for abstract section
abstract_match = re.search(r'abstract.*?(?=keywords|1\.|<h[1-6])', text, re.S|re.I)
if abstract_match:
    abstract_text = re.sub(r'<[^>]+>', ' ', abstract_match.group())
    abstract_text = htmllib.unescape(abstract_text).strip()
    abstract_text = re.sub(r'\s+', ' ', abstract_text)
    print(f"\nABSTRACT:\n{abstract_text[:2000]}")
else:
    # Get paragraphs
    paras = re.findall(r'<p[^>]*>(.*?)</p>', text, re.S|re.I)
    for p in paras:
        clean = re.sub(r'<[^>]+>', '', p)
        clean = htmllib.unescape(clean).strip()
        if len(clean) > 80 and ('black' in clean.lower() or 'orbit' in clean.lower() or 'jet' in clean.lower() or 'mrk' in clean.lower()):
            print(f"\nPARA: {clean[:500]}")
