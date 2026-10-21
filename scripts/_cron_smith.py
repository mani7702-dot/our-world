import xml.etree.ElementTree as ET
# Smithsonian has bad XML chars; strip non-XML-safe bytes
import re
raw = open("/tmp/smith.xml", encoding="utf-8", errors="ignore").read()
raw = re.sub(r"[^\x09\x0A\x0D\x20-\x{D7FF}\x{E000}-\x{FFFD}]+", "", raw)
try:
    root = ET.fromstring(raw)
except Exception as e:
    print("PARSE ERR:", e); raise SystemExit
for it in root.iter("item"):
    t=(it.findtext("title") or "").strip()
    l=(it.findtext("link") or "").strip()
    d=(it.findtext("description") or "").strip()
    d=re.sub(r"<[^>]+>","",d)
    print(t[:140]); print("  "+l[:160]); print("  "+d[:300]); print()
