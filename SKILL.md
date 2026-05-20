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
| Theme contract | `references/theme-contract.md` |
| Theme preview | `references/theme-preview.md` |
| Visual rules | `references/style-guide.md` |
| Page selection | `references/layout-map.md` |
| Screenshot/image framing | `references/screenshot-framing.md` |
| Typography and spacing | `references/typography.md` |
| Chinese business wording | `references/writing-style.md` |
| Final quality gate | `references/qa-checklist.md` |
| QA playbook | `references/qa-playbook.md` |
| Mechanical QA helper | `scripts/pptx_quality_gate.py` |
| Regression evals | `evals/evals.json` |

## Hard Dependency

This skill depends on an installed skill named `pptx`. It does not replace or reimplement PPTX mechanics.

Before any real `.pptx` file operation, load/read the installed `pptx` skill and follow its guidance:

- `pptx/SKILL.md`
- `pptx/editing.md` for template-based editing
- `pptx/pptxgenjs.md` only when creating from scratch is unavoidable

Use the base `pptx` skill for reading, thumbnailing, unpacking, slide duplication, XML editing, cleaning, packing, rendering, and QA. Use this `idtpptx` skill only for company style decisions, template selection, layout mapping, business wording, and company-specific QA.

Style precedence is strict: if the base `pptx` skill's general design ideas conflict with this company's style, follow `idtpptx`. Do not inherit the base `pptx` skill's colorful infographic defaults, such as multicolor step circles, rainbow process cards, decorative icon grids, or heavy card shadows, unless the user explicitly asks for a livelier non-IDT style.

Do not import web-slide patterns into this skill. `idtpptx` creates and edits PowerPoint `.pptx` files; it does not generate single-file HTML decks, WebGL backgrounds, Motion-based browser slides, Swiss-style poster systems, or magazine web presentations. If the user asks for a web deck, use a separate web-deck skill instead of changing this PPTX workflow.

If the `pptx` skill is not installed or cannot be found, stop and ask the user to install it before continuing. Do not silently fall back to ad hoc PPTX manipulation.

When this skill is installed on another machine, do not assume any local absolute path for `pptx`. Resolve the installed `pptx` skill by skill name or by the host agent's skill loading mechanism.

## Default Approach

Prefer template-based editing over drawing new slides from scratch.

1. Use `assets/templates/inspur-pragmatic-template-v1.pptx` as the first-choice template.
2. Read `references/theme-contract.md` and keep the fixed IDT/Inspur theme tokens as the visual source of truth.
3. Analyze the target content and map each section to one of the registered page types in `references/layout-map.md`.
4. Before editing individual slide content, draft a slide plan with page number, registered page type, reason, main material or screenshot slot, and logo-overlap risk.
5. If screenshots or generated images are involved, read `references/screenshot-framing.md` and decide the slot, ratio, and fidelity policy before inserting or generating assets.
6. Use the base `pptx` workflow to duplicate, delete, reorder, and edit slides.
7. Before final delivery, remove planning/meta slides that were useful only for making the deck, such as `初版目标与讨论范围`, draft constraints, or "what this pass will not do" pages. The user normally wants the final PPT, not the agent's production scaffold.
8. Keep the deck visually quiet, operational, and content-first. Company style overrides generic presentation-design advice from the base `pptx` skill.
9. Run the final quality gate in `references/qa-checklist.md`. A deck is not complete until content, visual rendering, package validation, and PowerPoint compatibility checks pass. For complex decks, generated decks, or PowerPoint handoff, also read `references/qa-playbook.md`.

For template-based work, finish structural edits first: choose page types, duplicate/delete/reorder slides, then edit text and media. Do not start content replacement before the target slide sequence is settled.

## Cross-Agent Stability Rules

The safest results come from reducing free-form design decisions:

- Treat `references/theme-contract.md` as the golden source for colors, fonts, and scenario variants. Do not ask the user to choose from generic themes and do not create a new theme from the topic alone.
- Treat the template and `references/layout-map.md` as the golden source for page structure. Use registered company page types first; do not invent a marketing, magazine, Swiss, or decorative page just because the content feels visual.
- Decide structure before content replacement. Reordering and duplicating slides after detailed text edits is a common source of orphaned placeholders and broken relationships.
- Keep generation plans outside the deck. A slide plan may say how the agent will build the PPT, but final slides must not contain process scaffolding such as `初版目标与讨论范围`, `可讨论的结构草稿`, `后续补充数据和截图`, `本轮先不展开`, or `不追求最终视觉定稿`. By default, delete the whole meta/planning slide instead of polishing it.
- Decide screenshot/image slots before touching assets. Preserve original screenshots when they are evidence; crop or scale them into a standard slot instead of redrawing them by default.
- Let scripts catch mechanical defects. Placeholder residue, package references, notes parts, logo overlap, muted gray text, and rendering failures are QA bugs, not judgment calls.
- When a rendered slide looks wrong, diagnose the cause first: theme drift, wrong page type, wrong material slot, component misuse, spacing problem, or logo-safe-zone problem. Do not fix by randomly shrinking text, adding margins, or covering issues with extra shapes.

