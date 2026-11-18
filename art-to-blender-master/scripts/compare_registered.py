"""Compare masks and named polylines already registered to one reference image."""
import argparse
import hashlib
import json
from pathlib import Path
import warnings

try:
    import numpy as np
    from PIL import Image, ImageDraw
except (ImportError, OSError):
    raise SystemExit("Comparison requires working NumPy and Pillow installations.") from None


class ComparisonError(ValueError):
    """A diagnostic constructed from fixed text and input roles."""


class ComparisonParser(argparse.ArgumentParser):
    def error(self, message):
        # argparse may include user-supplied paths verbatim in its message.
        self.exit(2, "Invalid command arguments. Use --help to see the accepted options.\n")


def check_label(value, role):
    if (not isinstance(value, str) or not value.strip() or value.strip() in (".", "..")
            or any(not (c.isalnum() or c in " ._-()") for c in value)):
        raise ComparisonError(f"Use a descriptive {role} label without path separators or control characters.")


def mask(role, path):
    try:
        with Image.open(path) as image:
            if image.mode not in ("1", "L"):
                raise ComparisonError(f"The {role} mask must be binary or 8-bit grayscale.")
            return np.asarray(image.convert("L")) >= 128
    except (OSError, Image.DecompressionBombError, Warning):
        raise ComparisonError(f"Cannot read the {role} mask. Check the image and its permissions.") from None


def geometry(binary):
    y, x = np.nonzero(binary)
    if not len(x):
        return {"area_px": 0, "bbox_xyxy_inclusive": None, "centroid_xy": None}
    return {
        "area_px": len(x),
        "bbox_xyxy_inclusive": [int(x.min()), int(y.min()), int(x.max()), int(y.max())],
        "centroid_xy": [round(float(x.mean()), 4), round(float(y.mean()), 4)],
    }


def boundary(binary):
    p = np.pad(binary, 1, constant_values=False)
    return binary & ~(p[:-2, 1:-1] & p[2:, 1:-1] & p[1:-1, :-2] & p[1:-1, 2:])


def curve(coords, closed, valid):
    points = np.asarray(coords, dtype=float)
    if points.ndim != 2 or points.shape[1] != 2 or len(points) < 2 or not np.isfinite(points).all():
        raise ComparisonError("A polyline needs at least two finite x,y points")
    h, w = valid.shape
    if np.any(points < 0) or np.any(points > [w - 1, h - 1]):
        raise ComparisonError("Feature outside the registered canvas")
    if closed and not np.array_equal(points[0], points[-1]):
        points = np.vstack((points, points[0]))
    starts, ends = points[:-1], points[1:]
    lengths = np.linalg.norm(ends - starts, axis=1)
    keep = lengths > 0
    starts, ends, lengths = starts[keep], ends[keep], lengths[keep]
    if not len(lengths) or (closed and len(np.unique(points, axis=0)) < 3):
        raise ComparisonError("Degenerate polyline")
    samples, weights = [], []
    for a, b, length in zip(starts, ends, lengths):
        count = max(1, int(np.ceil(length)))
        fractions = (np.arange(count) + 0.5) / count
        samples.append(a + fractions[:, None] * (b - a))
        weights.append(np.full(count, length / count))
    samples = np.concatenate(samples)
    # Check every pixel touched by the rendered line as well as the subpixel samples.
    drawn = Image.new("1", (w, h))
    ImageDraw.Draw(drawn).line([tuple(p) for p in np.rint(points).astype(int).tolist()], fill=1)
    x, y = np.rint(samples).astype(int).T
    if np.any(np.asarray(drawn) & ~valid) or not valid[y, x].all():
        raise ComparisonError("Feature crosses an excluded region; supply separate visible spans")
    return points, starts, ends, samples, np.concatenate(weights)


def directional_distance(source, target):
    _, _, _, samples, weights = source
    _, starts, ends, _, _ = target
    nearest_sq = np.full(len(samples), np.inf)
    for a, b in zip(starts, ends):
        step = b - a
        delta = samples - a
        t = np.clip(np.sum(delta * step, axis=1) / np.dot(step, step), 0, 1)
        residual = delta - t[:, None] * step
        nearest_sq = np.minimum(nearest_sq, np.sum(residual * residual, axis=1))
    return float(np.average(np.sqrt(nearest_sq), weights=weights))


