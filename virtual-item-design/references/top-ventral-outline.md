# Top and Ventral Silhouette Lock

For the same rigid spacecraft in the same state, opposite orthographic projections share one footprint. Obtain the approved Top, identify the bow direction, longitudinal axis, fixed origin and pixels per unit. Keep the bow pointing the same way in Ventral. Reflect across the longitudinal axis. A horizontal bow calls for a vertical image flip. A vertical bow calls for a horizontal image flip. Place the axis through the middle of the shared registration window, with padding if an asymmetric hull requires it. Keep the original pixel grid for both views.

1. Extract the Top silhouette from the approved artwork. Prefer genuine subject alpha. For an opaque sheet, exclude labels, guides and shadows and verify the mask against the visible edge. Include all projected parts, recesses and real through-holes. Inspect narrow protrusions and negative spaces. Use one documented binarization convention on both images. Record the authority file/version, crop, registration origin, scale and mask method.
2. Make the reflected stencil with the bundled helper (Python 3 and Pillow). Attach it to ImageGen. Use the approved Port and Aft views to decide which surfaces can be seen from below. A dorsal feature can affect the far edge, but its upper housing and surface details must remain occluded wherever the hull covers it.
3. Render the new ventral surface inside the authorized footprint. For a stencil-bound composite, inspect the unmasked art and rendered boundary for exposed background, truncated geometry, false pods, or distorted features. A stencil can constrain the edge; it cannot validate the depicted surface. Address discrepancies within the authorized step; seek approval before changing hull geometry or mechanism state.
4. Reopen the actual delivery image. Extract the visible hull independently of the construction stencil: verify that opaque pixels contain hull art and that margins and holes contain background. If using an alpha mask from a clipped export, cross-check it against visible color or a contrasting-background inspection. Preserve origin/scale; use the recorded crop for each image, never independently tight-fit the two masks. Run the checker. **Ready for review requires zero missing and zero extra pixels on the agreed binary grid.** Gross extents or rounded IoU are insufficient. If segmentation is ambiguous, document it and resolve it before claiming an exact match.
5. Review bow shoulders, stern cutouts, port/starboard asymmetries, and any named attachments. Log the comparison next to the art and make the overlay available to the user. The geometry check and the user's design approval are separate decisions.

Run the commands from the skill directory. Input PNGs use white for hull and black for empty space, with identical frame dimensions.

```text
python scripts/opposed_outline.py stencil --top top-mask.png --bow left --out ventral-stencil.png
python scripts/opposed_outline.py check --top top-mask.png --bow left --bottom final-ventral-mask.png --report outline-report.json --overlay outline-overlay.png
```

The checker returns 0 for an exact match, 1 for a silhouette mismatch and 2 for invalid inputs. In the overlay green marks coincident boundaries, red marks missing hull and blue marks excess hull. These checks apply to registered orthographic views of a common state; record a separate reference when a mechanism legitimately changes the silhouette.
