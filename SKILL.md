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
| Official V1 template | `assets/templates/inspur-pragmatic-template-v1.pptx` |
| Theme contract | `references/theme-contract.md` |
| Theme preview | `references/theme-preview.md` |
| Visual rules | `references/style-guide.md` |
| Title system | `references/title-system.md` |
| Page selection | `references/layout-map.md` |
| Layout variants | `references/layout-registry.md` |
| Component system | `references/component-system.md` |
| Composition grammar | `references/composition-grammar.md` |
| Cleaned sample slide specs | `references/cleaned-layout-sample-specs.md` |
| Screenshot/image framing | `references/screenshot-framing.md` |
| Typography and spacing | `references/typography.md` |
| Text box containment | `references/text-box-fit.md` |
| Chinese business wording | `references/writing-style.md` |
| Reference deck inventory | `references/reference-deck-inventory.md` |
| Reference layout extraction | `references/reference-layout-extraction.md` |
| Final quality gate | `references/qa-checklist.md` |
| QA playbook | `references/qa-playbook.md` |
| Mechanical QA helper | `scripts/pptx_quality_gate.py` |
| Template builder | `scripts/build_template.py` |
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

Template-derived composition is the default delivery path. Do not create an
IDT/Inspur deck from zero when the company template is available, but also do
not make every deck a page-by-page clone of the V1 sample template.

1. Use `assets/templates/inspur-pragmatic-template-v1.pptx` as the only
   official V1 template for master chrome, logo, theme relationships, and visual
   calibration.
2. Read `references/theme-contract.md` and keep the fixed IDT/Inspur theme
   tokens as the visual source of truth.
3. Analyze the target content and map each section first to a registered page
   type in `references/layout-map.md`.
4. Read `references/component-system.md` and
   `references/composition-grammar.md`; choose components and composition
   recipes by content shape: screenshots, table density, process length,
   diagram width, conclusion priority, and logo risk.
5. Use `references/layout-registry.md` to choose a layout ID as a recipe, not as
   a mandatory full-slide clone. The cleaned V1 sample slide is a specimen and
   fallback, not the normal unit of generation.
6. Before editing individual slide content, draft a slide plan with page number,
   intent, layout ID, selected components, material shape, variant reason, and
   QA risk. Keep this plan outside the final deck.
7. If screenshots or generated images are involved, read
   `references/screenshot-framing.md` and decide the slot, ratio, and fidelity
   policy before inserting or generating assets.
8. Use the base `pptx` editing workflow to start from the V1 template, reuse
   master/layout chrome, duplicate/delete/reorder slides when useful, and build
   final pages by composing registered components in the real content zone.
9. Duplicate a cleaned sample slide only when its geometry genuinely matches the
   current content, or when a low-risk fallback is better than a one-off layout.
   If the deck begins to match the V1 sample sequence, re-plan from components.
10. Normalize slide titles with `references/title-system.md`: delete unneeded
    title/subtitle placeholders, keep one title system per slide, and balance
    title font size against the compact template title band.
11. For any card, note bar, callout, or framed component, follow
    `references/text-box-fit.md`: calculate the visible frame first, place text
    in an inner box, enable wrapping, and shorten/split content before it can
    run outside the frame.
12. Before final delivery, remove planning/meta slides that were useful only for
    making the deck, such as `初版目标与讨论范围`, draft constraints, or "what this
    pass will not do" pages. The user normally wants the final PPT, not the
    agent's production scaffold.
13. Keep the deck visually quiet, operational, and content-first. Company style
    overrides generic presentation-design advice from the base `pptx` skill.
14. Run the final quality gate in `references/qa-checklist.md`. A deck is not
    complete until content, visual rendering, package validation, and PowerPoint
    compatibility checks pass. For complex decks, generated decks, or
    PowerPoint handoff, also read `references/qa-playbook.md`.

For template-based work, finish structural edits first: choose page intents,
components, recipes, and slide order; then edit text and media. Do not start
content replacement before the target slide sequence and component plan are
settled.