def compare(args):
    check_label(args.view, "view")
    paths = {"reference": args.reference, "candidate": args.candidate}
    if args.baseline:
        paths["baseline"] = args.baseline
    masks = {name: mask(name, path) for name, path in paths.items()}
    ref = masks["reference"]
    valid = mask("valid", args.valid) if args.valid else np.ones_like(ref)
    if any(m.shape != ref.shape for m in [valid, *masks.values()]):
        raise ComparisonError("Canvas mismatch: prepare all masks with the same saved registration")
    if not (ref & valid).any():
        raise ComparisonError("Reference has no foreground in the visible region")
    versions = ["baseline", "candidate"] if args.baseline else ["candidate"]
    inputs = dict(paths)
    if args.valid:
        inputs["valid"] = args.valid
    if args.features:
        inputs["features"] = args.features
    outputs = [args.out / "metrics.json", args.out / "overlay.png"]
    if {p.resolve() for p in inputs.values()} & {p.resolve() for p in outputs}:
        raise ComparisonError("Output path would overwrite an input")
    report = {
        "view": args.view, "canvas_wh": list(ref.shape[::-1]),
        "inputs": {role: {} for role in inputs},
        "valid_px": int(valid.sum()), "reference": geometry(ref & valid), "versions": {},
        "features": {},
    }
    if args.local_provenance:
        for role, path in inputs.items():
            digest = hashlib.sha256()
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
            report["inputs"][role]["sha256"] = digest.hexdigest()
    panels = {}
    gold, cyan = (255, 192, 56), (48, 221, 232)
    for version in versions:
        model = masks[version]
        inter = np.count_nonzero(ref & model & valid)
        union = np.count_nonzero((ref | model) & valid)
        report["versions"][version] = {**geometry(model & valid), "iou": inter / union,
                                       "intersection_px": int(inter), "union_px": int(union)}
        rgb = np.full((*ref.shape, 3), (21, 26, 32), dtype=np.uint8)
        rgb[(ref | model) & valid] = (59, 67, 71)
        rgb[~valid] = (42, 41, 50)
        re, me = boundary(ref) & valid, boundary(model) & valid
        rgb[re], rgb[me], rgb[re & me] = gold, cyan, (239, 244, 237)
        panels[version] = Image.fromarray(rgb)
    features = []
    if args.features:
        try:
            features = json.loads(args.features.read_text(encoding="utf-8-sig"))
        except (ValueError, OSError):
            raise ComparisonError("Cannot read the features input as UTF-8 JSON.") from None
    if not isinstance(features, list) or (args.features and not features):
        raise ComparisonError("Feature file must contain a non-empty list")
    for feature in features:
        name = feature["name"]
        check_label(name, "feature")
        if name in report["features"]:
            raise ComparisonError("Each feature needs a unique non-empty name")
        closed = feature.get("closed", False)
        if not isinstance(closed, bool):
            raise ComparisonError("A feature's closed field must be a JSON boolean")
        source = curve(feature["reference"], closed, valid)
        measures = {}
        for version in versions:
            target = curve(feature[version], closed, valid)
            measures[version] = (directional_distance(source, target) + directional_distance(target, source)) / 2
            draw = ImageDraw.Draw(panels[version])
            for line, color in [(source[0], gold), (target[0], cyan)]:
                draw.line([tuple(p) for p in line.tolist()], fill=color, width=2)
        report["features"][name] = {"closed": closed, "symmetric_mean_px": measures}
    w, h = ref.shape[::-1]
    board = Image.new("RGB", (w * len(versions), h + 20), (21, 26, 32))
    for i, version in enumerate(versions):
        board.paste(panels[version], (w * i, 20))
        ImageDraw.Draw(board).text((w * i + 3, 2), version, fill=(239, 244, 237))
    args.out.mkdir(parents=True, exist_ok=True)
    board.save(outputs[1])
    outputs[0].write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf8")


def main():
    parser = ComparisonParser(prog="compare_registered", description=__doc__, allow_abbrev=False)
    parser.add_argument("--local-provenance", action="store_true",
                        help="include input SHA-256 fingerprints in this local report")
    parser.add_argument("--view", required=True)
    for key in ("reference", "candidate", "baseline", "valid", "features", "out"):
        parser.add_argument("--" + key, type=Path, required=key in ("reference", "candidate", "out"))
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            compare(parser.parse_args())
    except ComparisonError as exc:
        parser.exit(1, f"Comparison failed: {exc}\n")
    except OSError:
        parser.exit(1, "Comparison failed: check input and output permissions and available space.\n")
    except (ValueError, TypeError, KeyError, IndexError, OverflowError):
        parser.exit(1, "Comparison failed: check the feature fields and numeric coordinates.\n")
    except Exception:
        # Decoder and library exceptions can contain filenames or raw input data.
        parser.exit(1, "Comparison failed while processing the supplied data.\n")


if __name__ == "__main__":
    main()
