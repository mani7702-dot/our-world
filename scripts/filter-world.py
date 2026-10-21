#!/usr/bin/env python3
import re, sys
import xml.etree.ElementTree as ET

xml_file = sys.argv[1] if len(sys.argv) > 1 else "/tmp/bbc-world.xml"
tree = ET.parse(xml_file)
root = tree.getroot()

BLOCK_KW = [
    'war', 'killed', 'death', 'attack', 'court', 'lawsuit', 'politic', 'terror',
    'bomb', 'shooting', 'ebola', 'disease', 'covid', 'trump', 'putin', 'ukraine',
    'yemen', 'sudan', 'france', 'macron', 'rioting', 'protest', 'drone', 'missile',
    'behead', 'murder', 'assault', 'prison', 'ira', 'alberta', 'canada', 'kenya',
    'cult', 'gambia', 'jammeh', 'jail', 'charged', 'convicted', 'fraud', 'looter',
    'looting', 'stalking', 'illegal', 'deport', 'migrant', 'openai', 'saudi',
    'probe', 'investigation', 'clashes', 'violent', 'riot', 'demonstration',
    'democracy', 'dictator', 'regime', 'military', 'forces', 'army', 'navy',
]

for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    if not t:
        continue
    tl = t.lower()
    skip = False
    for kw in BLOCK_KW:
        if kw in tl:
            skip = True
            break
    if not skip:
        link = (it.findtext("link") or "").strip()
        desc = (it.findtext("description") or "").strip()[:150]
        print(f"TITLE: {t}")
        print(f"  URL: {link}")
        print(f"  DESC: {desc}")
        print()