If a task asks for a new company-style deck but does not explicitly forbid using
the template, treat it as template-derived composition. In particular, do not
jump to PptxGenJS just because the base `pptx` skill offers a "create from
scratch" path.

## Cross-Agent Stability Rules

The safest results come from reducing free-form design decisions:

- Treat `references/theme-contract.md` as the golden source for colors, fonts, and scenario variants. Do not ask the user to choose from generic themes and do not create a new theme from the topic alone.
- Treat the template, `references/layout-map.md`, `references/layout-registry.md`, `references/component-system.md`, and `references/composition-grammar.md` as the golden source for page structure. Use registered company page types, recipes, and components first; do not invent a marketing, magazine, Swiss, or decorative page just because the content feels visual.
- Treat layout IDs as recipes. A cleaned V1 sample slide shows one valid specimen, not the only valid final page.
- Do not choose layouts randomly for visual variety. Variety must come from content shape: number of screenshots, table density, process steps, diagram width, conclusion priority, and evidence type.
- Avoid template-clone decks. If the generated deck follows the V1 sample slide count, order, and geometry too closely, re-plan from components instead of adding decoration.
- Decide structure before content replacement. Reordering and duplicating slides after detailed text edits is a common source of orphaned placeholders and broken relationships.
- Keep generation plans outside the deck. A slide plan may say how the agent will build the PPT, but final slides must not contain process scaffolding such as `初版目标与讨论范围`, `可讨论的结构草稿`, `后续补充数据和截图`, `本轮先不展开`, or `不追求最终视觉定稿`. By default, delete the whole meta/planning slide instead of polishing it.
- Clean title placeholders before polishing. Final decks must not show PowerPoint default prompts such as `单击此处添加标题` / `Click to add title`, and section divider pages should not keep a top-left title placeholder in addition to the center section bar.
- Treat framed text containment as geometry, not decoration. A card body, note-bar sentence, or callout paragraph must be generated inside that frame's inner text box; do not create a row-wide text box over several cards and rely on visual wrapping.
- Decide screenshot/image slots before touching assets. Preserve original screenshots when they are evidence; crop or scale them into a standard slot instead of redrawing them by default.
- Let scripts catch mechanical defects. Placeholder residue, package references, notes parts, logo overlap, muted gray text, and rendering failures are QA bugs, not judgment calls.
- When a rendered slide looks wrong, diagnose the cause first: theme drift, wrong page type, wrong material slot, component misuse, spacing problem, or logo-safe-zone problem. Do not fix by randomly shrinking text, adding margins, or covering issues with extra shapes.

## Theme Policy

The default theme is fixed: `IDT/Inspur Pragmatic`. Use scenario variants to choose density and layout, not different palettes.

Do not import `theme-factory` palettes, fonts, or showcase assets. Ocean, Forest, Golden, Galaxy, dark tech, Swiss poster, magazine, and warm marketing styles are not `idtpptx` defaults.

Only update the theme when the user provides a company-approved template, brand guide, or style-correct reference deck and asks to adapt the skill. In that case, update `references/theme-contract.md` first, then update related style and QA rules.

## Template-Derived Composition Policy

Do not treat `idtpptx` as permission to bypass the base `pptx` skill. The safest path is still:

1. Start from the `idtpptx` template.
2. Reuse template masters, layouts, placeholders, logo/media relationships, and existing brand elements wherever possible.
3. Compose final slides from registered components and recipes.
4. Duplicate, delete, reorder, and edit cleaned sample slides only when they are a genuine fit or a deliberate fallback.

PptxGenJS is a fallback, not the normal `idtpptx` route. Use PptxGenJS or another from-scratch generator only when one of these is true:

- No usable company template or reference deck is available.
- The user explicitly asks for a scratch-generated deck or prototype.
- The requested structure cannot be produced by template-derived component composition, and you explain that tradeoff before delivery.

