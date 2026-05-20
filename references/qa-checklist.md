# Company PPT QA Checklist

Run this before delivering any deck created or edited with `idtpptx`.

A deck is not complete just because it renders in LibreOffice or exports to PDF. PowerPoint is stricter about OOXML structure, so the final gate must cover content, visual rendering, package validity, and PowerPoint compatibility.

## Required QA Gate

Run all four layers:

1. **Content QA**: extract text, check slide order, missing sections, typos, and placeholder residue.
2. **Visual QA**: render slides to images and inspect for overlap, overflow, unreadable tables, logo coverage, and bad spacing.
3. **Package QA**: verify the PPTX zip package and run the base `pptx` OpenXML validator.
4. **PowerPoint compatibility QA**: treat any validator error as blocking, even if LibreOffice renders successfully.

For complex decks, generated decks, or decks that will be opened in Microsoft PowerPoint, also read `references/qa-playbook.md`.

Mechanical helper:

```bash
python scripts/pptx_quality_gate.py output.pptx --outdir /tmp/idtpptx-qa
```

If the current agent/runtime Python cannot import `markitdown`, `defusedxml`, or `PIL`, rerun with `--python python` or set `IDTPPTX_PYTHON=python` to use the environment where those dependencies are installed.

The helper is a gate, not a substitute for visual inspection. If it reports `BLOCK`, fix the blocker. If it reports `PASS`, inspect the rendered slide images or contact sheet before delivery.

## Severity Levels

Use this severity model so different agents make the same delivery decision.

### P0 Blocking

Fix before delivery:

- Without an explicit user-approved style exception, the deck has drifted away from the fixed IDT/Inspur theme in `references/theme-contract.md`, such as a dominant dark tech, warm marketing, magazine, Swiss poster, or generic multi-theme palette.
- The slide sequence was not mapped to registered page types in `references/layout-map.md`.
- Placeholder text, old source-deck screenshots, old URLs, contacts, credentials, or product-specific source content remain unintentionally.
- Agent/deck-production process text remains in final slides, such as `可讨论的结构草稿`, `后续补充数据和截图`, `本轮先不展开`, `不追求最终视觉定稿`, or similar notes about how the PPT was generated.
- A deck-production setup page remains in the final deck, such as `初版目标与讨论范围`, `本轮先不展开`, or a page whose only purpose is to explain the draft's limitations rather than the business content.
- Rendered text overlaps other text, table cells, screenshots, card borders, title rules, or the logo. Text overprint is a blocking readability bug.
- Text intended to belong to a filled background box, card, note bar, or callout runs outside that container instead of wrapping inside it.
- Any text, table border, screenshot, annotation, chart, or shape overlaps the bottom-right logo mark.
- A screenshot needed for the task is too small to inspect after rendering.
- A normal 3-5 column table is not readable at presentation size.
- A normal table visibly mixes horizontal alignment modes or leaves short cell text stuck to the top/bottom instead of vertical middle.
- Normal editable text uses muted gray, blue-gray, pale yellow, or another low-contrast color instead of black/near-black.
- Zip integrity, OpenXML validation, package reference checks, relationship checks, non-negative shape extents, or PowerPoint compatibility checks fail.
- Notes parts exist when speaker notes were not intentionally requested.

### P1 Must Fix Unless Explicitly Accepted

- The chosen page type does not match the content shape.
- Local theme drift appears on individual pages: unauthorized accent colors, non-YaHei editable fonts, copied external theme styling, or a generated image with its own external visual frame.
- A generated image includes its own PPT title, footer, page number, logo, watermark, or decorative frame.
- Screenshot groups use mismatched crop density, size, or ratio.
- Sparse pages keep small single-spaced text in a large blank area.
- Tables are stretched to fill space while text remains small.
- Repeated elements are visibly misaligned.
- The mechanical helper warns about possible editable text overlap. Open the affected slide image and fix it unless the overlap is intentional and visually harmless.
- The mechanical helper warns about text possibly overflowing its background/container. Open the affected slide image and fix it by wrapping, resizing the container, shortening the sentence, or splitting content.
- The mechanical helper warns about mixed table alignment or non-middle table cell anchoring. Open the affected slide image and fix it unless a user-provided source table intentionally requires the exception.
- Normal business slides contain English-heavy labels or mixed Chinese-English phrases where a clear Chinese phrase exists, such as raw `generated / accepted / candidateLines`, `exact / partial`, `daily facts`, or `attribution job`.

### P2 Polish

- Captions, notes, or sources are longer than needed.
- Red annotation boxes are visually heavier than the UI detail they identify.
- A page has avoidable empty placeholder-shaped regions after cleanup.

### P3 Optional

- Minor wording improvements that do not change meaning.
- Small spacing refinements that do not affect readability or brand safety.

Recommended commands:

