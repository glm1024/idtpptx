# Layout Map

Use registered page types as composition recipes. Do not preserve source
business content, and do not treat template sample slides as fixed final pages.

This file is the registered page-type map for `idtpptx`. It is a guardrail
against free-form slide invention across different models and agents, while
still allowing content-driven component composition.

For specific layout variants and IDs, read `references/layout-registry.md` after
choosing the broad page type here.

For component selection and page composition, read
`references/component-system.md` and `references/composition-grammar.md`.

## Template Asset

Primary template:

`assets/templates/inspur-pragmatic-template-v1.pptx`

This template contains master chrome, logo/media relationships, and cleaned
sample pages distilled from a pragmatic Inspur-style reference corpus. The
sample pages are specimens and fallbacks for cover, directory/progress,
roadmap, screenshot, troubleshooting, architecture, table, and handoff recipes.
They are not a mandatory final deck sequence.

## Registered Page Types

Use these registered page types before inventing anything new. Then select a
specific layout ID from `references/layout-registry.md` when more than one
variant is available.

| Type | Use For |
|---|---|
| Cover | Deck title and short metadata |
| Section Divider | Major chapter breaks |
| Text Explanation Page | Context, definitions, constraints, principles |
| Comparison Table Page | Matrices, feature comparisons, responsibility lists |
| Screenshot Step Page | UI walkthroughs and operation manuals |
| Choice/Recommendation Page | Options, scenario choices, recommended paths |
| Problem/Solution Page | FAQ, troubleshooting, known issues |
| Process / Workflow Summary Page | Non-UI process, algorithm, review, or data flow |
| Summary / Handoff Page | Final conclusion, decision recap, owners, dates, next actions |

Before editing slide content, create a simple planning table:

| Page | Layout ID | Registered page type | Reason | Main material / screenshot slot | Logo risk |
|---|---|---|---|---|---|
| 1 | `COV-01` | Cover | Title and version | None | Low |
| 2 | `TXT-01` | Text Explanation Page | Scope and audience | None | Low |
| 3 | `SS-02` | Screenshot Step Page | Three UI actions | 3 screenshots, horizontal sequence | Medium |

Rules:

- Decide the full page sequence, page intent, layout ID, and component plan
  before replacing detailed text or media.
- Use layout IDs as recipes, not as instructions to clone full sample slides.
- Generate variety through registered components and content-driven composition:
  table density, screenshot count, process length, diagram width, and conclusion
  priority.
- Do not choose layouts randomly to make slides look different. If more than one
  recipe fits, choose the one whose slots match the material most directly.
- Use the registered template content zone at full slide scale. Do not place a compact mini-layout in the upper-left while leaving most of the right side and lower half empty.
- Clean title placeholders before detailed content work. Replace the real page title, delete unused title/subtitle placeholders, and keep one title system per slide.
- Reuse the template's page chrome. Do not add a second top rule, page marker, footer/logo, or artificial slide frame inside the existing template frame.
- Treat the planning table as a working artifact, not a slide. By default, final decks should not include an initial `目标 / 范围 / 产出` page when that page only explains how the PPT draft was produced.
- Do not create marketing landing pages, magazine-style spreads, Swiss-style poster pages, decorative hero images, WebGL/HTML slide structures, or arbitrary card grids inside this company PPTX skill.
- If a reusable company page type is missing, first describe it here as a registered page type with use cases, boundaries, and QA rules. If only a variant is missing under an existing page type, register it in `references/layout-registry.md`. Do not hide a new page type inside one deck as a one-off.
- If no registered type fits, default to Text Explanation Page and keep it restrained.
- For any registered page type that uses visible cards, callouts, note bars, or conclusion boxes, apply `references/text-box-fit.md`: the visible frame owns an inner text zone, and text must not extend beyond the frame.
- If the generated deck has the same count, order, and geometry as the V1
  sample template, treat it as a template-clone risk and re-plan from
  `references/composition-grammar.md`.

## Page Type Details

### 1. Cover

Use for the deck title.

Best for:

- Training title
- Project report title
- Internal manual title
- Formal review / leadership update title, when using `COV-02`

Keep:

- Broad gray title band.
- Blue top band.
- Bottom-right logo.

Replace:

- Title text.
- Optional subtitle/date/department if the layout supports it.

Rules:

- Put date, version, department, and objective copy as plain text on the cover canvas.
- Keep one main title and one optional real subtitle. Delete any duplicated or unneeded title/subtitle placeholders before adjusting font size.
- Do not create a white metadata card, white filled text box, white diagonal decoration, or empty white rectangle on top of the cover background.
- Keep date/version metadata inside the gray band; do not let it touch the gray/white boundary above the logo area.
- Use `COV-01` for normal training/report covers and `COV-02` for formal review covers that need a stronger centered title.
- If the cover needs more explanation than a short objective line, move that explanation to the next slide instead of adding a white panel to the cover.

