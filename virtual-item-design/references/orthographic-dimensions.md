# Resolving dimensions across orthographic views

Use this procedure for a rigid item in one state when the drawings will govern fit, a master sheet or a modeling handoff. Run it before accepting the first dimensioned set, when a controlling view or dimension changes, or when a blockout disagrees with approved art.

## 1. Recover the drawings the user actually sees

Open the current index or sheet and resolve its thumbnail, enlarged view, original file and displayed crop. Record the approved version and scope for each affected projection. A side panel inside a newer sheet may still contain an older drawing. Trace plans, sections and detail plates to their own sources. A perspective illustration can establish appearance or orientation. Use orthographic art for axis measurements.

For each view record the two physical axes, positive directions, pose, units, datum and full visible extrema. Use a consistent inclusion rule for handles, feet or fine antenna tips. Measure the subject in the original pixel grid, excluding margins, captions and shadows. Check that the crop contains both extrema. Record edge-picking uncertainty and the resulting uncertainty of the full span. A gallery can enlarge an end view until it looks as tall as a side view. Compare ratios within each original or place both at one known physical scale.

## 2. Check whether one object can satisfy the views

For length `L`, width `W` and height `H`, the plan supplies `L/W`, the side supplies `L/H` and the end supplies `W/H`. The side and end imply a second estimate of the plan ratio.

```text
L/W implied by side and end = (L/H from side) / (W/H from end)
```

The estimates must agree within the uncertainty of the measured spans. Each view may have its own uniform zoom. An exact reflected pair proves agreement within that pair only. For a view with a confirmed physical span, compute `units per pixel = known span / its pixel span` and use that same scale on the other axis. Check a second known feature in the other direction where available. Independently fitting horizontal and vertical scales can conceal a conflict.

Use [the ratio checker](../scripts/check_view_ratios.py) for repeatable calculations. Enter the subject spans in the physical axis order shown, swapping image axes for a rotated view. Supply the uncertainty of a full span in source pixels. If it differs between measurements, use a conservative common bound or calculate individual intervals. Use adopted physical dimensions at their recorded precision and account for rounding of physical anchors when interpreting a mismatch.

```sh
python scripts/check_view_ratios.py --plan 840 360 --side 700 260 --end 450 300 --span-error-px 2 --envelope 420 180 120
```

This fictional tray cabinet has a 60 mm end-view feature spanning 150 px. It sets the width to 180 mm and height to 120 mm. The plan then implies a length of 420 mm. At that length the side drawing implies a height of **156 mm**, a **36 mm excess**. Holding the end-view height instead makes the side imply a length of about **323 mm**. Together, side and end imply `L/W ≈ 1.79`. The plan shows `2.33`. Changing the side spans to `700 200` reconciles the views. The checker returns 0 for agreement within the supplied bounds, 1 for a conflict and 2 for invalid inputs. Without an envelope it can check all three ratios without claiming an absolute size.

## 3. Decide which source governs each dimension

Report each conflict as **view and feature → reference dimension → inferred dimension → signed difference**, with units and picking uncertainty. First check for an obsolete source, a clipped extent, dissimilar poses, perspective and nonuniform page scaling. If a model looks wrong but the original projections agree, check model units, camera projection, crop and landmark placement before revising artwork.

Use the user's selected authority for each axis or feature. Where authority is open, show what changes under each plausible choice and ask the user to settle the disputed dimension. Record the adopted envelope, state, datum, tolerances, controlling source per axis and local dimensions to preserve. With only proportions and no absolute anchor, keep conclusions dimensionless. With unresolved conflicts, keep the affected view out of dimensional handoff.

Check constraints that distinguish the choices. In the cabinet, six 64 mm trays in one row with five 4 mm gaps require **404 mm** before end clearances or walls. A 323 mm exterior rules out that layout. A 420 mm exterior leaves 16 mm for both ends and walls combined. Usable internal length still needs checking. Evaluate the opening, internal arrangement and moving clearance separately when they matter. Follow the changed axis into station dimensions, sections, captioned ratios and index descriptions. Mark each affected entry as conflicting, compatible within a stated scope, or unmeasurable from that projection.

## 4. Rebuild and verify the affected view

Transfer longitudinal stations from the approved plan and heights from the approved end or section into a common two-dimensional construction guide. Identify the station origin, height datum, shared scale and the landmarks that determine the reported error. For a projecting component, locate its mount, axis, outer housing and exposed tip. Check which surfaces are visible edge-on. A correct outline can contain an incorrectly placed or shaped component.

Redraw the authorized view from the approved art and guide. Reconstruct panel spacing and local features at their intended size instead of stretching an old painting to the target box. Respect the user's reference choices. If the blockout is under investigation or the user specifies artwork-only reconstruction, keep it and derivatives based on it out of the generation inputs.

Reopen the saved image. Measure its unpadded outline, run the ratio check again and read back the named landmarks against the agreed datums. Report residuals and edge uncertainty. Show the corrected view and obtain approval before using it as the reference for its opposite. For rigid opposite views, choose the reflection on a common grid. Left and right elevations with the front switching sides reflect horizontally. A horizontal plan and underside with the front kept on the same side reflect vertically. Check the [extracted silhouettes](top-ventral-outline.md) and inspect visible hardware separately. The existing helper interprets its bow option for a plan and underside pair. For upright left and right elevations, compare the saved mask directly against a left-to-right reflection of the approved side mask on the same grid. Reapply readable lettering and preserve the approved handedness of emblems.

Use [Approved Reference Sheets](approved-reference-sheets.md#revise-a-sheet-and-publish-it) to update dependent sheets and the index at their authorized stages. Assemble approved images directly, verify untouched panels pixel-for-pixel, and check thumbnail, enlargement and original-file links against the accepted versions.
