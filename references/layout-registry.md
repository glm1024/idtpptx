# Layout Registry

This is the controlled layout registry for `idtpptx`.

Use this file when choosing among multiple company-style layout recipes. The
goal is to make layout choice deterministic across models and agents: select by
content shape, scenario, and slot requirements, not by visual taste, random
choice, or whole-slide cloning.

`references/layout-map.md` defines broad page types. This registry defines
specific reusable recipes under those page types. For the component inventory
and combination rules behind these recipes, read
`references/component-system.md` and `references/composition-grammar.md`.

## Registry Rules

- Every reusable layout recipe needs an ID before it becomes a template asset.
- Do not add raw reference slides to `assets/templates/` just because they look
  useful. First register the reusable structure here.
- Do not choose randomly. If more than one layout can work, use the priority
  order and scenario fit in this file.
- Do not default to cloning the cleaned V1 sample slide. A cleaned sample is one
  valid specimen and a fallback, not the normal generation unit.
- Compose final pages from registered components whenever the content shape
  differs from the sample.
- Do not create a one-off layout inside a deliverable deck unless no registered
  layout fits. If the one-off layout proves reusable, register it after the deck
  is reviewed.
- Keep the fixed `IDT/Inspur Pragmatic` theme. Layout variants may change
  structure and density, not the core color/font system.
- Each variant must state its slots, text limits, "do not use" cases, and QA
  risks before being promoted to a cleaned V1 template specimen.

## Recipe Vs Specimen

Each layout ID is a recipe:

- page intent;
- component families;
- material slots;
- text limits;
- density boundaries;
- QA risks.

The V1 template may contain a cleaned sample slide for a recipe, such as
`TBL-03A` or `ARC-02A`. That sample is a specimen. Use it for calibration,
fallback editing, and regression checks. Do not generate a full deck by copying
the specimen sequence unless the user's content truly has the same sequence and
material shape.

## Slide Planning Contract

For non-trivial decks, draft a planning table before editing slide content:

| Page | Layout ID | Page type | Components | Why this recipe | Material shape | Risk |
|---|---|---|---|---|---|---|
| 1 | `COV-01` | Cover | title, subtitle, metadata | Standard internal report cover | title + date | Low |
| 2 | `DIR-01` | Section / directory | progress rows | Long training deck needs progress map | 4 chapters | Low |
| 3 | `SS-02` | Screenshot Step | screenshot slots, arrows, captions | Two UI states with arrow | 2 screenshots | Medium |

The planning table is a working artifact. Do not insert it into the final deck
unless the user explicitly asks for a deck-production appendix.

If the draft plan maps most pages directly to the V1 sample sequence, pause and
re-plan. The deck should be content-driven, not a template tour.

## Selection Priority

Use the first matching branch:

1. Cover or closing page -> `COV-*` / `SUM-*`.
   - Use `SUM-02` when the closing slide needs decision, owner, date, and next
     action fields.
2. Chapter break or progress map -> `SEC-*` / `DIR-*`.
3. UI operation evidence -> `SS-*`.
   - Use `SS-03` when troubleshooting or FAQ content requires screenshot
     evidence to explain the symptom or fix.
4. Dense comparison, responsibility, protocol, metric, or decision table ->
   `TBL-*`.
5. Technical architecture, non-UI workflow, topology, or data path -> `ARC-*`
   or `PRC-*`.
   - Use `PRC-03` when the content is a phased roadmap, rollout path, or
     leadership update timeline.
   - Use `ARC-01` when explanation and diagram share the page.
   - Use `ARC-03` when a diagram and narrative explanation need a stable
     two-column split and either side may lead the reading order.
   - Use `ARC-02` when the diagram is the primary evidence and needs full
     width to keep labels readable.
6. Problem diagnosis or exception handling -> `PRB-*`.
7. Option selection or recommendation -> `CHO-*`.
8. Plain context, scope, principle, or explanation -> `TXT-*`.

If content matches several branches, prefer the one with the most concrete
material slot. Example: a process with real UI screenshots should use `SS-*`,
not `PRC-*`.

## Registered Variants

### `COV-01` Standard Corporate Cover

Page type: Cover

Status: registered fallback; no cleaned V1 sample yet

Best for:

- Internal report title.
- Training/manual title.
- Review deck title with department/date/version.

Slots:

