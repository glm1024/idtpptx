# IDT/Inspur Pragmatic PPT Style Guide

## Scope

This guide captures reusable company presentation style. It intentionally excludes source-deck business content.

## Visual Identity

- Use a 16:9 widescreen deck.
- Keep the background white by default.
- Use Inspur blue as the primary accent. Current observed palette:
  - Primary blue: `0062AC`
  - Deep blue: `00518E`
  - Dark navy: `213261`
  - Neutral gray: `A4A3A4`
  - Light cyan accent: `BBE0E3`
- Use black or dark gray for body text.
- Use red primarily for arrows, callouts, risks, or marking a specific UI location in screenshots.

## Color Discipline

- Treat color as brand and meaning, not decoration. Default to blue, white, gray, and occasional light cyan.
- Do not assign different colors to each step, card, badge, or vertical bar just to make the slide look more designed.
- Avoid the base `pptx` skill's generic colorful infographic look: multicolor numbered circles, rainbow process cards, alternating blue/green/yellow/red accent bars, decorative icon grids, and heavy card shadows.
- Green, amber, and red may be used only when they encode clear status, severity, or risk meaning. Use them consistently on the slide and avoid mixing semantic and decorative colors.
- If a slide needs a secondary color, use at most one secondary semantic color beyond the blue/gray brand palette unless the content itself is a status matrix.

## Brand Elements

- Keep the Inspur logo in the bottom-right on normal content slides.
- Treat the bottom-right logo area as protected space. Reserve at least the rightmost `2.7 in` and bottom `1.1 in` on 16:9 content slides for the logo, page number, and breathing room.
- No body text, table grid, screenshot, callout, chart, or decorative block may cover or visually crowd the bottom-right logo safe zone. If content would enter this zone, split the slide or move/resize the content.
- Keep the small blue corner marker at the top-right.
- Keep the thin blue/gray header rule at the top.
- Cover and closing slides may use a larger logo.

## Typography

- Default editable font is `微软雅黑` / `Microsoft YaHei` for Chinese, English, numbers, and punctuation.
- Use bold `微软雅黑` for titles, section labels, card headings, and table headers.
- Avoid `宋体`, `仿宋`, `楷体`, `黑体`, Calibri, Arial, Aptos, or theme-default fonts in normal editable text unless the user explicitly asks to match a source deck.
- Normal slide titles are compact and top-left, usually `24-30 pt`.
- Main body text is usually `13-18 pt`; use larger body text on sparse slides and split the slide before shrinking below readable size.
- Main body text should not default to single spacing. Use `1.3-1.45x` for normal body text and `1.5-1.7x` on sparse explanation pages with obvious empty space.
- Tables, dense process cards, captions, and footnotes may use tighter spacing; follow `references/typography.md` for the scenario-specific size and line-spacing rules.

## Layout Principles

- The deck should feel like an internal training manual or operational report.
- Use clear rectangular zones and generous white background.
- Favor screenshots, tables, and annotated process evidence over abstract illustrations.
- Keep content aligned to a consistent left edge.
- Keep dense content away from the lower-right corner; do not use a full-width table or screenshot that extends into the logo safe zone.
- For process or workflow slides, prefer simple blue-gray step labels, quiet tables, screenshot sequences, or light line flows over colorful step badges and card grids.
- Do not create decorative cards, gradient hero sections, large stock imagery, or colorful infographic-heavy slides unless the user explicitly asks for a different style.

## Cover Slides

- Keep cover slides clean: blue top band, gray title band, title/subtitle, plain metadata text, and logo are enough.
- Do not add white cards, white text panels, white filled boxes, or decorative white strips on the cover. Metadata and objectives should sit directly on the white or gray canvas without a filled rectangle behind them.
- If a copied template cover contains a white cutout, diagonal strip, or empty white overlay shape, delete it unless it is the actual slide background.

## Common Page Chrome

Normal content pages usually include:

- Top title line near the upper-left.
- Thin line under or near the title area.
- Small right-top blue corner marker.
- Logo at bottom-right.
- Main content occupying the center with comfortable margins.

Section divider pages usually include:

- Center blue horizontal bar.
- Section number block attached to the bar.
- Simple section title in white text inside the bar.

## Screenshots

- Screenshots should be large enough to inspect.
- If multiple screenshots show a flow, arrange them horizontally and use red arrows between steps.
- If a screenshot is busy, crop to the meaningful area instead of shrinking the entire screen too much.
- Red arrows and red boxes are acceptable for practical operation guidance.

## Tables

- Use tables for comparisons, lists, exports, and matrix-style decisions.
- Keep table styling quiet: thin grid lines, plain header row, minimal fills.
- Do not over-style tables with heavy colors.
- Table cells should default to vertical-middle alignment. Top alignment is reserved for long paragraphs, lists, code, or cells with `3+` wrapped lines.
- Center short headers and short categorical values; left-align descriptive text and sentence-like cells.
- Normal 3-5 column tables should use `12-13 pt` body text. Do not leave a large table area filled with small spreadsheet-like text and oversized row whitespace.

## Avoid

- Text-only slides without structure.
- Marketing-style hero pages.
- Cover pages with redundant white panels, empty white shapes, or white decorative cutouts.
- Decorative gradient orbs, large abstract backgrounds, or unrelated illustrations.
- Excessive icon grids.
- Multicolor step circles, rainbow process cards, alternating colored vertical bars, and other base-`pptx` colorful infographic patterns without business meaning.
- Center-aligned body paragraphs.
- Keeping old screenshots, URLs, contacts, or product instructions from a source deck as accidental placeholders.