When the template contains the logo or other shared brand media, do not embed a new copy of the same logo on every slide. Prefer the template's master/layout logo or reuse the existing media relationship. Per-slide duplicate image embedding is a PowerPoint compatibility risk and should be treated as a warning sign during QA.

Do not draw a second presentation shell inside the template. If a template layout already provides the top rule, page marker, logo, or other page chrome, do not manually add another title bar, page number, footer logo, or slide frame in generated code. Use the registered template page's real content zone and compose within it. A rendered slide where the material sits only in the upper-left while the right and bottom remain mostly empty should be treated as a structure bug, not as acceptable whitespace.

If PptxGenJS or another generator is used from scratch, run an explicit PowerPoint-compatibility cleanup before delivery:

- Remove unintentional `ppt/notesSlides/` and `ppt/notesMasters/` parts unless speaker notes are explicitly required.
- Remove notes relationships, notes content type overrides, and `p:notesMasterIdLst` when notes are not required.
- Normalize generated line shapes so `a:xfrm/a:ext` `cx` and `cy` are never negative. Use `flipH` or `flipV` to preserve direction.
- Remove `[Content_Types].xml` overrides for parts that do not exist in the package.
- Validate picture/media relationships: every `a:blip` embed must resolve to an existing internal image part with a valid image content type and decodable image bytes.
- Treat generic attachment/package icons, broken images, or PowerPoint "repair" prompts as delivery blockers even when LibreOffice renders the deck.
- Run `scripts/pptx_quality_gate.py`; do not deliver if it reports `BLOCK`.

## What To Load

- For visual rules, read `references/style-guide.md`.
- For fixed theme tokens and scenario variants, read `references/theme-contract.md`.
- For visual calibration or theme-drift diagnosis, read `references/theme-preview.md`.
- For title placeholder cleanup, title zone sizing, and title font-size decisions, read `references/title-system.md`.
- For choosing pages, read `references/layout-map.md`.
- For choosing among layout variants such as `COV-01`, `TBL-02`, or `SS-02`, read `references/layout-registry.md`.
- For component-level building blocks, read `references/component-system.md`.
- For combining components into varied pages, read `references/composition-grammar.md`.
- For building or updating cleaned sample slides in the V1 template, read `references/cleaned-layout-sample-specs.md`.
- For screenshots, generated images, or UI evidence, read `references/screenshot-framing.md`.
- For font family, font size, line spacing, and density decisions, read `references/typography.md`.
- For cards, note bars, callouts, conclusion boxes, or any framed text component, read `references/text-box-fit.md`.
- For wording and tone, read `references/writing-style.md`.
- When evolving templates or adding layout IDs from local reference decks, read `references/reference-deck-inventory.md` and `references/reference-layout-extraction.md`; absorb rules and slot contracts, not source deck content.
- Before final delivery, read `references/qa-checklist.md` and run its required checks.
- For non-trivial or generated decks, read `references/qa-playbook.md`.

## Template Policy

The V1 template was distilled from practical internal decks. The original
business content is not part of the skill. Treat the template as a master
chrome, brand-style source, component specimen board, and fallback reference,
not as a fixed deck that should be cloned page by page.

Keep the distributable skill small. `assets/templates/` should contain only the
single official V1 company template and reusable brand assets needed at
generation time. Do not place raw reference PPT collections, source decks,
customer/project decks, or large local research corpora inside the skill root.
Keep those materials outside this repository, for example in a local-only
sibling directory such as `../ppt-reference/`, and distill their lessons into
`references/reference-deck-inventory.md` or registered layout rules before
using them.

Template direction:

- Treat `assets/templates/inspur-pragmatic-template-v1.pptx` as the only
  official V1 template used by agents.
- The V1 template contains cleaned sample slides for registered variants,
  currently `COV-02A`, `DIR-01A`, `PRC-03A`, `SS-02A`, `SS-03A`, `ARC-01A`,
  `ARC-02A`, `ARC-03A`, `TBL-02A`, `TBL-03A`, and `SUM-02A`.
