#!/usr/bin/env python3
import re, sys
from xml.etree import ElementTree as ET
tree = ET.parse(sys.argv[1])
for it in tree.getroot().iter("item"):
    t = (it.findtext("title") or "").strip()
    l = (it.findtext("link") or "").strip()
    d = re.sub(r"<[^>]+>", "", it.findtext("description") or "").strip()
    print(t); print("  URL:", l); print("  DESC:", d[:220]); print()
