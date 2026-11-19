"""Check whether measured orthographic spans admit one rigid length, width and height."""

import argparse
import json
import math


VIEWS = {
    "plan": ("length", "width"),
    "side": ("length", "height"),
    "end": ("width", "height"),
}


def span_ratio(spans, error):
    a, b = spans
    return {
        "value": a / b,
        "range": [(a - error) / (b + error), (a + error) / (b - error)],
    }


def overlaps(first, second):
    lo, hi = max(first[0], second[0]), min(first[1], second[1])
    return lo <= hi or math.isclose(lo, hi, rel_tol=1e-12)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name, axes in VIEWS.items():
        parser.add_argument("--" + name, nargs=2, type=float, metavar=tuple(a.upper() + "_PX" for a in axes))
    parser.add_argument("--span-error-px", type=float, required=True,
                        help="Absolute uncertainty of each measured full pixel span, in its source image")
    parser.add_argument("--envelope", nargs=3, type=float, metavar=("L", "W", "H"),
                        help="Approved full extents in one common physical unit")
    args = parser.parse_args()
    error = args.span_error_px
    if not math.isfinite(error) or error < 0:
        parser.error("span error must be finite and non-negative")
    measured = {name: getattr(args, name) for name in VIEWS if getattr(args, name) is not None}
    if not measured or (len(measured) < 3 and args.envelope is None):
        parser.error("supply all three views for closure, or at least one view and an approved envelope")
    if any(not math.isfinite(v) or v <= error for spans in measured.values() for v in spans):
        parser.error("each span must be finite and larger than its uncertainty")
    if args.envelope and any(not math.isfinite(v) or v <= 0 for v in args.envelope):
        parser.error("physical extents must be finite and positive")

    dimensions = dict(zip(("length", "width", "height"), args.envelope or []))
    ratios = {}
    conflicts = []
    for name, spans in measured.items():
        first, second = VIEWS[name]
        row = span_ratio(spans, error)
        row["axes"] = [first, second]
        row["spans_px"] = spans
        if dimensions:
            target = dimensions[first] / dimensions[second]
            row["approved_ratio"] = target
            inferred = dimensions[first] / row["value"]
            row["inferred_" + second] = inferred
            row[second + "_difference"] = inferred - dimensions[second]
            if not overlaps(row["range"], [target, target]):
                conflicts.append(name)
        ratios[name] = row

    report = {"span_error_px": error, "approved_extents": dimensions, "views": ratios}
    if len(ratios) == 3:
        side, end = ratios["side"], ratios["end"]
        implied = [side["range"][0] / end["range"][1], side["range"][1] / end["range"][0]]
        report["length_over_width_from_side_and_end"] = {
            "value": side["value"] / end["value"], "range": implied,
        }
        if not overlaps(ratios["plan"]["range"], implied):
            conflicts.append("three_view_closure")
    report["conflicts"] = conflicts
    print(json.dumps(report, indent=2, allow_nan=False))
    return 1 if conflicts else 0


if __name__ == "__main__":
    raise SystemExit(main())
