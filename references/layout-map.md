# Layout Map

Use the template slides as reusable page types. Do not preserve source business content.

## Template Asset

Primary template:

`assets/templates/inspur-pragmatic-template-v1.pptx`

This template contains cleaned placeholder pages distilled from a pragmatic Inspur-style training deck.

## Page Types

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

Rules:

- Keep table borders light.
- Prefer fewer columns and readable row height.
- Vertically align table text to the middle by default. Use top alignment only for paragraph-like cells, bullet lists, code, or cells with `3+` wrapped lines.
- Header row should usually be centered horizontally and vertically.
- Horizontally center short categorical columns such as module, status, owner, date, count, percentage, and short capability labels.
- Left-align descriptive columns such as current path, review comment, risk, evidence, action, and sentence-like explanations.
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

Rules:

- Use one to three screenshots.
- Use red arrows between screenshots for sequence.
- Add concise text above the screenshots.
- Keep screenshot captions and step labels compact, usually `10-12 pt` with `1.0-1.2x` line spacing.
- Remove unused screenshot placeholders entirely.
- Keep screenshots, arrows, and annotation boxes off the bottom-right logo itself. If the screenshot must be large, crop the meaningful area instead of covering the logo.

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

Rules:

- Prefer a restrained blue-gray sequence, a compact table, or a light line flow.
- Use simple numbered text labels or small blue tags instead of large multicolor circular badges.
- Do not use rainbow step cards, alternating colored vertical bars, or heavy shadow cards unless each color carries a documented business meaning.
- Keep the final step, callout, or summary from overlapping the bottom-right logo.

## Mapping Heuristics

- Decide the full slide sequence before editing individual slide content.
- If the content is a new chapter, use Section Divider.
- If the content is a UI operation workflow, use Screenshot Step Page.
- If the content is a process or algorithm workflow without screenshots, use Process / Workflow Summary Page.
- If the content is a side-by-side decision, use Comparison Table or Choice/Recommendation.
- If the content is an exception or support answer, use Problem/Solution.
- If no strong pattern fits, use Text Explanation Page.
- Remove surplus placeholders, screenshot boxes, arrows, and table rows entirely; do not just clear their text.
- Before finalizing a slide, make sure the bottom-right logo remains uncovered; do not reserve a large empty area above or left of it.