- These sample slides are specimens and fallbacks. They demonstrate one valid
  composition for each recipe, but final decks should be built by content-driven
  component composition unless the sample geometry is genuinely the best fit.
- Prefer a Guizang-style mechanism adapted to native PPTX: one compact company
  template + registered components + recipe IDs + slot rules + QA checks.
- Do not create a second PPT template for normal use.
  Keep one V1 template and rebuild it through `scripts/build_template.py`.
- Before adding `COV-02`, `DIR-01`, `PRC-03`, `SS-02`, `SS-03`, `ARC-01`,
  `ARC-02`, `ARC-03`, `TBL-02`, `TBL-03`, `SUM-02`, or any other cleaned
  sample to the V1 template, follow `references/cleaned-layout-sample-specs.md`
  for geometry, placeholder content, and promotion checks.

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
- Delete unused title/subtitle placeholders entirely. Do not clear a title placeholder and leave the shape behind, because PowerPoint can show `单击此处添加标题` or `单击此处添加副标题` in edit mode.
- Replace draft-process copy with reader-facing copy. Do not leave notes about how the PPT was planned, which evidence will be added later, or what this generation pass chose not to polish.
- Delete deck-production setup pages before handoff. Keep a goal/scope page only when it is a real audience-facing business scope, not a note about producing an initial PPT draft.
- If a screenshot slot is not needed, remove the entire placeholder group instead of leaving empty boxes.

Before declaring a deck complete, run the full QA checklist in `references/qa-checklist.md`. At minimum, extract text and check for leftover template placeholders. Treat any hit as a bug:

```bash
python -m markitdown output.pptx | grep -iE "项目名称|汇报主题|章节标题|正文页标题|对比表页标题|步骤说明页标题|说明页标题|问题说明页标题|截图占位|方案 A|方案 B|对比项|单击此处添加|点击此处添加|click[[:space:]]+to[[:space:]]+add|xxxx|lorem|ipsum"
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
- Normal content titles should use a compact title band: delete stale title placeholders first, then use about `24-30 pt` title text rather than stretching a large PowerPoint placeholder.
- Body, table, caption, and note text should default to black or near-black, not muted gray or blue-gray. Use red only for warnings, risks, key callouts, and screenshot annotations; use green/amber only for explicit status meaning.
- Use `微软雅黑` / `Microsoft YaHei` as the default editable font. Do not rely on PowerPoint's theme defaults.
- Use Chinese-first wording. Keep ordinary explanations, process labels, metric names, and card bodies in Chinese; reserve English for real product/module names, code fields, industry abbreviations, or terms that are genuinely clearer in English. Prefer `中文（English）` on first mention instead of English-only labels.
- Main body text should not default to single spacing. Use `1.3-1.45x` for normal body text and `1.5-1.7x` when a sparse slide would otherwise leave small cramped text in a large blank area.
- One idea per slide when possible, but moderate information density is acceptable for training/manual decks.
- Screenshots and tables are primary visual evidence.
- Screenshots should preserve evidence by default. Use generated or redesigned images only when the user asks for a conceptual illustration or when the original screenshot is unusable for the chosen slot.
- Tables should default to vertical-middle cell alignment. Pick one horizontal alignment mode for the whole table before filling content: all-center for compact categorical matrices, or all-left for sentence/evidence tables. Do not mix center and left alignment inside the same table as an aesthetic choice; normal 3-5 column tables should usually use `12-13 pt` body text.
- Framed text must stay inside its visible frame in both horizontal and vertical directions. Use an inner text box, wrapping, and content reduction; if it still does not fit at readable size, split the card row or slide.
- Main content may use the space above and left of the bottom-right logo, but must not cover the logo itself. Keep a small breathing margin around the logo mark.
- Reuse the finite component system for variety. A deck should feel like the
  same company style, not the same sample slide sequence with replaced text.
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

If several company reference decks are collected at once, inventory them first in
`references/reference-deck-inventory.md`. Do not merge decks into the template
or copy slides into assets until the reusable layout pattern has a registered
page type, slot rules, and QA boundaries.
