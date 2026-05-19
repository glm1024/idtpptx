# Typography And Spacing

Use this as the default typography contract for IDT/Inspur PPTX work. It is tuned for 16:9 internal reports, training decks, review materials, and operation manuals.

## Font Family

- Default font for all editable text: `微软雅黑` / `Microsoft YaHei`.
- Use the same default font for Chinese, English, numbers, punctuation, and mixed Chinese-English sentences. This avoids the uneven rhythm caused by mixing Songti, Calibri, Arial, and YaHei in the same paragraph.
- Use bold `微软雅黑` for slide titles, section labels, card headings, and table headers.
- Avoid `宋体`, `仿宋`, `楷体`, `黑体`, Calibri, Arial, Aptos, or theme-default fonts in normal editable text unless the user explicitly asks to match a source deck.
- Keep fonts inside screenshots as-is; do not edit screenshots just to normalize fonts.
- Code, SQL, commands, file paths, and API snippets may use `Consolas`, `Menlo`, or another monospace font at `9-11 pt`. Short inline technical terms inside Chinese sentences should usually stay in `微软雅黑`.

When generating with PptxGenJS or another code generator, set font explicitly on every text box and table cell. Do not rely on PowerPoint defaults.

## Font Size Defaults

For 16:9 slides, use these ranges before shrinking content. If content does not fit at the minimum readable size, split the slide.

| Scenario | Default Size | Range | Notes |
|---|---:|---:|---|
| Cover title | 38 pt | 34-44 pt | Use bold; keep it visually dominant but not marketing-style oversized. |
| Cover subtitle | 24 pt | 20-28 pt | Use when the subtitle is a real qualifier, not a second title. |
| Cover metadata/date/version | 15 pt | 13-16 pt | Keep plain text; do not put it in a white card. |
| Normal slide title | 28 pt | 24-30 pt | Top-left, bold, usually one line. |
| Section divider title | 26 pt | 22-30 pt | White text on the blue bar, bold. |
| Card/process heading | 17 pt | 15-20 pt | Use bold; keep each heading short. |
| Main body text | 15 pt | 13-18 pt | Use 16-18 pt on sparse pages, 13-15 pt on normal pages. |
| Numbered bullets | 14.5 pt | 13-16 pt | Prefer short lines; avoid paragraph-length bullets. |
| Process-card body | 12.5 pt | 11-14 pt | Compact, because cards usually appear in rows. |
| Table header | 13 pt | 12-14.5 pt | Bold; center short headers unless the header is a long phrase. |
| Table body | 12 pt | 10.5-13.5 pt | Use `12-13 pt` for normal 3-5 column tables; reserve smaller sizes for dense tables. |
| Captions, notes, sources | 9 pt | 8-10.5 pt | Use muted gray; keep short. |
| Big numeric callout | 36 pt | 30-48 pt | Pair with a 10-12 pt label. |

Do not use body text below `12 pt` outside tables, labels, footnotes, or dense process cards. Do not use table body below `10.5 pt` unless the table is genuinely dense and cannot be split; never go below `9.5 pt` for deliverables intended to be read on screen.

## Line Spacing Defaults

Single spacing is not the default for main body text. Choose spacing by content density:

| Scenario | Line Spacing | Use When |
|---|---:|---|
| Sparse explanation | 1.5-1.7x | A slide has only 2-5 short body lines and obvious empty vertical space. Increase body size first, then use wider line spacing. |
| Normal body / numbered bullets | 1.3-1.45x | Most explanation pages, review conclusions, constraints, and grouped bullets. |
| Dense but readable body | 1.18-1.28x | Content is moderately dense but still text-led. Prefer splitting before going tighter. |
| Process cards / small labels | 1.1-1.2x | Short two-line card descriptions, stage labels, compact annotations. |
| Tables | 1.05-1.18x | Table cells and matrix pages where row height is the limiting factor. |
| Captions / footnotes | 1.0-1.15x | Short source lines and notes. |
| Standalone quote / slogan | 1.8-2.0x | Only for very sparse title-like text. Do not use 2.0x for bullets or dense paragraphs. |

If a mostly empty slide still has small single-spaced body text, treat it as a layout bug. Make the text larger, use `1.4-1.6x` line spacing, or redesign the slide with a clear two-column/card structure.

## Paragraph And Group Spacing

- Keep paragraph spacing more important than decorative boxes. Separate ideas with `4-8 pt` after each paragraph or bullet group.
- For normal numbered lists, use `2-4 pt` after each item and `1.3-1.45x` line spacing.
- For two distinct groups on the same slide, leave `0.18-0.30 in` vertical space between groups.
- For card grids, keep card body compact and put more spacing between cards than inside each card.
- Do not compensate for an empty slide by adding blank filler shapes. Improve typography, enlarge evidence screenshots, or split/rebalance the layout.

## Table Typography And Alignment

Default table alignment:

- Vertically align table text to the middle by default. This is required for matrix, comparison, scope, responsibility, and capability tables where most cells are one or two lines.
- Use top vertical alignment only when a cell contains a paragraph, a multi-item list, code, or `3+` wrapped lines. Do not top-align ordinary short table rows.
- Header row: vertical middle; horizontal center for short labels such as `模块`, `能力`, `当前口径`, `建议`. Left-align only if the header itself is long or wraps.
- Short categorical body cells should usually be horizontally centered: module names, status, priority, owner, yes/no, date, count, percentage, score, or short capability labels.
- Descriptive body cells should be left-aligned: explanations, review comments, current paths, risk descriptions, actions, evidence, and any sentence-like text.
- Numeric columns should be right-aligned only when comparing magnitudes across rows; otherwise center short numbers.
- Keep left/right cell padding around `0.08-0.12 in` and top/bottom padding around `0.04-0.08 in`. Do not make rows tall while leaving small text visually floating in the middle.

Default table sizing:

- Normal 3-5 column tables with `3-7` rows should use `12-13 pt` body text and `13-14 pt` headers. A wide table with only a few rows should never look like a small-font spreadsheet pasted into a large empty frame.
- Dense tables with `8+` rows, `6+` columns, or many wrapped cells may use `10.5-11.5 pt` body text. If readability still depends on going smaller, split the table.
- Very dense appendix-style tables may use `9.5-10.5 pt` only when the slide is explicitly an appendix or source-data page.
- If a table occupies most of the slide width but the body text feels small, increase the font before increasing row height. If the table still feels empty, reduce the table height or add a concise takeaway/caption outside the table.
- Do not stretch a table vertically just to fill the slide. Row height should be driven by readable text and balanced padding, not by the need to occupy blank canvas.

## Density Decisions

- Sparse slide: title plus `2-5` short lines. Use `16-18 pt` body and `1.5-1.7x` line spacing.
- Normal explanation slide: `6-10` lines. Use `14-16 pt` body and `1.3-1.45x` line spacing.
- Dense evidence slide: screenshots, tables, or `10+` lines. Use structured zones, `11-14 pt` text, and `1.1-1.28x` line spacing. Split the slide if readability depends on going smaller.
- Process overview slide: card headings `16-18 pt`, card body `12-13 pt`, card line spacing `1.1-1.2x`. Avoid long card paragraphs.
- Table slide: table body `12-13 pt` for normal 3-5 column tables, `10.5-11.5 pt` for dense tables, line spacing `1.05-1.18x`, vertical-middle alignment by default, and enough row height for Chinese characters. If the table overlaps the logo or needs smaller text, split it.
