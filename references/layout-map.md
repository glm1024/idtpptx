# Layout Map

Use the template slides as reusable page types. Do not preserve source business content.

This file is the registered page-type map for `idtpptx`. It is a guardrail against free-form slide invention across different models and agents.

## Template Asset

Primary template:

`assets/templates/inspur-pragmatic-template-v1.pptx`

This template contains cleaned placeholder pages distilled from a pragmatic Inspur-style training deck.

## Registered Page Types

Use these registered page types before inventing anything new:

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

Before editing slide content, create a simple planning table:

| Page | Registered page type | Reason | Main material / screenshot slot | Logo risk |
|---|---|---|---|---|
| 1 | Cover | Title and version | None | Low |
| 2 | Text Explanation Page | Scope and audience | None | Low |
| 3 | Screenshot Step Page | Three UI actions | 3 screenshots, horizontal sequence | Medium |

Rules:

- Decide the full page sequence before replacing detailed text or media.
- Treat the planning table as a working artifact, not a slide. By default, final decks should not include an initial `目标 / 范围 / 产出` page when that page only explains how the PPT draft was produced.
- Do not create marketing landing pages, magazine-style spreads, Swiss-style poster pages, decorative hero images, WebGL/HTML slide structures, or arbitrary card grids inside this company PPTX skill.
- If a reusable company page type is missing, first describe it here as a registered page type with use cases, boundaries, and QA rules. Do not hide a new page type inside one deck as a one-off.
- If no registered type fits, default to Text Explanation Page and keep it restrained.

## Page Type Details

### 1. Cover

Use for the deck title.

Best for:

- Training title
- Project report title
- Internal manual title

Keep:

- Broad gray title band.
- Blue top band.
- Bottom-right logo.

Replace:

- Title text.
- Optional subtitle/date/department if the layout supports it.

Rules:

- Put date, version, department, and objective copy as plain text on the cover canvas.
- Do not create a white metadata card, white filled text box, white diagonal decoration, or empty white rectangle on top of the cover background.
- If the cover needs more explanation than a short objective line, move that explanation to the next slide instead of adding a white panel to the cover.

### 2. Section Divider

Use between major chapters.

Best for:

- Numbered training modules.
- Process phases.
- Report chapters.

Keep:

- Center blue bar.
- Section number block.
- Simple white section title.

### 3. Text Explanation Page

Use for definitions, context, principles, and plain explanation.

Best for:

- Background.
- Scope.
- Notes and constraints.
- Before/after explanation without screenshots.

Rules:

- Keep the top title compact.
- Use short paragraphs or grouped bullet-like lines.
- Use black or near-black body text; avoid gray explanatory text.
- If the slide has only a few lines and obvious blank space, use larger body text with `1.5-1.7x` line spacing instead of leaving small single-spaced text.
- For normal explanation pages, use `1.3-1.45x` body line spacing.
- If content becomes long, split into two slides instead of shrinking text too far.

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
- Avoid long narrative paragraphs.
- Use `1.3-1.45x` line spacing for diagnosis text; split the slide if the structure becomes visually cramped.

### 8. Process / Workflow Summary Page

Use for process logic, algorithm phases, review paths, or non-UI workflows.

Best for:

- Algorithm steps.
- Operational review process.
- Data flow or attribution flow.
- Multi-stage plan without screenshots.

Not for:

- UI click-by-click instructions that need screenshots.
- Quantitative comparisons that belong in a table or chart.
- Decorative pipeline art with no operational sequence.
- A deck-production plan, draft scope, or `初版目标与讨论范围` page. Those are working notes and should be removed from final PPT handoff unless explicitly requested.

Rules:

- Prefer a restrained blue/black sequence, a compact table, or a light line flow.
- Use simple numbered text labels or small blue tags instead of large multicolor circular badges.
- Do not use rainbow step cards, alternating colored vertical bars, or heavy shadow cards unless each color carries a documented business meaning.
- Reserve separate title and body zones inside each process card. If an English title wraps to two lines, move the body down, shorten the title, widen the card, stack fewer cards per row, or split the slide. Never let title text overlap body text.
- Keep card body text inside the card background. If a body sentence is wider than the card, wrap it, shorten it, or split the card; do not create a text box that spills across adjacent cards.
- Use Chinese-first process labels. English-only labels are acceptable only for real module names or standard abbreviations; otherwise translate them or use `中文（English）` on first mention.
- Keep the final step, callout, or summary from overlapping the bottom-right logo.
- Use real process stages. Do not invent numbers, percentages, or pseudo-KPIs just to make the layout feel fuller.

## Mapping Heuristics

- Decide the full slide sequence before editing individual slide content.
- Write the page planning table first for non-trivial decks.
- If the content is a new chapter, use Section Divider.
- If the content is a UI operation workflow, use Screenshot Step Page.
- If the content is a process or algorithm workflow without screenshots, use Process / Workflow Summary Page.
- If the content is a side-by-side decision, use Comparison Table or Choice/Recommendation.
- If the content is an exception or support answer, use Problem/Solution.
- If no strong pattern fits, use Text Explanation Page.
- Remove surplus placeholders, screenshot boxes, arrows, and table rows entirely; do not just clear their text.
- Before finalizing a slide, make sure the bottom-right logo remains uncovered; do not reserve a large empty area above or left of it.
- If a slide looks awkward after rendering, first reassess the page-type choice and material slot. Avoid fixing a wrong structure by adding random margins, shrinking text below readable size, or adding decorative boxes.
