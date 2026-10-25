import urllib.request, os

# Choose the image: Starr 011025-0021 Clusia rosea (CC BY 3.0, shows leaves, Forest & Kim Starr)
img_url = "https://upload.wikimedia.org/wikipedia/commons/1/19/Starr_011025-0021_Clusia_rosea.jpg"
slug = "2026-10-25-tropical-trees-breathe-at-night-cam-photosynthesis"
out_path = f"/home/ubuntu/our-world/assets/images/{slug}.jpg"

req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0 (compatible; OurWorldBot/1.0)'})
resp = urllib.request.urlopen(req, timeout=60)
img_data = resp.read()

os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, 'wb') as f:
    f.write(img_data)

print(f"Downloaded {len(img_data)} bytes to {out_path}")

# Check it's a valid JPEG
print(f"First bytes: {img_data[:4].hex()}")
