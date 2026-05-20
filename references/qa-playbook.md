# PPT QA Playbook

Use this playbook when a deck is more than a small text edit, when it was generated from code, or when the final audience will open it in Microsoft PowerPoint.

## QA Mindset

- Assume the first render has problems. If no issue is found on the first pass, inspect high-risk slides again.
- A positive signal is not a pass by itself: text extraction, zip integrity, LibreOffice rendering, and PowerPoint compatibility check different failure modes.
- Run validation after the last edit. A deck can be valid before a final repack and invalid afterward.
- Do not deliver a deck that PowerPoint prompts to repair, even if it looks fine after repair.
- Structure comes before polish. If a slide feels wrong, first check whether the registered page type and screenshot/image slot fit the content before tuning margins, fonts, or colors.
- Theme comes before decoration. If a slide feels visually foreign, check `references/theme-contract.md` before adding new colors, fonts, backgrounds, or cards.
- Mechanical checks are not taste checks, and visual checks are not package checks. Treat them as separate layers.

## Minimum Delivery Gate

Every final deck needs:

1. Text extraction and placeholder scan.
2. Zip package integrity check.
3. OpenXML validation through the base `pptx` skill.
4. Picture/media relationship checks.
5. PDF/image render and visual inspection.
6. Explicit final note about any skipped check.

For company-style decks, the expected creation route is template-derived editing. If the company template is usable, duplicate and edit template pages through the base `pptx` editing workflow. Treat PptxGenJS/from-scratch generation as an exception that must be justified and checked more strictly.

The helper script can run most mechanical checks:

```bash
python scripts/pptx_quality_gate.py output.pptx --outdir /tmp/idtpptx-qa
```

If dependencies are installed under a different interpreter, use `--python python` or `IDTPPTX_PYTHON=python`.

If the script reports `BLOCK`, fix the issue before delivery. If it reports `PASS`, still inspect the rendered images or `contact-sheet.jpg`.

## Visual Inspection Heuristics

Open the individual slide image for any high-risk slide. Contact sheets are useful for scanning, but too small for final judgment.

High-risk slides:

- Cover slides, especially when metadata/objective text was added after template replacement.
- Early setup or "discussion scope" pages, especially titles like `初版目标与讨论范围`; these usually should be removed from a final deck unless the user explicitly asked for a workshop agenda.
- Title-heavy pages copied from templates, especially if PowerPoint edit mode may show `单击此处添加标题` or an empty title/subtitle placeholder.
- Dense tables, especially near the bottom-right logo.
- Pages with long Chinese and English mixed labels; English tokens often widen text unexpectedly.
- Pages with English-heavy metrics or field names on business-facing cards, such as `generated / accepted / candidateLines`, `exact / partial`, `daily facts`, or `attribution job`.
- Sparse pages where only a few short body lines sit in a large blank area.
- Titles that may wrap to two lines while a top divider line or marker was positioned for one line.
- Screenshot pages with arrows, red boxes, or multiple screenshots.
- Generated image pages where the image might contain its own title, footer, page number, logo, or fake deck frame.
- Generated chart/diagram pages where the asset may bring a dark tech, marketing, magazine, or poster-like theme.
- Slides copied from external decks where fonts, fills, or accent colors may carry another theme.
- Pages whose layout uses the space near the bottom-right logo.
- Slides copied from templates where empty placeholders may still exist as blank boxes.
- Section divider pages where a top-left title placeholder may remain in addition to the center blue section bar.
- Slides generated with a blank layout or custom code on top of a branded template; these often duplicate the template chrome and compress content into a small upper-left area.
- Any slide edited after the first render.

Look for:

- Cover metadata placed inside a white filled rectangle, white card, white diagonal strip, or empty white overlay shape.
- More than one visible Inspur logo on a slide. If the template already has the bottom-right or cover logo, remove manually inserted logo images.
- A small inner slide effect: a second header line, page number, footer/logo, or content group appears inside the existing template frame, with large unused space on the right and bottom.
- PowerPoint default placeholder prompts such as `单击此处添加标题`, `单击此处添加副标题`, `单击此处添加文本`, or `Click to add title`.
- A duplicated title system: a top-left title placeholder plus a section bar title, or a cover title plus an old subtitle/title placeholder.
- Normal content titles that are tiny inside a tall title placeholder, or oversized titles that collide with the divider rule.
- Text, table borders, cell fills, screenshots, callouts, charts, or background shapes overlapping the bottom-right logo.
- Text overlapping the logo, page number, table border, screenshot, arrow, or title rule.
- Text that visually belongs to a filled note/card/conclusion background but extends past the right or bottom edge of that background.
- Process-card headings overlapping card body text, especially when English labels wrap to two lines.
- Text clipped at the edge of a text box, table cell, or slide.
- Tables so dense that row text is not readable at normal presentation size.
- Tables that use small body text while rows are tall and mostly empty.
- Table text vertically stuck to the top or bottom when cells are otherwise short.
- A single table mixing centered headers, centered short cells, and left-aligned descriptive cells without an intentional source-table reason.
- Sentence/evidence tables centered in a way that makes Chinese explanations harder to scan; compact categorical tables left-aligned in a way that makes the matrix look uneven.
- Main body text that is still single-spaced on a sparse slide, or line spacing that is too loose for dense tables/process cards.
- Mixed editable fonts such as YaHei plus Songti/Calibri/Arial/Aptos in the same normal body area.
- Mixed Chinese-English wording that reads like raw implementation notes instead of a Chinese internal report.
- Normal text rendered in gray, blue-gray, or other low-contrast muted colors instead of black/near-black.
- Non-IDT theme drift: dark tech backgrounds, warm marketing palettes, magazine-style color systems, Swiss poster styling, or generic multi-theme colors.
- Footer/source text colliding with the main content.
- Uneven alignment among repeated cards, columns, table rows, or step boxes.
- Conclusion bars, note boxes, and cards where the visible background is shorter or narrower than the text.
- Large empty placeholder regions left after deleting source content.
- Low contrast text in light blue, gray, blue-gray, or pale yellow zones.
- Images or screenshots with mismatched crop density, inconsistent ratios, or important UI text squeezed too small.
- Generated visuals that look like a standalone poster or slide instead of an asset inside the company PPT.

