"""Parse arXiv Atom XML feed and print entries."""
import sys
import xml.etree.ElementTree as ET

xml_path = sys.argv[1]
tree = ET.parse(xml_path)
root = tree.getroot()
ns = {'atom': 'http://www.w3.org/2005/Atom'}
count = 0
for entry in root.findall('atom:entry', ns):
    title_el = entry.find('atom:title', ns)
    id_el = entry.find('atom:id', ns)
    summary_el = entry.find('atom:summary', ns)
    title = title_el.text.strip() if title_el is not None and title_el.text else 'N/A'
    url = id_el.text.strip() if id_el is not None and id_el.text else 'N/A'
    summary = summary_el.text.strip()[:400] if summary_el is not None and summary_el.text else ''
    print(f'TITLE: {title}')
    print(f'URL: {url}')
    print(f'SUMMARY: {summary}')
    print('---')
    count += 1
print(f'Total entries: {count}')
