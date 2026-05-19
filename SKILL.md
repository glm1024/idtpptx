---
name: idtpptx
description: Use when creating or editing PowerPoint/PPTX files that should follow the company's IDT/Inspur pragmatic presentation style. This is an overlay skill that depends on the existing pptx skill for all PPTX file operations, and adds company-specific template selection, layout mapping, writing style, and visual QA rules.
license: Proprietary. LICENSE.txt has complete terms.
---

# IDT PPTX

This skill creates and edits company-style PowerPoint decks using a simple, pragmatic Inspur/IDT visual language.

## Quick Reference

| Task | What to use |
|------|-------------|
| PPTX mechanics | Load the installed `pptx` skill |
| First-choice template | `assets/templates/inspur-pragmatic-template-v1.pptx` |
| Visual rules | `references/style-guide.md` |
| Page selection | `references/layout-map.md` |
| Typography and spacing | `references/typography.md` |
| Chinese business wording | `references/writing-style.md` |
| Final quality gate | `references/qa-checklist.md` |
| QA playbook | `references/qa-playbook.md` |
| Mechanical QA helper | `scripts/pptx_quality_gate.py` |

## Hard Dependency

This skill depends on an installed skill named `pptx`. It does not replace or reimplement PPTX mechanics.

Before any real `.pptx` file operation, load/read the installed `pptx` skill and follow its guidance:

- `pptx/SKILL.md`
- `pptx/editing.md` for template-based editing
- `pptx/pptxgenjs.md` only when creating from scratch is unavoidable

Use the base `pptx` skill for reading, thumbnailing, unpacking, slide duplication, XML editing, cleaning, packing, rendering, and QA. Use this `idtpptx` skill only for company style decisions, template selection, layout mapping, business wording, and company-specific QA.

If the `pptx` skill is not installed or cannot be found, stop and ask the user to install it before continuing. Do not silently fall back to ad hoc PPTX manipulation.

When this skill is installed on another machine, do not assume any local absolute path for `pptx`. Resolve the installed `pptx` skill by skill name or by the host agent's skill loading mechanism.

## Default Approach

Prefer template-based editing over drawing new slides from scratch.

1. Use `assets/templates/inspur-pragmatic-template-v1.pptx` as the first-choice template.
2. Analyze the target content and map each section to one of the reusable page types in `references/layout-map.md`.
3. Use the base `pptx` workflow to duplicate, delete, reorder, and edit slides.
4. Keep the deck visually quiet, operational, and content-first.
5. Run the final quality gate in `references/qa-checklist.md`. A deck is not complete until content, visual rendering, package validation, and PowerPoint compatibility checks pass. For complex decks, generated decks, or PowerPoint handoff, also read `references/qa-playbook.md`.

For template-based work, finish structural edits first: choose page types, duplicate/delete/reorder slides, then edit text and media. Do not start content replacement before the target slide sequence is settled.

## Generation Policy

Do not treat `idtpptx` as permission to bypass the base `pptx` skill. The safest path is still:

1. Start from the `idtpptx` template.
2. Use the base `pptx` editing workflow to duplicate, delete, reorder, and edit slides.
3. Use PptxGenJS from scratch only when template-based editing is truly not practical.

If PptxGenJS or another generator is used from scratch, run an explicit PowerPoint-compatibility cleanup before delivery:

- Remove unintentional `ppt/notesSlides/` and `ppt/notesMasters/` parts unless speaker notes are explicitly required.
- Remove notes relationships, notes content type overrides, and `p:notesMasterIdLst` when notes are not required.
- Normalize generated line shapes so `a:xfrm/a:ext` `cx` and `cy` are never negative. Use `flipH` or `flipV` to preserve direction.
- Remove `[Content_Types].xml` overrides for parts that do not exist in the package.
- Run `scripts/pptx_quality_gate.py`; do not deliver if it reports `BLOCK`.

## What To Load

- For visual rules, read `references/style-guide.md`.
- For choosing pages, read `references/layout-map.md`.
- For font family, font size, line spacing, and density decisions, read `references/typography.md`.
- For wording and tone, read `references/writing-style.md`.
- Before final delivery, read `references/qa-checklist.md` and run its required checks.
- For non-trivial or generated decks, read `references/qa-playbook.md`.

## Template Policy

The V1 template was distilled from a practical internal training deck. The original training content is not part of the skill. Treat the template as a layout and brand-style source only.

Keep reusable elements:

- Inspur logo placement
- Bottom-right logo safe zone
- White background and blue brand accents
- Thin top divider line
- Small right-top blue corner marker
- Section divider bar with simple numbered structure
- Large screenshot/table content zones
- Dense but readable operational text layout

Do not preserve source-deck business content:

- Do not copy old training copy, URLs, email examples, screenshots, support contacts, or product-specific instructions unless the user explicitly asks for that exact content.
- Replace all placeholders with the user's current material.
- If a screenshot slot is not needed, remove the entire placeholder group instead of leaving empty boxes.

Before declaring a deck complete, run the full QA checklist in `references/qa-checklist.md`. At minimum, extract text and check for leftover template placeholders. Treat any hit as a bug:

```bash
python -m markitdown output.pptx | grep -iE "项目名称|汇报主题|章节标题|正文页标题|对比表页标题|步骤说明页标题|说明页标题|问题说明页标题|截图占位|方案 A|方案 B|对比项|xxxx|lorem|ipsum"
```

When possible, run the bundled helper:

```bash
python scripts/pptx_quality_gate.py output.pptx --outdir /tmp/idtpptx-qa
```

If helper dependencies are installed under a different interpreter, pass it explicitly:

```bash
python scripts/pptx_quality_gate.py output.pptx --outdir /tmp/idtpptx-qa --python python
```

## Style Summary

The style is practical corporate training/reporting, not a marketing deck:

- White canvas, restrained blue accents, minimal decoration.
- Clear top title area, mostly left-aligned text.
- Use `微软雅黑` / `Microsoft YaHei` as the default editable font. Do not rely on PowerPoint's theme defaults.
- Main body text should not default to single spacing. Use `1.3-1.45x` for normal body text and `1.5-1.7x` when a sparse slide would otherwise leave small cramped text in a large blank area.
- One idea per slide when possible, but moderate information density is acceptable for training/manual decks.
- Screenshots and tables are primary visual evidence.
- Tables should default to vertical-middle cell alignment. Center short categorical values, but left-align descriptive text; normal 3-5 column tables should usually use `12-13 pt` body text.
- Main content must not enter the bottom-right logo safe zone. If a table, screenshot, callout, or text block reaches the logo area, resize it, split the slide, or move the content upward/left.
- Cover slides should not add redundant white cards, filled metadata boxes, diagonal white strips, or empty white overlay shapes. Put short metadata/objective text directly on the cover canvas, or move longer context to slide 2.
- Avoid decorative gradients, large hero illustrations, icon-heavy marketing layouts, and overly stylized “AI generated” slides.

## Evolution Workflow

When the user provides a better company-style PPT later:

1. Analyze it with the base `pptx` skill.
2. Compare it against the current `references/` rules.
3. Add only reusable style principles, layout patterns, or QA rules.
4. Do not dump source-deck content into the skill.
5. If a new reference conflicts with old rules, update the rule and note the applicable scenario.

When updating the skill from a new reference deck, keep `SKILL.md` concise. Put detailed page-type or style discoveries in `references/`, and use assets only for reusable templates or brand resources.
