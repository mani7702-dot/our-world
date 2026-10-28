import subprocess
url = "https://mani7702-dot.github.io/our-world/news/2026-10-28-mysterious-dwarf-planet-candidate-beyond-neptune.html"
# Get the page and check for key content
p = subprocess.run(
    ["curl", "-sL", "--max-time", "30", "-A",
     "Mozilla/5.0 (compatible; OurWorld/1.0; contact andugulamani722@gmail.com)", url],
    capture_output=True, text=True
)
html = p.stdout
print(f"Page length: {len(html)}")
# Check for key content
for kw in ["2026 ED138", "dwarf planet", "Rubin Observatory", "Neptune", "image", "neptune.png"]:
    if kw in html:
        print(f"  Found: '{kw}'")
    else:
        print(f"  MISSING: '{kw}'")

# Check the image tag
import re
imgs = re.findall(r'<img[^>]*src="([^"]+)"[^>]*>', html)
for img in imgs:
    print(f"  Image: {img}")