```bash
python -m markitdown output.pptx
python -m markitdown output.pptx | grep -iE "项目名称|汇报主题|章节标题|正文页标题|对比表页标题|步骤说明页标题|说明页标题|问题说明页标题|截图占位|方案 A|方案 B|对比项|xxxx|lorem|ipsum"
unzip -t output.pptx
python /path/to/pptx/scripts/office/validate.py output.pptx
python /path/to/pptx/scripts/office/soffice.py --headless --convert-to pdf --outdir /tmp/render output.pptx
pdftoppm -jpeg -r 150 /tmp/render/output.pdf /tmp/render/slide
```

Replace `/path/to/pptx` with the resolved path of the installed base `pptx` skill. Do not hardcode machine-specific paths in reusable skill instructions.

For the placeholder `grep`, no output is the expected pass result. If it returns any lines, fix them. If `validate.py` reports any new validation error, fix the PPTX structure before delivery.

## Brand And Layout

- `references/theme-contract.md` was followed for color tokens, font contract, and scenario variants.
- The deck uses only registered company page types unless a new reusable page type has been added to `references/layout-map.md`.
- For non-trivial decks, a slide planning table exists before detailed edits: page number, registered page type, reason, main material/screenshot slot, and logo risk.
- Cover slides do not contain redundant white cards, white filled metadata boxes, white diagonal strips, or empty white overlay shapes.
- Cover metadata and objective copy sit directly on the canvas; if they need a panel to be readable, simplify the cover or move the detail to slide 2.
- Normal content slides keep the top rule, top-right blue marker, and bottom-right logo unless intentionally using cover/closing style.
- New slides match the simple white-and-blue corporate style.
- New slides do not introduce generic theme palettes, dark tech backgrounds, warm marketing fills, magazine-style color systems, or Swiss poster styling unless explicitly accepted by the user.
- Titles are compact and aligned consistently.
- Editable text uses `微软雅黑` / `Microsoft YaHei` by default. Any non-YaHei font in normal text is intentional, not a leftover theme/default font.
- Normal editable text uses black or near-black, not muted gray, blue-gray, or pale low-contrast colors.
- Main content fits the center content area without covering the logo.
- The bottom-right logo itself is clear: no body text, table border, table fill, screenshot, annotation, chart, or shape overlaps the logo mark or its small breathing margin.
- Tables, screenshots, and callouts may use the logo's upper-left surrounding space when they do not cover the logo.
- No decorative gradients, stock-photo hero compositions, or marketing-style cards were introduced.
- No base-`pptx` colorful infographic style was introduced: multicolor numbered circles, rainbow card grids, alternating colored vertical bars, decorative icon grids, and heavy card shadows are blocking brand issues unless the user explicitly requested that style.
- Red text/boxes/arrows are reserved for warnings, risks, key callouts, and screenshot annotations. Green means completed/healthy/accepted; amber means pending/caution/needs confirmation. Color used only for decoration should be revised to the blue/black/white brand palette.
- Theme-factory palettes, showcase styling, DejaVu/FreeSans/FreeSerif fonts, and generic theme picker behavior were not imported into the deck.

## Content Hygiene

- No source-deck training text remains unless explicitly requested.
- No old URLs, support contacts, email addresses, screenshots, product names, or credentials remain as accidental placeholders.
- Placeholder words such as `项目名称`, `汇报主题`, `章节标题`, `正文页标题`, `截图占位`, `说明`, `对比项`, `方案 A`, or `方案 B` do not remain in final deliverables.
- No PPT-making process or draft-scaffolding text remains. A slide may describe project assumptions, scope boundaries, or next steps, but it must not describe the agent's plan for writing the deck or say that this generation pass chose not to finish evidence, visuals, screenshots, or data. By default, remove the whole meta page instead of rewriting it.
- Technical wording follows the Chinese-first rule in `references/writing-style.md`: use Chinese for the business meaning, keep English only for accepted abbreviations, real module names, or precise code fields that the audience needs.
- Screenshots belong to the current task and are readable.

Recommended placeholder check:

```bash
python -m markitdown output.pptx | grep -iE "项目名称|汇报主题|章节标题|正文页标题|对比表页标题|步骤说明页标题|说明页标题|问题说明页标题|截图占位|方案 A|方案 B|对比项|xxxx|lorem|ipsum"
python -m markitdown output.pptx | grep -iE "初版目标与讨论范围|初版.{0,8}(讨论范围|目标)|可讨论[[:space:]]*PPT|可讨论的?结构草稿|结构草稿|形成一版可讨论|后续.{0,8}(逐页)?补(充|齐).{0,8}(数据|截图|真实)|本轮.{0,6}不展开|先不展开|不追求最终视觉定稿|最终视觉定稿|先把主线讲顺.{0,12}证据补齐|先统一(口径|路径).{0,12}再讨论(实现)?细节"
```

## Practical Readability