- Main title: 1-2 lines.
- Optional subtitle/objective: 1 short line.
- Metadata: department, date, version, presenter, as needed.
- Logo: provided by template, bottom-right or cover-specific placement.

Text limits:

- Main title: prefer <= 24 Chinese characters; split subtitle if longer.
- Metadata/objective: <= 1 line each.

Do not use for:

- A long background paragraph.
- Multi-item scope notes.
- Marketing hero visuals or generated AI illustration covers.

QA:

- Delete stale PowerPoint title/subtitle placeholders.
- Do not add white cards, diagonal strips, or empty metadata panels.
- Keep one visible logo system.

### `COV-02` Formal Review Cover

Page type: Cover

Status: registered variant; cleaned V1 template sample exists as `COV-02A`

Source inspiration:

- `裸金属图形化控制台v1.0.pptx`
- `跨云迁移分享.pptx`
- `云智能助手架构和功能设计方案1015_副本.pptx`
- `智能编码专项 - V2.2.pptx`

Best for:

- Leadership review decks.
- Technical方案评审 or architecture review.
- Formal internal reports where the title needs more presence than `COV-01`.

Slots:

- Main title in the center gray band.
- Optional subtitle/objective under the title.
- Department/team, date, version, or confidentiality label in the lower-left.
- Logo provided by the template, bottom-right.

Text limits:

- Main title: prefer one line; allow two balanced lines only when the title is
  genuinely long.
- Subtitle/objective: one short line.
- Metadata: 2-3 short rows, no paragraph.

Do not use for:

- Long purpose/scope explanations; move them to slide 2.
- Marketing hero covers, generated illustrations, or dark tech openers.
- A cover that needs multiple logos or customer/project imagery.

QA:

- Keep all metadata inside the gray band and away from the gray/white boundary.
- Do not add a white metadata card, diagonal white strip, or extra logo.
- Title font should match the title zone: usually `28-34 pt`, not an oversized
  default PowerPoint placeholder.
- Delete or replace the original template subtitle placeholder; final cover
  must not show `项目名称 / 汇报主题`.

### `SEC-01` Simple Section Divider

Page type: Section Divider

Status: registered fallback; no cleaned V1 sample yet

Best for:

- Major chapter break.
- Training module divider.
- Long deck rhythm reset.

Slots:

- Section number or short label.
- Section title.

Text limits:

- Section title: one line preferred; two short lines allowed only if balanced.

Do not use for:

- Content-heavy explanation.
- A deck-production planning page.

QA:

- Remove inherited top-left title placeholders.
- Do not keep both a center divider title and a normal slide title.

### `DIR-01` Numbered Directory / Progress Map

Page type: Section Divider / Text Explanation Page

Status: registered variant; cleaned V1 template sample exists as `DIR-01A`

Source inspiration:

- `反向代理访问虚拟机控制台.pptx`
- `跨云迁移分享.pptx`
- `裸金属图形化控制台v1.0.pptx`

Best for:

- Training decks with 3-6 chapters.
- Solution decks that revisit progress before each chapter.
- Long operation manuals where the reader needs orientation.

Slots:

- 3-6 numbered chapter rows.
- Optional current-chapter highlight.
- Optional short chapter note.

Text limits:

- Chapter label: <= 14 Chinese characters.
- Optional note: <= 18 Chinese characters.

Do not use for:

- One-page agenda with only two trivial items.
- Detailed work plan or task checklist.

QA:

- Highlight color must be semantic and restrained. Default to brand blue; use
  amber/orange only for current-step emphasis when the meaning is documented.
- Do not turn directory rows into decorative marketing cards.

### `TXT-01` Standard Explanation Page

Page type: Text Explanation Page

Status: registered fallback; no cleaned V1 sample yet

Best for:

- Background, scope, principle, definition, or concise context.
- Sparse content that needs readable internal-report wording.

Slots:

- Slide title.
- 1-3 grouped text blocks or short bullet-like paragraphs.
- Optional note/callout bar.

Text limits:

- Main body: 80-180 Chinese characters preferred.
- If body exceeds roughly 220 Chinese characters, split the slide or switch to
  a table/structured layout.

Do not use for:

- Dense metric comparison.
- UI step walkthrough.
- Technical topology that needs a diagram slot.

QA:

- Use black or near-black body text.
- Keep line spacing at `1.3-1.45x`, or `1.5-1.7x` for sparse pages.

### `TBL-01` Compact Comparison Table

Page type: Comparison Table Page

