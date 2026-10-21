import xml.etree.ElementTree as ET, sys
root = ET.parse(sys.argv[1])
for it in root.iter("item"):
    print(it.findtext("title","").strip()[:160])
    print("  "+(it.findtext("link","")).strip()[:200])
    print("  "+(it.findtext("description","")).strip()[:220])
