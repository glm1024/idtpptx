# IDT/Inspur Pragmatic PPT Style Guide

## Scope

This guide captures reusable company presentation style. It intentionally excludes source-deck business content.

For exact color and font tokens, `references/theme-contract.md` is the source of truth. This guide explains how those tokens should feel and behave in slides.

## Visual Identity

- Use a 16:9 widescreen deck.
- Keep the background white by default.
- Use Inspur blue as the primary accent. See `references/theme-contract.md` for the authoritative token list. Current observed palette:
  - Primary blue: `0062AC`
  - Deep blue: `00518E`
  - Dark navy: `213261`
  - Neutral gray for fills/rules only: `A4A3A4`
  - Light cyan accent: `BBE0E3`
- Use black or near-black for body text, table text, card text, captions, notes, and sources. Good defaults are `000000`, `111111`, `1F2933`, or template-compatible `202020`.
- Do not use medium gray or blue-gray for normal editable text; it looks faint in projection and screenshots.
- Use red primarily for warnings, risks, key callouts, arrows, boxes, or marking a specific UI location in screenshots. Good defaults are `D93025`, `C00000`, existing annotation red `FF4B4B`, or template-compatible `FF0000`.
- Do not replace the IDT/Inspur theme with generic palettes such as Ocean, Forest, Golden, Galaxy, warm marketing, dark tech, magazine, or Swiss poster themes.

## Color Discipline

- Treat color as brand and meaning, not decoration. Default to white canvas, black/near-black text, and blue brand accents.
- Gray is allowed for background bands, table header fills, grid lines, separators, and disabled placeholders; it is not the default text color.
- Do not assign different colors to each step, card, badge, or vertical bar just to make the slide look more designed.
- Avoid the base `pptx` skill's generic colorful infographic look: multicolor numbered circles, rainbow process cards, alternating blue/green/yellow/red accent bars, decorative icon grids, and heavy card shadows.
- Green, amber, and red may be used only when they encode clear status, severity, or risk meaning. Use them consistently on the slide and avoid mixing semantic and decorative colors.
- If a slide needs a secondary color, use at most one secondary semantic color beyond the blue/black/white brand palette unless the content itself is a status matrix.
- Use green for completed/healthy/accepted states, amber for pending/caution/needs confirmation, and red for risk/error/important attention. Do not use red for ordinary category labels.
- Treat unexpected dominant colors as theme drift. Fix the source token or layout choice instead of adding more colors to balance the slide.

## Brand Elements

- Keep the Inspur logo in the bottom-right on normal content slides.
- Protect the logo mark itself, not a large lower-right empty zone. Content may use the space above and left of the logo.
- No body text, table grid, screenshot, callout, chart, or decorative block may overlap the logo mark. Keep only a small breathing margin around the logo.
- Use exactly one visible Inspur logo per slide unless the user explicitly provides a special cover/closing reference that shows otherwise. When the template or master already supplies the logo, do not insert another per-slide logo from code.
- Keep the small blue corner marker at the top-right.
- Keep the thin blue/gray header rule at the top.
- Cover and closing slides may use a larger logo.

## Typography

- Default editable font is `微软雅黑` / `Microsoft YaHei` for Chinese, English, numbers, and punctuation.
- Use bold `微软雅黑` for titles, section labels, card headings, and table headers.
- Avoid `宋体`, `仿宋`, `楷体`, `黑体`, Calibri, Arial, Aptos, or theme-default fonts in normal editable text unless the user explicitly asks to match a source deck.
- Do not import theme-factory font pairings such as DejaVu Sans, FreeSans, or FreeSerif into Chinese company PPTX work.
- Normal slide titles are compact and top-left, usually `24-30 pt`; see `references/title-system.md` before adjusting title size or title band height.
- Remove unused title/subtitle placeholders instead of clearing their text. Final slides must not show `单击此处添加标题`, `单击此处添加副标题`, or similar PowerPoint default prompts.
- Main body text is usually `13-18 pt`; use larger body text on sparse slides and split the slide before shrinking below readable size.
- Main body text should not default to single spacing. Use `1.3-1.45x` for normal body text and `1.5-1.7x` on sparse explanation pages with obvious empty space.
- Tables, dense process cards, captions, and footnotes may use tighter spacing; follow `references/typography.md` for the scenario-specific size and line-spacing rules.

## Layout Principles

- The deck should feel like an internal training manual or operational report.
- Use clear rectangular zones and generous white background.
- Favor screenshots, tables, and annotated process evidence over abstract illustrations.
- Keep content aligned to a consistent left edge.
- Fill the registered template content zone. Avoid layouts that make the whole slide feel like a small slide pasted into the upper-left of a larger slide, with an unused right side and unused lower half.
- Do not recreate template chrome inside the slide body. If the template already has a header rule, page marker, footer/logo, or title placeholder, replace or reuse those elements instead of drawing a second inner header/footer system.
- Keep dense content from covering the bottom-right logo; the area above and left of the logo remains usable when it does not overlap the mark.
- For process or workflow slides, prefer simple blue/black step labels, quiet tables, screenshot sequences, or light line flows over colorful step badges and card grids.
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

The normal title band should feel compact. If a title looks too small inside a large title placeholder, first delete leftover placeholders and compress the title zone, then raise the title toward `26-28 pt`; do not keep an oversized empty title area.

Section divider pages usually include:

- Center blue horizontal bar.
- Section number block attached to the bar.
- Simple section title in white text inside the bar.
- No extra top-left title placeholder.

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
- Choose one horizontal alignment mode for the whole table and apply it consistently to header and body: all-center for compact categorical matrices, all-left for explanation/evidence/risk/action tables. Do not mix center and left alignment within the same table as a visual shortcut.
- Normal 3-5 column tables should use `12-13 pt` body text. Do not leave a large table area filled with small spreadsheet-like text and oversized row whitespace.

## Avoid

- Text-only slides without structure.
- Marketing-style hero pages.
- Cover pages with redundant white panels, empty white shapes, or white decorative cutouts.
- Decorative gradient orbs, large abstract backgrounds, or unrelated illustrations.
- Dark tech, warm marketing, magazine, Swiss poster, or multi-theme palette styling unless the user explicitly requests a non-IDT style exception.
- Excessive icon grids.
- Multicolor step circles, rainbow process cards, alternating colored vertical bars, and other base-`pptx` colorful infographic patterns without business meaning.
- DejaVu, FreeSans, FreeSerif, Aptos, Calibri, Arial, Songti, Fangsong, Kaiti, or other non-YaHei editable fonts in normal Chinese company content.
- Center-aligned body paragraphs.
- Keeping old screenshots, URLs, contacts, or product instructions from a source deck as accidental placeholders.
- PowerPoint default placeholder prompts such as `单击此处添加标题`, `单击此处添加副标题`, or `Click to add title`.