Status: registered fallback; no cleaned V1 sample yet

Best for:

- 3-5 column comparison with short categorical cells.
- Responsibility matrix.
- Simple feature or option comparison.

Slots:

- Slide title.
- Table header.
- 3-7 rows.
- Optional one-line conclusion below or above the table.

Text limits:

- Header labels: <= 8 Chinese characters preferred.
- Body cells: short phrases; avoid paragraph cells.

Do not use for:

- Long evidence paragraphs.
- API/protocol route details.
- More than 7 rows unless the slide is explicitly an appendix.

QA:

- Use one horizontal alignment mode across the whole table.
- Vertically middle-align cells by default.
- Keep body font usually `12-13 pt`.

### `TBL-02` Dense Evidence / Protocol Table

Page type: Comparison Table Page

Status: registered variant; cleaned V1 template sample exists as `TBL-02A`

Source inspiration:

- `云智能助手架构和功能设计方案1015_副本.pptx`
- `跨资源池调度方案设计v1.0-孔维亭.pptx`
- `ICOS v5资源池管理方案2.pptx`

Best for:

- Technical protocol comparison.
- API route / capability / constraint table.
- Evidence table for方案评审.
- Metric table in leadership review material.

Slots:

- Slide title.
- Optional one-line framing sentence.
- Dense table, usually 4-6 columns.
- Optional footnote or conclusion sentence.

Text limits:

- Prefer 4-6 columns and 4-8 rows.
- Body font may use `10.5-11.5 pt` only when the table remains readable.
- Paragraph-like cells should be left-aligned and vertically top only when
  three or more wrapped lines are unavoidable.

Do not use for:

- Screenshots or UI walkthroughs.
- Narrative explanation that can be split into cards or text blocks.

QA:

- Check table does not become a mini spreadsheet pasted into the slide.
- Split by category if the content needs tiny text.
- Keep theme colors and cell fills within `references/theme-contract.md`.

### `TBL-03` Metric / Evaluation Table

Page type: Comparison Table Page

Status: registered variant; cleaned V1 template sample exists as `TBL-03A`

Source inspiration:

- `智能助手-资源-26年技术规划研讨-0.1_副本.pptx`
- `跨资源池调度方案设计v1.0-孔维亭.pptx`
- `附件2：持续改进优秀案例及优秀复制推广案例评选模板.pptx`

Best for:

- Review criteria and acceptance framing.
- Metric definitions for leadership or technical review.
- Current state / target / evidence / owner style evaluation pages.
- Scoring or priority matrices when each row is a metric or condition.

Slots:

- Slide title.
- Optional one-line framing sentence.
- Metric/evaluation table, usually 4-5 columns.
- Optional conclusion or action note below the table.

Recommended columns:

- `指标` / `判断内容` / `通过标准` / `业务含义`.
- Or `维度` / `当前判断` / `目标要求` / `下一步`.

Text limits:

- Prefer 4 columns and 4-6 rows.
- Header labels: <= 8 Chinese characters.
- Body cells: one line preferred; two wrapped lines allowed.
- Body font: usually `12-13 pt`; do not go below `11 pt` unless the page is
  explicitly a dense appendix.

Alignment:

- Use one horizontal alignment mode for the whole table.
- Use all-left mode when cells contain sentence-like explanations.
- Use all-center mode only when nearly every body cell is a short label, status,
  score, owner, or date.
- Vertically middle-align cells by default.

Do not use for:

- Protocol/API route tables that need many technical columns; use `TBL-02`.
- Work plans with many owners and dates; use future `TBL-04`.
- Screenshot evidence or UI steps.
- Large source-data tables that need appendix treatment.

QA:

- The table should look like a slide-native evaluation table, not a spreadsheet
  pasted into a large blank area.
- Header, body, and conclusion must use the same theme colors and font family.
- Row heights should be driven by readable text, not by stretching the table to
  fill empty space.
- If a row requires paragraph text, split the row, shorten wording, or move the
  detail into an appendix.
- Keep the conclusion note outside the table and away from the bottom-right
  logo.

### `SS-01` Single Screenshot With Explanation

Page type: Screenshot Step Page

Status: registered fallback; no cleaned V1 sample yet

Best for:

- One UI screen plus a concise explanation.
- A before/after state where one screenshot is enough.
- Product evidence page in a training deck.

Slots:

- Slide title.
- One screenshot slot, usually 16:9 or 16:10.
- 1-3 short explanation bullets or labels.

