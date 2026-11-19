---
name: virtual-item-design
description: Design original virtual items with ImageGen, from a written brief to an approved set of consistent concept images. Use for virtual objects of any kind, including spatial, flat, wearable, organic, or digital-only items, with user review at each creative step.
---

# Virtual Item Design

Start with what the item is, who encounters it, and what they should recognize or do with it. The deliverable is an approved set of images for the intended use, such as illustration, storytelling, an interactive experience, or a modeling handoff. Use ImageGen to create new artwork and revise its visual design. When the request is to assemble approved images into a sheet, lay out the original images directly.

## Naming

Use English for the skill, proposed item and component names, stage titles, views, states, and deliverable filenames. Use the same spelling in prompts, review notes, and final links. For example, the item **Tide Compass** can have an **Active** state and a file named `tide-compass-active-v02.png`. Preserve supplied source identifiers. If an existing item has a non-English name, propose an English display name for approval and keep the original as its source identifier. Conduct the discussion and explain decisions in the user's language.

## Approval at Every Step

1. Start with a short **Design Brief** in text. Establish the item category, intended use, and visual direction with the user. Record the distinguishing shape, parts or graphic elements, and any relevant states. Propose the image set and specify the first image, its composition, and what the user should be able to judge. Translate functional requirements into visible acceptance criteria, and record which details belong in a later view. Offer text options for open creative choices. Wait for explicit approval of the brief and first image before generating it.
2. Before every subsequent generation or edit, identify one image, its approved references, the proposed change or view, and one or two visible acceptance criteria. Wait for the user's explicit authorization for that step. A direct instruction about the stated image is sufficient. General enthusiasm, a request for the full set, silence, or elapsed time does not authorize another image. When the user asks for a fresh start, carry forward the accepted brief and any components they still designate. Exclude rejected artwork from the generation inputs. Generate alternatives one at a time. A sheet with several panels counts as one image only when the user has agreed to its contents.
3. Show the actual result with its English name and version. Point out any visible discrepancy and ask whether to adopt, revise, or discard it. Only a version the user has seen and accepted becomes a design reference. A specific correction authorizes that edit; show the revised image for a fresh decision. The user may approve the current result and explicitly authorize a stated next step in one reply.
4. Record the image, version, source, status and exact scope of the user's decision. An approval can cover one feature, proportion or view. A newer sheet can still contain panels from different approved versions. Preserve the originals and resolve the current source for each affected feature or panel when resuming work. Review affected derivatives individually.

## Select the Image Set

Choose views according to the design question. A single item can use more than one approach.

| Item and purpose | Useful images | What to compare |
|---|---|---|
| A spatial object for modeling or assembly | A three-quarter concept, orthographic views on common axes, a hidden face or an enlarged joint where needed | Shared dimensions, landmarks, handedness, occlusion, and connections |
| A soft, organic, or wearable item | A silhouette, a draped or worn view, and a detail of a fold, attachment, or pattern | Proportions, material behavior, pattern placement, and fit at the contact points |
| A flat or digital-only item | A face-on master at its intended aspect ratio, a legibility check at display size, and relevant states | Graphic boundaries, alignment, contrast, and which features persist across states |
| A changing or ephemeral item | An identifying state followed by individually proposed states or key moments | The visual feature that keeps it recognizable, and what changes between the selected moments |

For example, a digital ticket may need a face-on image and a redeemed state. A virtual folding lantern may need a three-quarter concept, a hinge detail, and an open view. Agree on which images answer the user's questions and skip stages that add no information.

## Calibrated Views and Publication

When relative dimensions, component fit or shared axes affect the design, use [Approved Reference Sheets](references/approved-reference-sheets.md) to select source views and check the delivered image. The same reference covers replacing one panel, verifying the others and updating a viewing index after approval.

## Opposite Orthographic Views

For spacecraft Top and Ventral views in the same state, lock the complete projected outline to the approved master. Follow [Top and Ventral Silhouette Lock](references/top-ventral-outline.md) for stencil creation, independent checks on the saved image and the exact pixel acceptance criterion. Verify visibility of surface hardware separately. Apply the same method to other rigid objects when their opposite views require an exact shared silhouette.

## Production Stages

| Stage | Action and review |
|---|---|
| **1. Concept** | Generate the first agreed image. Once the user adopts it, derive a short list of defining features from the actual image. Have the user settle differences with the brief and confirm the list. |
| **2. Master Sheet** | Establish the reference for structure, composition, or state. For a spatial item, align common dimensions across views. For a flat design, use its face-on layout. Reuse the approved concept when it already serves as the master. |
| **3. Details and States** | Identify one unseen surface, ambiguous connection, graphic detail, or undefined state. Explain what is already established and what the user is being asked to design. Generate the agreed detail, then seek acceptance. |
| **4. Individual Images** | Deliver the requested views or states in the agreed framing, resolution, and background. Reuse approved images that meet the specification. Compare regenerated images with the master at common landmarks and at the intended display size. |
| **5. Local Revision** | Enter this stage wherever a discrepancy occurs. Show the approved source, identify the target and one issue, and edit within the agreed scope. Compare the changed area and the complete result. Resume the affected stage after review. |
| **6. Final Appearance** | Agree on the finish relevant to this item, such as surface materials, palette, linework, transparency, or emission. Show the final appearance in the agreed composition and request approval. |

For the current step, adapt the corresponding [ImageGen Prompts](references/imagegen-prompts.md). Attach the actual references and identify the role of each. Use shared extents or anchors to compare images. Record physical units only when supported by a source. For an existing item, consult the project’s design index when available, identify the approved source for each affected view and establish which decisions remain open. A later request for Blender production follows the project's modeling workflow.

Deliver links to the accepted images and the defining features. Identify each image's view or state and any unresolved decisions. Mark the requested set complete once the user has accepted every required image.
