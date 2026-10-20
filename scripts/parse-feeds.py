"""Parse saved RSS XML files and print all headlines + URLs."""
import sys
import xml.etree.ElementTree as ET

files = [
    ("/tmp/sd.xml", "SD"),
    ("/tmp/bbc.xml", "BBC"),
]
for f, label in files:
    try:
        root = ET.parse(f).getroot()
    except Exception as e:
        print(f"{label}: parse error {e}")
        continue
    for it in root.iter("item"):
        t = (it.findtext("title") or "").strip()
        u = (it.findtext("link") or "").strip()
        if t and len(t) > 25:
            print(f"{label}: {t} | {u}")