### 2. Section Divider

Use between major chapters, or when a long deck needs a directory/progress
orientation page.

Best for:

- Numbered training modules.
- Process phases.
- Report chapters.
- 3-6 item directory/progress maps, using `DIR-01`.

Keep:

- Center blue bar.
- Section number block.
- Simple white section title.

Remove:

- Any top-left title placeholder inherited from a content layout.
- Any PowerPoint default prompt such as `单击此处添加标题`.

### 3. Text Explanation Page

Use for definitions, context, principles, and plain explanation.

Best for:

- Background.
- Scope.
- Notes and constraints.
- Before/after explanation without screenshots.

Rules:

- Keep the top title compact.
- Normal title text should usually be `24-30 pt`, with body content starting around `1.15-1.35 in` from the top. If the title area feels too tall, compress the title zone before shrinking body content.
- Use short paragraphs or grouped bullet-like lines.
- Use black or near-black body text; avoid gray explanatory text.
- If the slide has only a few lines and obvious blank space, use larger body text with `1.5-1.7x` line spacing instead of leaving small single-spaced text.
- For normal explanation pages, use `1.3-1.45x` body line spacing.
- If content becomes long, split into two slides instead of shrinking text too far.
- If this is the final page and the audience needs conclusion, owner, date, and
  next action fields, use `SUM-02` instead of a generic text page or decorative
  thank-you page.

### 4. Comparison Table Page

Use for feature comparisons, matrix decisions, lists with dates/status, or export plans.

Best for:

- Feature matrix.
- System comparison.
- Responsibility table.
- Export/import list.

Not for:

- Full operational walkthroughs with several UI screenshots.
- Narrative explanation that reads better as grouped text.
- Data-dense appendices that need multiple pages.

Rules:

- Keep table borders light.
- Prefer fewer columns and readable row height.
- Use black or near-black table text by default; do not use gray text for body cells.
- Vertically align table text to the middle by default. Use top alignment only for paragraph-like cells, bullet lists, code, or cells with `3+` wrapped lines.
- Choose one horizontal alignment mode for the whole table before writing cell text. Use all-center mode only when the table is mostly short categorical values; use all-left mode when it contains explanations, evidence, risks, actions, or sentence-like text.
- Header row follows the same horizontal mode as the body. Do not create a centered header row with mixed left/center body cells unless a provided source table explicitly requires it.
- If columns need very different alignment treatments, the content probably needs a different layout, a split table, or shorter wording instead of a mixed-alignment table.
- Use `12-13 pt` body text for normal 3-5 column tables with 3-7 rows. Use `10.5-11.5 pt` only for genuinely dense tables.
- Use `1.05-1.18x` table line spacing and balanced cell padding; do not stretch rows while keeping the text small.
- If table is too dense, split by category.
- Never let the table frame, last column, row fill, or cell text overlap the bottom-right logo. The space above and left of the logo remains usable.

### 5. Screenshot Step Page

Use for operation manuals and UI walkthroughs.

Best for:

- Product operation steps.
- Admin-console instructions.
- Before/after UI states.

Not for:

- Abstract process or algorithm explanation without UI evidence.
- Screenshots that are too small to inspect at presentation size.
- Decorative product mockups or generated hero art.

Rules:

- Use one to three screenshots.
- Use red arrows between screenshots for sequence.
- Add concise text above the screenshots.
- For troubleshooting with one evidence screenshot plus `现象 / 判断 / 处理`,
  use `SS-03` instead of forcing the content into a generic FAQ page.
- Keep screenshot captions and step labels compact, usually `10-12 pt` with `1.0-1.2x` line spacing.
- Remove unused screenshot placeholders entirely.
- Keep screenshots, arrows, and annotation boxes off the bottom-right logo itself. If the screenshot must be large, crop the meaningful area instead of covering the logo.
- Read `references/screenshot-framing.md` before resizing, cropping, beautifying, or regenerating screenshots.
- Preserve screenshot content by default. Redesign or regenerate a UI image only when the user asks for it or when the original screenshot cannot communicate the needed evidence in a readable slot.

### 6. Choice/Recommendation Page

Use when explaining options and recommending a path.

Best for:

- Configuration choices.
- Scenario-based guidance.
- Recommended vs fallback approach.

Rules:

- Keep the explanation direct.
- Number options with Chinese full-width parentheses when writing Chinese documents.
- Use `1.3-1.45x` line spacing for option explanations, or `1.5x` when there are only two or three short options.
- If using a conclusion bar, note box, or callout background, wrap the text inside that background with padding. Do not let the text box extend outside the filled area.
- Calculate the conclusion/note/callout inner box before inserting text. If the sentence does not fit, shorten it or increase the bar height; do not place a wider text box over the page.
- End with a short next-step sentence.

