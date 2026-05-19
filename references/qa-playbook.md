# PPT QA Playbook

Use this playbook when a deck is more than a small text edit, when it was generated from code, or when the final audience will open it in Microsoft PowerPoint.

## QA Mindset

- Assume the first render has problems. If no issue is found on the first pass, inspect high-risk slides again.
- A positive signal is not a pass by itself: text extraction, zip integrity, LibreOffice rendering, and PowerPoint compatibility check different failure modes.
- Run validation after the last edit. A deck can be valid before a final repack and invalid afterward.
- Do not deliver a deck that PowerPoint prompts to repair, even if it looks fine after repair.

## Minimum Delivery Gate

Every final deck needs:

1. Text extraction and placeholder scan.
2. Zip package integrity check.
3. OpenXML validation through the base `pptx` skill.
4. PDF/image render and visual inspection.
5. Explicit final note about any skipped check.

The helper script can run most mechanical checks:

```bash
python scripts/pptx_quality_gate.py output.pptx --outdir /tmp/idtpptx-qa
```

If dependencies are installed under a different interpreter, use `--python python` or `IDTPPTX_PYTHON=python`.

If the script reports `BLOCK`, fix the issue before delivery. If it reports `PASS`, still inspect the rendered images or `contact-sheet.jpg`.

## Visual Inspection Heuristics

Open the individual slide image for any high-risk slide. Contact sheets are useful for scanning, but too small for final judgment.

High-risk slides:

- Dense tables, especially near the bottom-right logo.
- Pages with long Chinese and English mixed labels; English tokens often widen text unexpectedly.
- Titles that may wrap to two lines while a top divider line or marker was positioned for one line.
- Screenshot pages with arrows, red boxes, or multiple screenshots.
- Slides copied from templates where empty placeholders may still exist as blank boxes.
- Any slide edited after the first render.

Look for:

- Text overlapping the logo, page number, table border, screenshot, arrow, or title rule.
- Text clipped at the edge of a text box, table cell, or slide.
- Tables so dense that row text is not readable at normal presentation size.
- Footer/source text colliding with the main content.
- Uneven alignment among repeated cards, columns, table rows, or step boxes.
- Large empty placeholder regions left after deleting source content.
- Low contrast text in light blue, gray, or pale yellow zones.

## Content Inspection Heuristics

- Read extracted text in slide order. Confirm the narrative still works without relying on visuals.
- Check slide titles are specific and name the page's job.
- Check every placeholder, old URL, old contact, old product name, old screenshot, and old email example was intentionally kept or removed.
- Check footnotes and sources are short enough not to collide with content.
- Check "待补充" text is intentional. If the deck is meant as final delivery, remove or replace it.

## Package And PowerPoint Compatibility

Use `unzip -t` for package integrity and the base `pptx` `validate.py` for OpenXML validity. LibreOffice rendering is necessary for visual QA, but it is not enough for PowerPoint delivery.

Known failure patterns:

- `p:notesMasterIdLst` after `p:sldIdLst` in `ppt/presentation.xml`: LibreOffice may render it, but PowerPoint can prompt to repair. Valid order puts `p:notesMasterIdLst` before `p:sldIdLst`.
- `[Content_Types].xml` `Override` entries that point to package parts that no longer exist, such as stale `ppt/slideMasters/slideMasterN.xml` entries after generator cleanup.
- Broken or stale relationship ids after duplicating, deleting, or reordering slides.
- Negative `a:xfrm/a:ext` dimensions on generated line shapes. If a line is drawn from right to left or bottom to top, normalize the bounding box to positive width/height and use `flipH`/`flipV` to preserve direction.
- Unintentional `ppt/notesSlides/` and `ppt/notesMasters/` parts from generated decks. If the deck has no speaker notes, remove notes parts, the notes relationships, notes content types, and `p:notesMasterIdLst`.
- Orphaned notes, media, charts, or layouts left after template cleanup.
- Invalid shape options from generated decks, especially unusual shadow, gradient, or rounded-rectangle combinations.
- Content type entries missing for new media, slide, notes, chart, or embedding files.

If PowerPoint reports a repair prompt:

1. Treat the deck as not delivered.
2. Preserve a copy of the broken file for diagnosis.
3. Run `unzip -t` and `validate.py`.
4. Inspect `ppt/presentation.xml`, slide relationships, and `[Content_Types].xml`.
5. Repack, validate, render, and inspect again.

## Final Handoff Standard

When reporting completion, include:

- Output `.pptx` path.
- Which QA layers passed.
- Render artifact path when useful.
- Any check that could not be run and the residual risk.

Do not say only "rendered successfully"; say whether OpenXML validation also passed.
