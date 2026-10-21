#!/usr/bin/env python3
"""Parse NASA main feed and print space-relevant titles + links."""
import xml.etree.ElementTree as ET

tree = ET.parse('/tmp/nasa.xml')
root = tree.getroot()
for item in root.iter('item'):
    title = (item.findtext('title') or '').strip()
    link = (item.findtext('link') or '').strip()
    desc = (item.findtext('description') or '')[:200].strip()
    print(f'TITLE: {title}')
    print(f'LINK: {link}')
    print(f'DESC: {desc}')
    print('---')
