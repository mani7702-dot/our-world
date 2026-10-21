#!/usr/bin/env python3
"""Filter ScienceDaily XML for space/astronomy stories."""
import xml.etree.ElementTree as ET, sys
path = sys.argv[1] if len(sys.argv) > 1 else "/tmp/sdi.xml"
root = ET.parse(path).getroot()
keywords = ['nasa', 'space', 'telescope', 'astronom', 'cosmic', 'galaxy', 'star', 'planet', 'moon', 'mars',
            'orbit', 'satellite', 'spacecraft', 'black hole', 'neutron', 'pulsar', 'supernova',
            'nebula', 'cosmos', 'universe', 'big bang', 'dark matter', 'dark energy', 'exoplanet',
            'quasar', 'gravity wave', 'hubble', 'webb', 'james', 'first five minutes', 'quantum limit',
            'dyson sphere', 'white dwarf', 'supermassive']
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    l = (it.findtext("link") or "").strip()
    tl = t.lower()
    if any(k in tl for k in keywords):
        print(f"[{t}] | {l}")