Text limits:

- Caption: 10-18 Chinese characters.
- Explanation: 1-3 lines.

Do not use for:

- Multi-step walkthrough with multiple screenshots.
- Very long screenshots that cannot remain readable.

QA:

- Preserve screenshot fidelity.
- Crop to meaningful area rather than shrinking unreadably.

### `SS-02` Two / Three Screenshot Step Sequence

Page type: Screenshot Step Page

Status: registered variant; cleaned V1 template sample exists as `SS-02A`

Source inspiration:

- `新邮箱系统使用培训-数据备份手册.pptx`
- `云智能助手架构和功能设计方案1015_副本.pptx`

Best for:

- Operation manual pages.
- Login/configuration/import/export workflows.
- Before -> after UI proof.
- 2-3 adjacent UI states connected by arrows.

Slots:

- Slide title.
- Optional one-line instruction above screenshots.
- Two or three screenshot slots with the same ratio.
- Red arrow, red box, or numbered connector between screenshots.
- Compact captions under or above each screenshot.

Recommended slot ratios:

- 2 screenshots: 16:10 or 4:3.
- 3 screenshots: 4:3 or cropped 16:10, depending on readable content.
- Long screenshot: crop into meaningful panels instead of using original long
  ratio.

Text limits:

- Instruction line: <= 40 Chinese characters.
- Each caption: <= 18 Chinese characters.
- Avoid paragraph text inside the screenshot row.
- If a step needs a paragraph, split the slide or move the explanation to a
  note/callout row below the screenshots.

Do not use for:

- Abstract process explanation without UI evidence.
- Screenshots that require zooming to be understood.
- Generated conceptual UI illustrations.

QA:

- All screenshots in the same group use consistent ratio and height.
- Screenshot group must be built from fixed slots, not manually scattered
  image boxes.
- Captions must sit in their own inner text boxes and must not overlap arrows,
  screenshot borders, or adjacent screenshots.
- Do not let arrows, annotations, or screenshots cover the bottom-right logo.
- If a screenshot contains sensitive data, redact before insertion.
- Follow `references/screenshot-framing.md`; do not redraw evidence screenshots
  unless the user asks for screenshot redesign.
- If the screenshots are not readable at slide size, crop the meaningful area
  or split into multiple `SS-01` / `SS-02` slides instead of shrinking further.

### `SS-03` Troubleshooting Screenshot

Page type: Screenshot Step Page / Problem/Solution Page

Status: registered variant; cleaned V1 template sample exists as `SS-03A`

Source inspiration:

- `新邮箱系统使用培训-数据备份手册.pptx`
- `云智能助手架构和功能设计方案1015_副本.pptx`

Best for:

- FAQ or troubleshooting pages where a screenshot proves the symptom.
- Operation manual exception handling.
- Support handoff pages that need to show what the user sees and what to do.

Slots:

- Slide title.
- One-line context or diagnosis guide.
- One large screenshot/evidence slot.
- Three diagnosis blocks: `现象`, `判断`, `处理`.
- Optional bottom note for boundary, risk, or next action.

Text limits:

- Context line: <= 36 Chinese characters.
- Screenshot caption: <= 18 Chinese characters.
- Each diagnosis block title: 2-4 Chinese characters.
- Each diagnosis block body: 1-2 short lines, each <= 20 Chinese characters.
- Bottom note: one short sentence.

Do not use for:

- Pure FAQ text with no visual evidence; use `PRB-01`.
- Multi-step operation walkthrough; use `SS-02`.
- Dense root-cause taxonomy; use a table or split pages.
- Full-screen screenshots whose text is unreadable at the chosen size.

QA:

- The screenshot must be the largest evidence object and remain readable after
  rendering.
- Red annotation boxes should point to one or two important areas only; do not
  cover the screenshot text.
- The diagnosis blocks must use fixed inner text zones. Body text must not
  spill outside the block or collide with the block title.
- The right diagnosis column and bottom note must not overlap the logo.
- If the screenshot needs more than two annotations or the diagnosis needs more
  than three blocks, split the page.

### `PRC-01` Horizontal Process Summary

Page type: Process / Workflow Summary Page

Status: registered fallback; no cleaned V1 sample yet

Best for:

- 4-6 non-UI process steps.
- Attribution, review, approval, or data-flow summary.
- Algorithm phases without screenshots.

Slots:

