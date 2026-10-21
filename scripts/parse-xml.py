import xml.etree.ElementTree as ET
import sys

path = sys.argv[1]
root = ET.parse(path).getroot()
for it in root.iter('item'):
    t = (it.findtext('title') or '').strip()
    l = (it.findtext('link') or '').strip()
    d = (it.findtext('description') or '').strip()[:200]
    print('TITLE:', t)
    print('URL:', l)
    print('DESC:', d)
    print('---')
