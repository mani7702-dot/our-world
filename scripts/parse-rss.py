"""Parse an RSS XML file and print all item titles/urls/descriptions."""
import sys
import xml.etree.ElementTree as ET

xml_path = sys.argv[1]
tree = ET.parse(xml_path)
root = tree.getroot()
count = 0
for item in root.iter('item'):
    title = (item.findtext('title') or '').strip()
    link = (item.findtext('link') or '').strip()
    desc = (item.findtext('description') or '').strip()[:250]
    pub = (item.findtext('pubDate') or '').strip()
    print(f'TITLE: {title}')
    print(f'URL: {link}')
    print(f'DATE: {pub}')
    print(f'DESC: {desc}')
    print('---')
    count += 1
print(f'Total items: {count}')
