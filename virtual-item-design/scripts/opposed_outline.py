"""Create or verify a top-to-bottom orthographic silhouette on a registered grid."""

import argparse
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter, ImageOps


def read_mask(path):
    with Image.open(path) as source:
        if source.mode not in ("1", "L"):
            raise ValueError(f"{path}: supply an opaque binary mask in mode 1 or L")
        mask = source.convert("L")
    histogram = mask.histogram()
    if sum(histogram[1:255]) or histogram[255] == 0:
        raise ValueError(f"{path}: use 255 for solid geometry and 0 for empty space")
    return mask


def opposite(mask, bow):
    if bow in ("left", "right"):
        return ImageOps.flip(mask)
    return ImageOps.mirror(mask)


def perimeter(mask):
    padded = ImageOps.expand(mask, border=1, fill=0)
    eroded = padded.filter(ImageFilter.MinFilter(3))
    return ImageChops.subtract(padded, eroded).crop((1, 1, mask.width + 1, mask.height + 1))


def compare(expected, actual, overlay_path):
    if expected.size != actual.size:
        raise ValueError(f"Registration grids differ: {expected.size} and {actual.size}")
    missing = ImageChops.subtract(expected, actual)
    extra = ImageChops.subtract(actual, expected)
    missing_px = missing.histogram()[255]
    extra_px = extra.histogram()[255]
    overlap_px = ImageChops.darker(expected, actual).histogram()[255]
    if overlay_path:
        overlay = Image.new("RGB", expected.size, "#faf9f7")
        overlay.paste("#d6dce0", mask=ImageChops.darker(expected, actual))
        overlay.paste("#246653", mask=ImageChops.darker(perimeter(expected), perimeter(actual)))
        overlay.paste("#ba4838", mask=missing)
        overlay.paste("#286bb0", mask=extra)
        overlay.save(overlay_path)
    return {
        "exact": missing_px == 0 and extra_px == 0,
        "grid_px": list(expected.size),
        "expected_bounds_px": expected.getbbox(),
        "actual_bounds_px": actual.getbbox(),
        "missing_px": missing_px,
        "extra_px": extra_px,
        "xor_px": missing_px + extra_px,
        "iou": overlap_px / (overlap_px + missing_px + extra_px),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    stencil = commands.add_parser("stencil", help="Save the reflected binary top mask")
    check = commands.add_parser("check", help="Compare against a mask read from the final bottom image")
    for command in (stencil, check):
        command.add_argument("--top", type=Path, required=True)
        command.add_argument("--bow", choices=("left", "right", "up", "down"), required=True)
    stencil.add_argument("--out", type=Path, required=True)
    check.add_argument("--bottom", type=Path, required=True)
    check.add_argument("--overlay", type=Path)
    check.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        expected = opposite(read_mask(args.top), args.bow)
        if args.command == "stencil":
            expected.save(args.out)
            return 0
        result = compare(expected, read_mask(args.bottom), args.overlay)
        result["bow"] = args.bow
        output = json.dumps(result, indent=2) + "\n"
        if args.report:
            args.report.write_text(output, encoding="utf-8")
        print(output, end="")
        return 0 if result["exact"] else 1
    except (OSError, ValueError) as error:
        parser.exit(2, f"{error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