- Slide title.
- 4-6 step cards or a compact step table.
- Optional boundary/value note.

Text limits:

- Step title: <= 8 Chinese characters or accepted technical term.
- Step body: <= 24 Chinese characters; split if longer.

Do not use for:

- UI operation pages.
- Dense technical topology.
- Decorative pseudo-process.

QA:

- Title and body zones inside each card must not overlap.
- Card body text must stay inside each visible frame.
- Use Chinese-first process labels.

### `PRC-03` Roadmap / Rollout Path

Page type: Process / Workflow Summary Page

Status: registered variant; cleaned V1 template sample exists as `PRC-03A`

Source inspiration:

- `跨云迁移分享.pptx`
- `裸金属图形化控制台v1.0.pptx`
- `智能编码专项 - V2.2.pptx`

Best for:

- Project roadmap.
- Rollout plan.
- Month-by-month or phase-by-phase implementation path.
- Leadership update pages that need to show sequence, deliverables, and risks.

Slots:

- Slide title.
- One-line framing sentence.
- 3-5 phase blocks on a horizontal timeline.
- Each phase has a short phase label, milestone title, and 1-2 outcome lines.
- Optional bottom note for dependency, risk, or next action.

Text limits:

- Phase label: <= 8 Chinese characters or short date/phase marker.
- Milestone title: <= 10 Chinese characters.
- Outcome lines: 1-2 short lines, each <= 18 Chinese characters.
- Bottom note: one short sentence.

Do not use for:

- UI operation steps; use `SS-*`.
- Architecture/data-chain diagrams; use `ARC-*`.
- Dense acceptance criteria or responsibility matrices; use `TBL-*`.
- Decorative roadmaps with arbitrary icons, gradients, or many colors.

QA:

- Timeline blocks must use identical width and aligned baselines.
- Use one horizontal reading order from left to right.
- Keep body text inside each phase block's inner area; do not let text spill
  into adjacent phases.
- Use brand blue for the active path and light gray for neutral phase panels.
  Use red/amber/green only for explicit risk/status meaning.
- If a phase requires more than two outcome lines, split the page or switch to a
  table instead of shrinking below readable size.

### `ARC-01` Technical Architecture / Flow Explanation

Page type: Process / Workflow Summary Page

Status: registered variant; cleaned V1 template sample exists as `ARC-01A`

Source inspiration:

- `跨资源池调度方案设计v1.0-孔维亭.pptx`
- `反向代理访问虚拟机控制台.pptx`
- `跨云迁移分享.pptx`
- `InCloudOS SDN网络技术分享.pptx`

Best for:

- Technical topology, architecture, or data path.
- Left explanation + right diagram.
- Simple or moderately complex diagrams that still remain readable in a
  two-column structure.
- Architecture pages where the explanation and diagram have similar importance.

Slots:

- Slide title.
- Left explanation area, usually 30-35% of the content width.
- Right architecture diagram slot, usually 60-65% of the content width.
- Optional short bottom note if the diagram needs one boundary statement.
- Optional legend or boundary note.

Text limits:

- Notes: 3-5 short bullets or one concise paragraph.
- Diagram labels should be readable; avoid tiny labels inside copied diagrams.
- If the explanation needs more than 5 bullets, switch to a table or split the
  topic.

Do not use for:

- UI screenshot walkthrough.
- A table that is fundamentally rows/columns.
- Decorative pipeline art with no operational meaning.
- Wide topology diagrams that become unreadable in a right-side slot; use
  `ARC-02` instead.

QA:

- If using a source diagram, redraw or simplify only when needed; do not copy
  source-specific customer/project content into the skill.
- Keep diagrams in blue/black restrained theme unless semantic status colors
  are necessary.
- Do not make the diagram a small image floating in a large empty content zone.
- Keep the explanation block and diagram visually connected; avoid two
  unrelated islands.

### `ARC-03` Bidirectional Diagram / Narrative Split

Page type: Process / Workflow Summary Page

Status: registered variant; cleaned V1 template sample exists as `ARC-03A`

Source inspiration:

- `跨云迁移分享.pptx`, especially diagram-led feature and key-technology pages.
- `跨资源池调度方案设计v1.0-孔维亭.pptx`, especially scenario diagram plus
  explanation pages.
- `反向代理访问虚拟机控制台.pptx`, for topology pages that pair a scheme diagram
  with explanatory text.

Best for:

