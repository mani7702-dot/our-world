import xml.etree.ElementTree as ET
raw = open("/tmp/smith.xml", "rb").read()
raw = raw.replace(b"\x00", b"").replace(b"\x01", b"")
# Try incremental parse to skip bad chars
lines = []
root = ET.fromstring(raw, parser=ET.XMLParser(recover=True) if hasattr(ET, "XMLParser") else ET.XMLParser())
