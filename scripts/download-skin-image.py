#!/usr/bin/env python3
"""Download the CC BY skin stem cell image and fill in frontmatter."""
import urllib.request, io, os

url = "https://upload.wikimedia.org/wikipedia/commons/0/01/Location_of_multipotent_stem_cells_with_neurogenic_potential_in_facial_and_trunk_skin..jpg"
UA = "OurWorldSite/1.0 (contact: andugulamani722@gmail.com)"

req = urllib.request.Request(url, headers={"User-Agent": UA})
resp = urllib.request.urlopen(req, timeout=45)
data = resp.read()
print(f"Downloaded {len(data)} bytes from {url[:80]}...")

os.makedirs("assets/images", exist_ok=True)
out = "assets/images/skin-cells-play-different-rules-boys-vs-girls-mice-study.jpg"
with open(out, "wb") as f:
    f.write(data)
print(f"Wrote {out}")

# Now check the image file
print(f"File size: {os.path.getsize(out)} bytes")
