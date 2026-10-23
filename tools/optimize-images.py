#!/usr/bin/env python3
"""Downsize Our World's article images in place, keeping every filename identical.

Why: assets/images was 104 MB, with single hero images up to 3.8 MB. Every article page
embeds one at width 1200, so anything wider is wasted bytes on a phone. Google also uses
page-experience signals, and a 3.7 MB LCP image is a straightforward ranking drag.

Safety:
  * Filenames never change, so no HTML/markdown reference can break.
  * Images already inside the size/quality budget are left byte-identical.
  * The original file is only replaced after the new encode succeeds.
  * --dry-run reports what would change without writing anything.

Usage:
  python tools/optimize-images.py --dry-run
  python tools/optimize-images.py
"""
import argparse
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES = os.path.join(ROOT, "assets", "images")

MAX_W = 1200          # article body renders at width=1200
MAX_H = 1200
JPEG_Q = 82           # visually lossless for photos at this size
PNG_MAX_BYTES = 400 * 1024   # PNGs stay PNG (alpha) but get optimized
SKIP_UNDER = 120 * 1024      # don't churn files that are already small

Image.MAX_IMAGE_PIXELS = None


def target_size(w, h):
    """Scale (w, h) down to fit MAX_W x MAX_H, never scaling up."""
    scale = min(MAX_W / w, MAX_H / h, 1.0)
    return max(1, int(w * scale)), max(1, int(h * scale))


def optimize(path, dry_run):
    before = os.path.getsize(path)
    ext = os.path.splitext(path)[1].lower()
    if ext not in (".jpg", ".jpeg", ".png", ".webp"):
        return None

    try:
        with Image.open(path) as im:
            fmt = im.format
            w, h = im.size
            new_w, new_h = target_size(w, h)
            needs_resize = (new_w, new_h) != (w, h)

            if not needs_resize and before < SKIP_UNDER:
                return None
            if not needs_resize and ext in (".jpg", ".jpeg") and before < 300 * 1024:
                return None
            if not needs_resize and ext == ".png" and before < PNG_MAX_BYTES:
                return None

            im = im.convert("RGB") if fmt == "JPEG" else im
            if needs_resize:
                im = im.resize((new_w, new_h), Image.LANCZOS)

            tmp = path + ".tmp-opt"
            if fmt == "JPEG":
                im.save(tmp, "JPEG", quality=JPEG_Q, optimize=True, progressive=True)
            elif fmt == "PNG":
                im.save(tmp, "PNG", optimize=True)
            else:
                im.save(tmp, "WEBP", quality=JPEG_Q, method=6)

        after = os.path.getsize(tmp)
        if after >= before:
            os.remove(tmp)
            return None
        if dry_run:
            os.remove(tmp)
        else:
            os.replace(tmp, path)
        return (os.path.relpath(path, ROOT), before, after, needs_resize)
    except Exception as exc:                                  # noqa: BLE001
        print("  skip %s (%s)" % (os.path.basename(path), exc))
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not os.path.isdir(IMAGES):
        sys.exit("no images dir at %s" % IMAGES)

    files = sorted(
        os.path.join(IMAGES, f) for f in os.listdir(IMAGES)
        if os.path.isfile(os.path.join(IMAGES, f))
    )
    total_before = sum(os.path.getsize(f) for f in files)
    results = [r for r in (optimize(f, args.dry_run) for f in files) if r]

    saved = sum(b - a for _, b, a, _ in results)
    resized = sum(1 for r in results if r[3])
    print("\n%s" % ("DRY RUN — nothing written" if args.dry_run else "optimized"))
    print("  files scanned : %d" % len(files))
    print("  files changed : %d  (%d resized)" % (len(results), resized))
    print("  before        : %.1f MB" % (total_before / 1048576))
    print("  after         : %.1f MB" % ((total_before - saved) / 1048576))
    print("  saved         : %.1f MB (%.0f%%)" % (
        saved / 1048576, 100.0 * saved / max(total_before, 1)))
    for name, b, a, was_resized in sorted(results, key=lambda r: r[1] - r[2], reverse=True)[:8]:
        print("    %-58s %6.2f -> %5.2f MB%s" % (
            name, b / 1048576, a / 1048576, "  (resized)" if was_resized else ""))


if __name__ == "__main__":
    main()
