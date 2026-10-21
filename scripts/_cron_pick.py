import xml.etree.ElementTree as ET
root = ET.parse("/tmp/sdi.xml")
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    l = (it.findtext("link") or "").strip()
    d = (it.findtext("description") or "").strip()
    # Show only items the scanner flagged MED-BLOCK that are NOT obviously medical
    if "quantum limit" in t.lower() or "microscope reveals living" in t.lower() or "red meat" in t.lower() or "blueberries" in t.lower() or "sleep builds muscle" in t.lower() or "uranium cubes" in t.lower() or "never-ending supply" in t.lower():
        print(t)
        print("  "+l)
        print("  "+d[:400])
        print()
