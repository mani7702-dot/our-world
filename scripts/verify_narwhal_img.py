#!/usr/bin/env python3
"""Verify the downloaded narwhal image."""
import os
from PIL import Image

img_path = "assets/images/2026-10-25-narwhal-tusk-double-helix.jpg"
img = Image.open(img_path)
print(f"File: {img_path}")
print(f"Size: {img.size}")
print(f"Mode: {img.mode}")
print(f"File size: {os.path.getsize(img_path)} bytes")
print(f"Format: {img.format}")