- Architecture, data path, deployment, resource scheduling, or platform
  capability pages where the diagram and explanation are both necessary.
- Diagram-left / text-right pages when the diagram is the reading entry or the
  main evidence.
- Text-left / diagram-right pages when the reader needs premise, boundary, or
  conclusion first, then the architecture visual.
- Simple or moderately complex diagrams that still remain readable in roughly
  55-62% of the content width.

Slots:

- Slide title.
- Optional one-line reading guide.
- Diagram zone, usually 55-62% of the content width.
- Narrative zone, usually 32-38% of the content width, with 3-4 explanation
  strips/cards.
- Optional bottom note only when it does not collide with the logo safe zone.

Orientation rules:

- `diagram-left`: use when the source material starts from a structure,
  topology, or data path and the text explains what the parts mean.
- `diagram-right`: use when the slide should first state the business premise,
  boundary, conclusion, or risk, and then show the supporting architecture.
- Reversing the visual orientation does not automatically reverse the semantic
  flow. Keep arrows and data direction faithful to the actual architecture.

Text limits:

- Reading guide: <= 36 Chinese characters.
- Narrative card title: 4-8 Chinese characters.
- Narrative card body: 1-2 short lines, <= 28 Chinese characters per card.
- Diagram node labels: <= 8 Chinese characters or accepted technical terms.

Do not use for:

- Wide, label-heavy architecture diagrams that need the full page; use
  `ARC-02`.
- Pure process steps with no system structure; use `PRC-*`.
- Screenshot walkthroughs; use `SS-*`.
- Dense criteria, protocol, or metric content that belongs in `TBL-*`.
- Decorative illustration where the diagram carries no operational meaning.

QA:

- Both zones must look intentional and balanced; neither side should become a
  tiny pasted object beside a large blank panel.
- Text in narrative strips/cards must be inside each visible frame with padding
  and wrapping; no row-wide text box may cross into the diagram zone.
- Diagram labels must remain readable after rendering.
- Keep source-specific business labels, customer names, URLs, IPs, and project
  details out of the template specimen.
- Keep all editable elements in the fixed theme tokens unless a semantic
  red/green/amber status is explicitly required.

### `ARC-02` Full-Width Technical Diagram

Page type: Process / Workflow Summary Page

Status: registered variant; cleaned V1 template sample exists as `ARC-02A`

Source inspiration:

- `跨资源池调度方案设计v1.0-孔维亭.pptx`
- `反向代理访问虚拟机控制台.pptx`
- `跨云迁移分享.pptx`
- `InCloudOS SDN网络技术分享.pptx`
- `ICOS v5资源池管理方案2.pptx`

Best for:

- Architecture, topology, migration path, or data-chain diagrams where labels
  must remain readable.
- Diagrams that are the primary evidence on the slide.
- Wide diagrams that would become too small in `ARC-01`.
- Technical方案 pages where one short conclusion plus the diagram is clearer
  than multiple cards.

Slots:

- Slide title.
- Optional one-line conclusion or reading guide.
- Full-width diagram slot under the title area.
- Bottom note strip for 1-2 boundary/value statements.
- Optional small legend if colors or line styles carry meaning.

Text limits:

- Conclusion/reading guide: <= 36 Chinese characters.
- Bottom note strip: 1-2 lines, or 3 very short bullets.
- Diagram labels should remain readable after rendering; if not, split the
  diagram or enlarge the critical region.

Do not use for:

- Diagrams that can be explained better as a table.
- Pure process steps with no diagram evidence; use `PRC-01`.
- Screenshot walkthroughs; use `SS-*`.
- Source-specific diagrams copied from an internal/customer deck without
  cleaning.

QA:

- Give the diagram real page width. Do not paste it as a small centered image
  surrounded by empty white space.
- Keep the bottom note strip inside its visible frame with padding; text must
  wrap inside the strip and never overflow horizontally or vertically.
- Keep the diagram and note strip away from the bottom-right logo.
- Normalize editable diagram colors to the theme tokens unless a red/green/amber
  color has explicit semantic meaning.
- If a source diagram is used only as inspiration, recreate the structure with
  neutral labels and remove source-specific business content before it becomes
  a template asset.

### `PRB-01` Problem / Reason / Solution

Page type: Problem/Solution Page

Status: registered fallback; no cleaned V1 sample yet

Best for:

- FAQ page.
- Troubleshooting item.
- Known issue with reason and action.