- Dense tables remain legible after rendering.
- Normal 3-5 column tables with a few rows use `12-13 pt` body text; they do not waste space with small spreadsheet-like text inside oversized rows.
- Table cells are vertically middle-aligned by default; only paragraph/list/code-heavy cells use top alignment.
- Each table uses one consistent horizontal alignment mode across header and body: all-center for compact categorical matrices, or all-left for explanation/evidence/risk/action tables.
- Mixed center/left table alignment is treated as a defect unless it is inherited from a user-provided source table and intentionally preserved.
- Sparse slides do not leave small single-spaced text floating in a large blank canvas; body text is enlarged, given `1.5-1.7x` line spacing, or the slide is redesigned.
- Normal explanation/body slides use about `1.3-1.45x` line spacing; process cards, tables, captions, and footnotes use tighter spacing only when density requires it.
- Body text stays at or above `12 pt` outside tables, captions, labels, and footnotes; table body text stays at or above `9.5 pt`.
- Captions, notes, and sources are smaller but still black or near-black; do not make them light gray just to de-emphasize them.
- Red arrows/boxes point to the intended UI detail and do not cover important text.
- Multi-step screenshot pages read left to right.
- Body copy uses direct internal-document Chinese.
- Process cards, table headers, and callouts use Chinese-first labels. English-only labels and slash-separated field lists should be rewritten unless they are real product names, exact field names, or standard abbreviations.
- No text, table grid, image, callout, or background shape overlaps the logo, page edge, screenshot, table, title rule, card title, or card body.
- Text inside light-gray conclusion bars, note boxes, cards, and callouts remains inside the visible background with padding.
- Process-card titles and bodies have separate vertical zones. If a card title wraps to two lines, the body does not collide with it.
- No cover text is wrapped inside a redundant white filled shape or card.

## Screenshots And Generated Images

- `references/screenshot-framing.md` was followed for any screenshot, product image, generated diagram, or UI evidence.
- Screenshots preserve the real UI by default; they were not redrawn or beautified unless requested or necessary for readability.
- The selected image slot and ratio were decided before cropping, scaling, or generating assets.
- Screenshot groups use one ratio, one crop density, and one caption style.
- Generated images are embedded assets only; they do not include PPT chrome, titles, footers, page numbers, logos, watermarks, or decorative frames.
- Long or narrow screenshots were cropped to the meaningful area or split into same-size panels instead of being squeezed into one unreadable image.

## PowerPoint Compatibility

- Do not rely on LibreOffice rendering alone. LibreOffice can tolerate OOXML ordering issues that PowerPoint reports as "content has a problem" and tries to repair.
- Always run the base `pptx` `scripts/office/validate.py` after packing or generating a deck.
- For decks generated by PptxGenJS or any non-template generator, pay special attention to `ppt/presentation.xml` element order.
- Known failure mode: `p:notesMasterIdLst` placed after `p:sldIdLst` can pass zip checks and render in LibreOffice, but fail PowerPoint strict validation. The valid order places `p:notesMasterIdLst` before `p:sldIdLst`.
- Known failure mode: `[Content_Types].xml` can contain `Override` entries for slide masters, slides, notes, charts, or media that do not exist in the package. LibreOffice and simple OpenXML validators may tolerate this, but PowerPoint can prompt for repair.
- Known failure mode: `.rels` files can point to deleted or renamed package parts after slide duplication, deletion, or cleanup. Treat any missing internal relationship target as blocking.
- Known failure mode: generated line shapes can produce negative `a:ext cx/cy` values when using end coordinates smaller than start coordinates. Normalize those to positive extents with `flipH`/`flipV`; PowerPoint may repair or delete the affected content.
- Known failure mode: PptxGenJS can emit notes slides/notes master parts even when the deck does not intentionally use speaker notes. For `idtpptx` delivery decks, remove notes parts unless the user explicitly needs speaker notes. If notes are intentional, run the helper with `--allow-notes`.
- If PowerPoint prompts for repair, treat the deck as not delivered. Inspect the validator output, fix the OOXML structure, repack, and re-run the full QA gate.

## Final Verification

- Render slides to images using the base `pptx` skill workflow.
- Use the contact sheet for scanning only. Open individual slide images for every high-risk page: cover, dense table, screenshot page, sparse text page, logo-adjacent layout, and any slide edited after the first render.
- Inspect affected slides visually and structurally.
- If a slide looks wrong, first classify the cause: wrong page type, wrong material slot, component misuse, spacing problem, logo-safe-zone problem, or real content overload. Do not fix by randomly shrinking text, adding margins, or hiding defects under extra shapes.
- If a slide feels like it came from another design system, classify it as theme drift first: wrong token, wrong font contract, wrong scenario variant, or source material carrying an external theme.
- Treat any content that overlaps the bottom-right logo mark as a blocking layout bug.
- Treat generic multicolor process decoration as a blocking brand bug when it comes from the base `pptx` visual style rather than from user-specified company material.
- Run zip and OpenXML validation after the last edit, not before.
- If a fix changes layout or package structure, re-render and re-validate.
- Do not treat the first render as proof. If any issue is found, fix it and re-run the affected QA layer before delivery.
