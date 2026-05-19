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

- Cover slides do not contain redundant white cards, white filled metadata boxes, white diagonal strips, or empty white overlay shapes.
- Cover metadata and objective copy sit directly on the canvas; if they need a panel to be readable, simplify the cover or move the detail to slide 2.
- Normal content slides keep the top rule, top-right blue marker, and bottom-right logo unless intentionally using cover/closing style.
- New slides match the simple white-and-blue corporate style.
- Titles are compact and aligned consistently.
- Editable text uses `微软雅黑` / `Microsoft YaHei` by default. Any non-YaHei font in normal text is intentional, not a leftover theme/default font.
- Normal editable text uses black or near-black, not muted gray, blue-gray, or pale low-contrast colors.
- Main content fits the center content area without covering the logo.
- The bottom-right logo itself is clear: no body text, table border, table fill, screenshot, annotation, chart, or shape overlaps the logo mark or its small breathing margin.
- Tables, screenshots, and callouts may use the logo's upper-left surrounding space when they do not cover the logo.
- No decorative gradients, stock-photo hero compositions, or marketing-style cards were introduced.
- No base-`pptx` colorful infographic style was introduced: multicolor numbered circles, rainbow card grids, alternating colored vertical bars, decorative icon grids, and heavy card shadows are blocking brand issues unless the user explicitly requested that style.
- Red text/boxes/arrows are reserved for warnings, risks, key callouts, and screenshot annotations. Green means completed/healthy/accepted; amber means pending/caution/needs confirmation. Color used only for decoration should be revised to the blue/black/white brand palette.

## Content Hygiene

- No source-deck training text remains unless explicitly requested.
- No old URLs, support contacts, email addresses, screenshots, product names, or credentials remain as accidental placeholders.
- Placeholder words such as `项目名称`, `汇报主题`, `章节标题`, `正文页标题`, `截图占位`, `说明`, `对比项`, `方案 A`, or `方案 B` do not remain in final deliverables.
- Screenshots belong to the current task and are readable.

Recommended placeholder check:

```bash
python -m markitdown output.pptx | grep -iE "项目名称|汇报主题|章节标题|正文页标题|对比表页标题|步骤说明页标题|说明页标题|问题说明页标题|截图占位|方案 A|方案 B|对比项|xxxx|lorem|ipsum"
```

## Practical Readability

- Dense tables remain legible after rendering.
- Normal 3-5 column tables with a few rows use `12-13 pt` body text; they do not waste space with small spreadsheet-like text inside oversized rows.
- Table cells are vertically middle-aligned by default; only paragraph/list/code-heavy cells use top alignment.
- Table horizontal alignment follows the content: short headers and categorical values are centered, while explanations, review comments, risks, evidence, and action text are left-aligned.
- Sparse slides do not leave small single-spaced text floating in a large blank canvas; body text is enlarged, given `1.5-1.7x` line spacing, or the slide is redesigned.
- Normal explanation/body slides use about `1.3-1.45x` line spacing; process cards, tables, captions, and footnotes use tighter spacing only when density requires it.
- Body text stays at or above `12 pt` outside tables, captions, labels, and footnotes; table body text stays at or above `9.5 pt`.
- Captions, notes, and sources are smaller but still black or near-black; do not make them light gray just to de-emphasize them.
- Red arrows/boxes point to the intended UI detail and do not cover important text.
- Multi-step screenshot pages read left to right.
- Body copy uses direct internal-document Chinese.
- No text, table grid, image, callout, or background shape overlaps the logo, page edge, screenshot, or table.
- No cover text is wrapped inside a redundant white filled shape or card.

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
- Inspect affected slides visually.
- Treat any content that overlaps the bottom-right logo mark as a blocking layout bug.
- Treat generic multicolor process decoration as a blocking brand bug when it comes from the base `pptx` visual style rather than from user-specified company material.
- Run zip and OpenXML validation after the last edit, not before.
- If a fix changes layout or package structure, re-render and re-validate.
- Do not treat the first render as proof. If any issue is found, fix it and re-run the affected QA layer before delivery.