Slots:

- Slide title.
- Problem, reason, solution blocks.
- Optional screenshot or evidence if needed.

Text limits:

- Each block: 1-3 lines.

Do not use for:

- Large root-cause taxonomy.
- Many unrelated issues on one slide.

QA:

- Keep a stable 问题 / 原因 / 解决 structure.
- Split if the diagnosis becomes cramped.

### `PRB-02` Background / Constraint / Scheme

Page type: Problem/Solution Page

Status: backlog candidate

Source inspiration:

- `反向代理访问虚拟机控制台.pptx`
- `裸金属图形化控制台v1.0.pptx`

Best for:

- Technical方案说明.
- 背景 / 约束 / 方案 / 风险.
- Architecture review where the issue needs context before the solution.

Slots:

- Slide title.
- 3-4 structured blocks.
- Optional diagram or table slot.

Text limits:

- Each block title: <= 8 Chinese characters.
- Each body: <= 2 short lines.

Do not use for:

- Pure operational screenshot steps.
- Long narrative background.

QA:

- Avoid turning it into four large cards with overflowing text.
- If the diagram/table is primary, consider `ARC-01` or `TBL-02` instead.

### `CHO-01` Recommendation / Option Choice

Page type: Choice/Recommendation Page

Status: registered fallback; no cleaned V1 sample yet

Best for:

- Recommended path vs fallback.
- Configuration choice.
- Two or three方案 options.

Slots:

- Slide title.
- 2-3 option blocks.
- Recommendation conclusion.

Text limits:

- Option title: <= 10 Chinese characters.
- Option body: <= 2 lines.
- Conclusion: one sentence.

Do not use for:

- Many options.
- Detailed scoring matrix; use `TBL-*` instead.

QA:

- Keep the recommendation visually clear but not marketing-like.
- Put conclusion text inside the conclusion frame, with padding.

### `SUM-01` Restrained Summary

Page type: Text Explanation Page / closing

Status: backlog candidate

Best for:

- Final recommendation.
- Review conclusion.
- Next steps.

Slots:

- Summary title.
- 3 concise takeaways or next actions.
- Optional owner/date line.

Text limits:

- Each takeaway: one line preferred.

Do not use for:

- Decorative "THANKS" pages.
- Motivational quote endings.

QA:

- Keep it business-facing.
- Do not add stock photos or generic closing art by default.

### `SUM-02` Decision Recap / Handoff

Page type: Text Explanation Page / closing

Status: registered variant; cleaned V1 template sample exists as `SUM-02A`

Source inspiration:

- `智能编码专项 - V2.2.pptx`
- Review-style pages in the local reference deck set.

Best for:

- Review handoff closing page.
- Decision recap after a technical方案评审.
- Final page that needs owner, date, and next action instead of a decorative
  thank-you slide.

Slots:

- Slide title.
- One-line conclusion strip.
- Three decision/next-action blocks.
- Compact owner/date/action table.
- Optional bottom note for unresolved assumptions or follow-up rhythm.

Text limits:

- Conclusion strip: one short sentence.
- Decision block title: <= 8 Chinese characters.
- Decision block body: 1-2 short lines, each <= 18 Chinese characters.
- Owner/date table: 3-4 rows, short phrases only.

Do not use for:

- Generic "谢谢" or contact slides.
- Dense project plans with many owners/dates; use a work-plan table.
- Detailed metric evidence; use `TBL-*`.

QA:

- The page must end with reader-facing decisions or actions, not deck-production
  process notes.
- Keep all block text inside visible frames with padding.
- Use one table alignment mode; this sample uses all-left because rows are
  action-like.
- Do not add stock photos, decorative hero graphics, or motivational quotes.
- Keep the owner/date table and note strip clear of the logo.

## Backlog Promotion Process

Use this process before a backlog candidate becomes a PPTX layout asset:

1. Confirm the layout solves a recurring content shape.
2. Write or refine the registry entry with slots, limits, and QA risks.
3. Produce a cleaned sample slide with no source business content. Use
   `references/cleaned-layout-sample-specs.md` when a spec exists for that
   layout ID.
4. Add that sample only to `assets/templates/inspur-pragmatic-template-v1.pptx`.
5. Render and inspect the sample.
6. Update `references/layout-map.md`, `references/qa-checklist.md`, or helper
   scripts if the new layout introduces new mechanical risks.

Do not promote a layout only because one reference slide looks good.
