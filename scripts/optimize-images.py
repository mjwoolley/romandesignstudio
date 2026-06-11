#!/usr/bin/env python3
"""Optimize images in images/ for web: fix orientation, cap width, re-encode JPEG.

Usage: python3 scripts/optimize-images.py [file ...]
With no args, processes every .jpg/.jpeg/.png in images/.
"""
import sys, os, glob
from PIL import Image, ImageOps

MAX_W = 1600       # generous for full-width retina display
QUALITY = 82

def optimize(path):
    before = os.path.getsize(path)
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    out = os.path.splitext(path)[0] + ".jpeg"
    im.save(out, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    if out != path:
        os.remove(path)
    after = os.path.getsize(out)
    print(f"{out}: {before//1024} KB -> {after//1024} KB ({im.width}x{im.height})")

def main():
    files = sys.argv[1:] or [f for ext in ("jpg", "jpeg", "png")
                             for f in glob.glob(f"images/*.{ext}")]
    for f in files:
        optimize(f)

if __name__ == "__main__":
    main()
