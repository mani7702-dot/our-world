#!/usr/bin/env python3
"""Load the downloaded narwhal image and encode as base64 for vision check."""
import base64
img_path = "assets/images/2026-10-25-narwhal-tusk-double-helix.jpg"
with open(img_path, "rb") as f:
    data = base64.b64encode(f.read()).decode("ascii")
# Return data URL
print(f"data:image/jpeg;base64,{data[:200]}...")
print(f"Total base64 length: {len(data)}")
# Write to a file for reference
with open("/tmp/narwhal_dataurl.txt", "w") as out:
    out.write(f"data:image/jpeg;base64,{data}")
print("Data URL written to /tmp/narwhal_dataurl.txt (will likely fail on /tmp quota)")