## Theme Policy

The default theme is fixed: `IDT/Inspur Pragmatic`. Use scenario variants to choose density and layout, not different palettes.

Do not import `theme-factory` palettes, fonts, or showcase assets. Ocean, Forest, Golden, Galaxy, dark tech, Swiss poster, magazine, and warm marketing styles are not `idtpptx` defaults.

Only update the theme when the user provides a company-approved template, brand guide, or style-correct reference deck and asks to adapt the skill. In that case, update `references/theme-contract.md` first, then update related style and QA rules.

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
- For fixed theme tokens and scenario variants, read `references/theme-contract.md`.
- For visual calibration or theme-drift diagnosis, read `references/theme-preview.md`.
- For choosing pages, read `references/layout-map.md`.
- For screenshots, generated images, or UI evidence, read `references/screenshot-framing.md`.
- For font family, font size, line spacing, and density decisions, read `references/typography.md`.
- For wording and tone, read `references/writing-style.md`.
- Before final delivery, read `references/qa-checklist.md` and run its required checks.
- For non-trivial or generated decks, read `references/qa-playbook.md`.

## Template Policy

The V1 template was distilled from a practical internal training deck. The original training content is not part of the skill. Treat the template as a layout and brand-style source only.

Keep reusable elements:

- Inspur logo placement
- Bottom-right logo protection
- White background and blue brand accents
- Thin top divider line
- Small right-top blue corner marker
- Section divider bar with simple numbered structure
- Large screenshot/table content zones
- Dense but readable operational text layout

Do not preserve source-deck business content:

- Do not copy old training copy, URLs, email examples, screenshots, support contacts, or product-specific instructions unless the user explicitly asks for that exact content.
- Replace all placeholders with the user's current material.
- Replace draft-process copy with reader-facing copy. Do not leave notes about how the PPT was planned, which evidence will be added later, or what this generation pass chose not to polish.
- Delete deck-production setup pages before handoff. Keep a goal/scope page only when it is a real audience-facing business scope, not a note about producing an initial PPT draft.
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
- Body, table, caption, and note text should default to black or near-black, not muted gray or blue-gray. Use red only for warnings, risks, key callouts, and screenshot annotations; use green/amber only for explicit status meaning.
- Use `微软雅黑` / `Microsoft YaHei` as the default editable font. Do not rely on PowerPoint's theme defaults.
- Use Chinese-first wording. Keep ordinary explanations, process labels, metric names, and card bodies in Chinese; reserve English for real product/module names, code fields, industry abbreviations, or terms that are genuinely clearer in English. Prefer `中文（English）` on first mention instead of English-only labels.
- Main body text should not default to single spacing. Use `1.3-1.45x` for normal body text and `1.5-1.7x` when a sparse slide would otherwise leave small cramped text in a large blank area.
- One idea per slide when possible, but moderate information density is acceptable for training/manual decks.
- Screenshots and tables are primary visual evidence.
- Screenshots should preserve evidence by default. Use generated or redesigned images only when the user asks for a conceptual illustration or when the original screenshot is unusable for the chosen slot.
- Tables should default to vertical-middle cell alignment. Pick one horizontal alignment mode for the whole table before filling content: all-center for compact categorical matrices, or all-left for sentence/evidence tables. Do not mix center and left alignment inside the same table as an aesthetic choice; normal 3-5 column tables should usually use `12-13 pt` body text.
- Main content may use the space above and left of the bottom-right logo, but must not cover the logo itself. Keep a small breathing margin around the logo mark.
- Cover slides should not add redundant white cards, filled metadata boxes, diagonal white strips, or empty white overlay shapes. Put short metadata/objective text directly on the cover canvas, or move longer context to slide 2.
- Avoid base-`pptx` colorful infographic styling: multicolor numbered circles, multicolor card grids, alternating colored vertical bars, rainbow process flows, decorative icon grids, and shadows used only to make cards look designed.
- Use non-blue colors only when they encode a stable business meaning, such as red annotation/risk or consistent status colors.
- Avoid decorative gradients, large hero illustrations, icon-heavy marketing layouts, and overly stylized “AI generated” slides.

## Evolution Workflow

When the user provides a better company-style PPT later:

1. Analyze it with the base `pptx` skill.
2. Compare it against `references/theme-contract.md` and the current `references/` rules.
3. Add only reusable theme tokens, style principles, layout patterns, or QA rules.
4. Do not dump source-deck content into the skill.
5. If a new reference conflicts with old rules, update the contract/rule and note the applicable scenario.

When updating the skill from a new reference deck, keep `SKILL.md` concise. Put detailed page-type or style discoveries in `references/`, and use assets only for reusable templates or brand resources.