## Structure Diagnosis

When visual QA finds a problem, classify it before fixing:

- **Wrong page type**: the content should move to another registered type in `layout-map.md`, such as Comparison Table instead of card-like process boxes.
- **Theme drift**: the slide uses colors, fonts, generated imagery, or copied deck styling that violates `theme-contract.md`.
- **Wrong material slot**: a screenshot or image was placed in a slot too small, too wide, or too close to the logo.
- **Component misuse**: a table, card, arrow, or callout was used as decoration rather than evidence.
- **Spacing problem**: the structure is right, but title, body, table, screenshot, or caption spacing needs adjustment.
- **Title-system problem**: leftover title/subtitle placeholders remain, the title band is too tall, or the title font was changed without resizing the title zone.
- **Logo-safe-zone problem**: content uses the lower-right area without protecting the actual logo mark.
- **Nested-slide problem**: generated content has its own mini header/footer/logo system or occupies only the upper-left of the template content zone. Rebuild using a registered template page type rather than tuning margins.
- **Content overload**: the page needs to split, not shrink.

Do not repair a wrong structure or theme drift by randomly shrinking text, adding arbitrary margins, covering old elements with new shapes, or inserting decorative cards.

## Content Inspection Heuristics

- Read extracted text in slide order. Confirm the narrative still works without relying on visuals.
- Confirm non-trivial decks were planned against registered page types before detailed editing.
- Check slide titles are specific and name the page's job.
- Check title placeholders are gone. Section dividers should use the center blue bar title only, and normal content slides should have one compact top-left title.
- Check the deck uses `微软雅黑` / `Microsoft YaHei` by default for editable text.
- Check the deck follows `references/theme-contract.md`; scenario variants may change density and page type, not the core color/font system.
- Check body, table, caption, and note text uses black or near-black; only warnings, risks, key callouts, and screenshot annotations use red.
- Check wording is Chinese-first. Keep English for `AI`, `Git`, `IDE`, `API`, lowercase technical nouns such as `git` and `linux`, real module names, and necessary code fields; translate ordinary metrics, statuses, matching modes, and process labels.
- Check sparse slides use larger body text and `1.5-1.7x` line spacing, while normal body slides use about `1.3-1.45x`.
- Check normal comparison/matrix tables use vertical-middle cell alignment, `12-13 pt` body text when not dense, and one consistent horizontal alignment mode for the whole table.
- Check every placeholder, old URL, old contact, old product name, old screenshot, and old email example was intentionally kept or removed.
- Check title size versus title space: for normal content slides, adjust both the title-zone height and the `24-30 pt` title size instead of only scaling text.
- Check the final sequence does not include deck-production setup pages. If a page only says what this draft will or will not cover, delete it rather than polishing it.
- Check footnotes and sources are short enough not to collide with content.
- Check "待补充" text is intentional. If the deck is meant as final delivery, remove or replace it.
- Check the extracted text does not contain PPT-making process notes. Phrases such as `形成一版可讨论 PPT`, `结构草稿`, `后续补充数据和截图`, `本轮先不展开`, and `不追求最终视觉定稿` are generation scaffolding, not audience-facing content.
- Check every text-on-background treatment: the text must wrap inside the filled rectangle/card/callout, not extend beyond its visible boundary.
- Check any full-width table or screenshot does not overlap the bottom-right logo mark. Space above and left of the logo can be used when the logo remains clear.
- Check cover metadata remains plain text and does not introduce a white panel.
- For screenshots and generated images, check `references/screenshot-framing.md`: real screenshots remain faithful unless the user requested redesign, image groups have consistent ratios, and generated assets do not include deck chrome.

## Package And PowerPoint Compatibility

Use `unzip -t` for package integrity and the base `pptx` `validate.py` for OpenXML validity. LibreOffice rendering is necessary for visual QA, but it is not enough for PowerPoint delivery.

Known failure patterns:

- `p:notesMasterIdLst` after `p:sldIdLst` in `ppt/presentation.xml`: LibreOffice may render it, but PowerPoint can prompt to repair. Valid order puts `p:notesMasterIdLst` before `p:sldIdLst`.
- `[Content_Types].xml` `Override` entries that point to package parts that no longer exist, such as stale `ppt/slideMasters/slideMasterN.xml` entries after generator cleanup.
- Broken or stale relationship ids after duplicating, deleting, or reordering slides.
- Broken image relationships: an `a:blip` embed id does not exist in the slide/layout/master `.rels`, the relationship target is missing, external, not under `ppt/media`, lacks an image content type, or the actual PNG/JPEG/GIF bytes are invalid.
- PowerPoint repair followed by images turning into generic attachment/package icons. Treat this as a media/package defect, not a cosmetic issue.
- Repeatedly embedding the same template logo as separate media files on every slide. This may render, but it is a sign that the deck was generated from scratch instead of reusing the template master/layout and should be inspected carefully.
- Reusing a branded template while also drawing custom slide chrome and logos in generated code. This can pass package validation but fail visual QA because the page reads as a smaller PPT inside a larger PPT.
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