### 7. Problem/Solution Page

Use for FAQ, troubleshooting, risk notes, or known issues.

Best for:

- Common problem and answer.
- Symptom, reason, solution.
- Operational exception handling.

Rules:

- Use a stable structure: 问题 / 原因 / 解决.
- Use screenshots only when they materially help diagnosis.
- If the screenshot is the main evidence, switch to `SS-03` so the screenshot
  gets a real evidence slot and the diagnosis text stays in fixed blocks.
- Avoid long narrative paragraphs.
- Use `1.3-1.45x` line spacing for diagnosis text; split the slide if the structure becomes visually cramped.

### 8. Process / Workflow Summary Page

Use for process logic, algorithm phases, review paths, or non-UI workflows.

Best for:

- Algorithm steps.
- Operational review process.
- Data flow or attribution flow.
- Multi-stage plan without screenshots.
- Technical architecture or topology diagrams when selected through `ARC-01`
  or `ARC-02` in `references/layout-registry.md`.

Not for:

- UI click-by-click instructions that need screenshots.
- Quantitative comparisons that belong in a table or chart.
- Decorative pipeline art with no operational sequence.
- A deck-production plan, draft scope, or `初版目标与讨论范围` page. Those are working notes and should be removed from final PPT handoff unless explicitly requested.

Rules:

- Prefer a restrained blue/black sequence, a compact table, or a light line flow.
- For technical diagrams, pick `ARC-01` when the explanation and diagram share
  the slide; pick `ARC-02` when the diagram must be full width to keep labels
  readable.
- For phased rollout or month-by-month planning, pick `PRC-03` instead of a
  generic process card row.
- Use simple numbered text labels or small blue tags instead of large multicolor circular badges.
- Do not use rainbow step cards, alternating colored vertical bars, or heavy shadow cards unless each color carries a documented business meaning.
- Reserve separate title and body zones inside each process card. If an English title wraps to two lines, move the body down, shorten the title, widen the card, stack fewer cards per row, or split the slide. Never let title text overlap body text.
- Keep card body text inside the card background. Build each card with a fixed inner body box; if a body sentence is wider or taller than that inner box, wrap it, shorten it, reduce cards per row, switch to a table, or split the slide. Do not create a text box that spills across adjacent cards.
- Use Chinese-first process labels. English-only labels are acceptable only for real module names or standard abbreviations; otherwise translate them or use `中文（English）` on first mention.
- Keep the final step, callout, or summary from overlapping the bottom-right logo.
- Use real process stages. Do not invent numbers, percentages, or pseudo-KPIs just to make the layout feel fuller.

### 9. Summary / Handoff Page

Use for final reader-facing conclusions and review handoff.

Best for:

- Final decision recap after a technical方案评审.
- Closing page that needs owner/date/action fields.
- Internal review material where the next step must be explicit.

Not for:

- Decorative `谢谢` / `THANKS` pages.
- Deck-production notes about what the agent will do next.
- Long work plans with many rows; those belong in a table page or appendix.

Rules:

- Use `SUM-01` for a restrained high-level summary / next-steps page.
- Use `SUM-02` when the slide needs decision, owner, date, and next action
  slots.
- Lead with the conclusion, then show responsibility and follow-up actions.
- Keep all handoff text inside fixed frames with inner padding; do not let the
  table, note strip, or decision blocks overlap the bottom-right logo.

## Mapping Heuristics

- Decide the full slide sequence before editing individual slide content.
- Write the page planning table first for non-trivial decks.
- Select a concrete layout ID from `references/layout-registry.md` after the broad page type is chosen. Do not pick a variant randomly.
- If the content is a new chapter, use Section Divider.
- If the content is a UI operation workflow, use Screenshot Step Page.
- If the content is a process or algorithm workflow without screenshots, use Process / Workflow Summary Page.
- If the content is a side-by-side decision, use Comparison Table or Choice/Recommendation.
- If the content is an exception or support answer, use Problem/Solution.
- If the content is a final decision, owner/date/action handoff, or review
  closeout, use Summary / Handoff Page.
- If no strong pattern fits, use Text Explanation Page.
- Remove surplus placeholders, screenshot boxes, arrows, and table rows entirely; do not just clear their text.
- Before finalizing a slide, make sure the bottom-right logo remains uncovered; do not reserve a large empty area above or left of it.
- If rendered content looks like a small slide nested inside the template, pick a registered page type with a larger content slot, widen the table/process/screenshot group, or split the material. Do not fix it by adding another logo, page number, frame, or decorative empty panel.
- If a slide looks awkward after rendering, first reassess the page-type choice and material slot. Avoid fixing a wrong structure by adding random margins, shrinking text below readable size, or adding decorative boxes.
