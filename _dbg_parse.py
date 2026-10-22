import xml.etree.ElementTree as ET
root = ET.parse('/tmp/feed-science-0.xml').getroot()
print('root tag:', root.tag)
items = list(root.iter('item'))
print('item count via iter:', len(items))
print('first 500 chars of root:')
print(ET.tostring(root)[:500])
