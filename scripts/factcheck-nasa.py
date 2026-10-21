#!/usr/bin/env python3
"""Final fact-check: extract key facts from NASA article for cross-verification."""
import re
txt = open("/tmp/nasa-longest-drive.html", encoding="utf-8", errors="ignore").read()
text = re.sub(r'<[^>]+>', ' ', txt)
text = re.sub(r'\s+', ' ', text)

facts = {
    "Perseverance rover on Mars": "perseverance" in text.lower() and "mars" in text.lower(),
    "45.22 kilometers": "45.22" in text,
    "28.10 miles": "28.10" in text,
    "Sol 2006": "2006" in text,
    "October 11 2026": "Oct" in text and "11" in text and "2026" in text,
    "Guinness World Records": "guinness" in text.lower() or "world record" in text.lower(),
    "odometer": "odometer" in text.lower(),
    "AutoNav / Autonomous Navigation": "autonomous navigation" in text.lower() or "autonav" in text.lower(),
    "24 degrees tilt": "24" in text and "tilt" in text.lower(),
    "20 centimeter clearance": "20" in text and "centimeter" in text.lower() or "centimet" in text.lower(),
    "GBLC Global Localization": "global localization" in text.lower() or "gblc" in text.lower(),
    "Navigation Camera": "navigation camera" in text.lower() or "navcam" in text.lower(),
}

for fact, found in facts.items():
    print(f"{'✓' if found else '✗'} {fact}: {found}")

# Extract a snippet about the Guinness record
for m in re.finditer(r'guinness|world record', text, re.IGNORECASE):
    start = max(0, m.start()-100)
    end = min(len(text), m.end()+100)
    print(f"\nSnippet: ...{text[start:end]}...")
    break
