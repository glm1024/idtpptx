# Cleaned Layout Sample Specs

Use this when converting registered layout recipes into cleaned sample slides
for the single official V1 template.

These specs are not source-deck copies and not final-slide cloning
instructions. They define reusable geometry, slot rules, placeholder text, and
QA expectations for the current `IDT/Inspur Pragmatic` template. A cleaned
sample slide is a specimen and fallback for a recipe; normal deck generation
should still start from content shape, `references/component-system.md`, and
`references/composition-grammar.md`.

## Scope

Current priority samples:

- `COV-02`: formal review cover.
- `DIR-01`: numbered directory / progress map.
- `PRC-03`: roadmap / rollout path.
- `SS-02`: two / three screenshot operation step sequence.
- `SS-03`: troubleshooting screenshot with diagnosis blocks.
- `ARC-01`: left explanation + right technical diagram.
- `ARC-02`: full-width technical diagram.
- `TBL-02`: dense evidence / protocol table.
- `TBL-03`: metric / evaluation table.
- `SUM-02`: decision recap / handoff closing page.

Do not add raw reference PPT pages to the skill. A sample slide can enter
`assets/templates/inspur-pragmatic-template-v1.pptx` only after it is rebuilt
with neutral placeholder content and passes visual QA. Adding a sample does not
mean agents should copy that slide by default; it means the recipe now has a
visual specimen for calibration and fallback editing.

## Shared Slide Geometry

Use the current V1 template size:

| Item | Value |
|---|---:|
| Slide width | `13.333 in` |
| Slide height | `7.500 in` |
| Normal title placeholder | `x=0.37, y=0.10, w=12.60, h=0.72` |
| Main content start | `y=1.15` |
| Preferred left content edge | `x=0.65-0.75` |
| Preferred right content edge | `x=12.55-12.75` |
| Preferred content bottom | `y<=6.70` |

Template chrome is provided by the master/layout:

- top title area;
- thin top divider line;
- top-right blue marker/page marker;
- bottom-right Inspur logo.

Do not redraw these elements inside the sample slide.

Logo note:

- The master logo sits at the bottom-right. Content can use the space above and
  left of it, but no text, screenshot, diagram, note strip, line, or shape may
  overlap the logo mark.
- If a full-width element reaches the lower part of the slide, keep its bottom
  at or above `y=6.70` unless a render proves the logo remains clear.

## Shared Visual Tokens

Use tokens from `references/theme-contract.md`:

| Use | Token |
|---|---|
| Background | `FFFFFF` |
| Placeholder fill | `F2F4F7` or `EDEDED` |
| Border / grid | `A4A3A4` |
| Brand accent | `0062AC` or `00518E` |
| Title / strong labels | `213261` |
| Body text | `000000` or `111111` |
| Screenshot annotation | `D93025`, `C00000`, or `FF4B4B` |

Font:

- Editable text: `微软雅黑` / `Microsoft YaHei`.
- Normal sample title: `28-30 pt` bold.
- Placeholder labels: `12-14 pt`.
- Screenshot captions: `10-12 pt`.
- Notes: `10-12 pt`, black or near-black.

## Placeholder Content Rules

Use neutral Chinese placeholder text that teaches the structure without
containing business facts.

Allowed examples:

- `操作步骤示例`
- `按入口、动作、结果组织截图，重点控件用红框标注。`
- `第一步：进入页面`
- `第二步：确认结果`
- `技术架构示例`
- `先看主链路，再看边界条件。`
- `入口层`
- `服务层`
- `数据层`
- `外部系统`
- `指标评估示例`
- `指标`
- `判断内容`
- `通过标准`
- `业务含义`
- `技术方案评审材料`
- `正式评审封面示例`
- `汇报部门：业务技术团队`
- `阶段推进示例`
- `调研确认`
- `试点验证`
- `推广落地`
- `故障排查示例`
- `现象`
- `判断`
- `处理`
- `决策复盘示例`
- `结论`
- `负责人`
- `时间`
- `下一步`

Do not use:

- source deck screenshots;
- source product names, URLs, contacts, customers, project names, or real data;
- deck-production notes such as `本页后续补截图` or `先占位`;
- PowerPoint default prompts such as `单击此处添加标题`;
- English-only labels unless they are genuine technical terms.

## `COV-02A` Formal Review Cover

Use when a deck is a leadership review, technical方案评审, architecture review,
or formal internal report.

This sample uses the V1 template's cover master/layout. It should not redraw
the cover chrome.

Recommended geometry:

| Element | x | y | w | h | Notes |
|---|---:|---:|---:|---:|---|
| Main title | `2.30` | `2.88` | `8.70` | `0.70` | Centered in gray band |
| Subtitle/objective | `2.55` | `3.62` | `8.20` | `0.36` | One short line |
| Department/team | `0.95` | `4.95` | `4.40` | `0.34` | Lower-left, inside gray band |
| Date/version | `0.95` | `5.32` | `4.40` | `0.34` | Lower-left, inside gray band |

Sample text:

- Title: `技术方案评审材料`
- Subtitle: `背景、结论与后续安排`
- Department: `汇报部门：业务技术团队`
- Date/version: `日期：2026 年 5 月`

Text limits:

- Main title: one line preferred; two balanced lines allowed when necessary.
- Subtitle/objective: <= 22 Chinese characters.
- Metadata: 2-3 short rows.

QA:

- The title must not inherit the original PowerPoint placeholder size or color.
- The title should sit comfortably in the gray band and must not overlap any
  stale template prompt.
- Metadata must stay above the gray/white boundary; do not let date text touch
  or cross into the white logo area.
- Do not add white cards, diagonal strips, generated illustrations, or a second
  logo.
- If the user wants a longer purpose statement, move it to slide 2 instead of
  expanding the cover.

## `DIR-01A` Numbered Directory / Progress Map

Use when a training deck, solution walkthrough, or long technical report needs
to orient the reader before a chapter starts.

Recommended geometry:

| Element | x | y | w | h | Notes |
|---|---:|---:|---:|---:|---|
| Title | `0.37` | `0.10` | `12.60` | `0.72` | Use the real title placeholder |
| Framing sentence | `0.70` | `1.12` | `11.95` | `0.36` | One short orientation sentence |
| Directory rows | `2.30` | `1.82` | `8.75` | `0.56` each | 3-6 rows, one active row |
| Number badge | row x | row y | `0.56` | row height | Same color as active row |
| Bottom note strip | `0.70` | `5.95` | `11.95` | `0.58` | Optional use rule |

Sample text:

- Title: `目录进度示例`
- Framing sentence: `长培训或方案说明先给读者定位当前位置。`
- Rows:
  - `1` / `背景和目标` / `先说明为什么要做`
  - `2` / `方案设计` / `本页高亮当前章节`
  - `3` / `实施路径` / `再说明怎么推进`
  - `4` / `验证结果` / `最后沉淀结论和动作`
- Note: `使用：超过 12 页或跨多个章节时，用目录页承接阅读节奏。`

Text limits:

- Chapter title: <= 10 Chinese characters.
- Row note: <= 18 Chinese characters.
- Use 3-6 rows. If a deck has more chapters, group them into phases or split
  the directory.

QA:

- Highlight exactly one current chapter unless the slide is a full agenda.
- Use brand blue for the active row; do not use multiple decorative colors.
- Keep row labels vertically centered and aligned.
- Do not let directory rows become marketing cards or dense work-plan rows.

## `PRC-03A` Roadmap / Rollout Path

Use when a project, rollout, or leadership update needs a clear sequence of
phases and deliverables.

Recommended geometry:

| Element | x | y | w | h | Notes |
|---|---:|---:|---:|---:|---|
| Title | `0.37` | `0.10` | `12.60` | `0.72` | Use the real title placeholder |
| Framing sentence | `0.70` | `1.12` | `11.95` | `0.36` | One short conclusion |
| Timeline axis | `1.05` | `2.58` | `11.10` | `0.08` | Brand blue |
| Phase blocks | `0.90` | `1.85` | `2.55` each | `2.70` | 4 equal blocks |
| Phase marker | centered | `2.38` | `0.24` | `0.24` | Small blue dot, no text |
| Bottom note strip | `0.70` | `5.72` | `11.95` | `0.62` | Optional dependency or next action |

Sample text:

- Title: `阶段推进示例`
- Framing sentence: `先试点验证，再按范围逐步推广。`
- Phases:
  - `阶段一` / `调研确认` / `明确对象、口径和边界`
  - `阶段二` / `试点验证` / `选择代表场景做闭环`
  - `阶段三` / `推广落地` / `扩展到主要团队和项目`
  - `阶段四` / `持续优化` / `按数据反馈迭代规则`
- Note: `依赖：每阶段结束后先确认口径，再进入下一阶段。`

Text limits:

- Phase label: <= 8 Chinese characters.
- Phase title: <= 10 Chinese characters.
- Phase body: 1-2 lines, each <= 18 Chinese characters.
- Bottom note: one short sentence.

QA:

- All phase blocks use identical width and height.
- Phase text uses separate label/title/body zones; no title-body overlap.
- Body text must stay inside its visible phase panel.
- Timeline markers align on one baseline and do not contain text.
- Do not use multicolor decorative status dots. Non-blue colors need explicit
  status meaning.
- If there are more than five phases, split the roadmap or use an appendix
  table.

## `SS-02A` Two Screenshot Sequence

Use when two UI states need side-by-side comparison or a two-step operation.

Recommended geometry:

| Element | x | y | w | h | Notes |
|---|---:|---:|---:|---:|---|
| Title | `0.37` | `0.10` | `12.60` | `0.72` | Use the real title placeholder |
| Instruction line | `0.70` | `1.12` | `11.95` | `0.36` | One short sentence |
| Screenshot 1 frame | `0.70` | `1.72` | `5.45` | `3.40` | 16:10-ish slot |
| Screenshot 2 frame | `7.20` | `1.72` | `5.45` | `3.40` | Same ratio and height |
| Connector arrow | `6.34` | `3.10` | `0.60` | `0.30` | Red, centered between frames |
| Caption 1 | `0.70` | `5.22` | `5.45` | `0.36` | Inside caption box |
| Caption 2 | `7.20` | `5.22` | `5.45` | `0.36` | Same style |
| Note strip | `0.70` | `5.95` | `11.95` | `0.58` | Optional, 1-2 lines |

Text limits:

- Instruction line: `<=40` Chinese characters.
- Captions: `<=18` Chinese characters each.
- Note strip: one short sentence or two short bullets.

Sample text:

- Title: `操作步骤示例`
- Instruction: `按入口、动作、结果组织截图，重点控件用红框标注。`
- Caption 1: `第一步：进入页面`
- Caption 2: `第二步：确认结果`
- Note: `说明：真实截图交付前需脱敏，截图文字必须可读。`

QA:

- Both screenshot frames must use identical size.
- Caption text boxes must stay inside their own caption zones.
- Red arrows/boxes must not cover important screenshot text or cleaned-sample
  placeholder labels. If the annotation sits inside a gray screenshot slot,
  keep the placeholder label in a separate inner text zone away from the
  annotation.
- If either screenshot is unreadable at this size, crop the meaningful region or
  split into two `SS-01` slides.

## `SS-02B` Three Screenshot Sequence

Use when a simple operation needs three adjacent UI states.

Recommended geometry:

| Element | x | y | w | h | Notes |
|---|---:|---:|---:|---:|---|
| Title | `0.37` | `0.10` | `12.60` | `0.72` | Use the real title placeholder |
| Instruction line | `0.70` | `1.12` | `11.95` | `0.36` | One short sentence |
| Screenshot 1 frame | `0.70` | `1.72` | `3.55` | `2.66` | 4:3 slot |
| Screenshot 2 frame | `4.90` | `1.72` | `3.55` | `2.66` | Same ratio |
| Screenshot 3 frame | `9.10` | `1.72` | `3.55` | `2.66` | Same ratio |
| Connector arrows | between frames | `2.88` | `0.42` | `0.24` | Red, small |
| Captions | same x as frames | `4.55` | frame width | `0.42` | 10-12 pt |
| Bottom explanation | `0.70` | `5.35` | `11.95` | `0.75` | Optional, 1-2 short lines |

Use this only when all three screenshots remain readable. Otherwise use two
slides, or use a 2+1 split in a future variant after it has its own geometry.

## `SS-03A` Troubleshooting Screenshot

Use when a troubleshooting or FAQ page needs one visual evidence screenshot and
short diagnosis blocks.

Recommended geometry:

| Element | x | y | w | h | Notes |
|---|---:|---:|---:|---:|---|
| Title | `0.37` | `0.10` | `12.60` | `0.72` | Use the real title placeholder |
| Context line | `0.70` | `1.12` | `11.95` | `0.36` | One short diagnosis guide |
| Screenshot frame | `0.70` | `1.72` | `7.25` | `3.95` | Primary evidence slot |
| Diagnosis column | `8.35` | `1.72` | `4.30` | `3.95` | Three stacked blocks |
| Bottom note strip | `0.70` | `5.95` | `11.95` | `0.58` | Boundary or next action |

Diagnosis block geometry:

| Element | x | y | w | h | Notes |
|---|---:|---:|---:|---:|---|
| Block 1 | `8.35` | `1.72` | `4.30` | `1.15` | `现象` |
| Block 2 | `8.35` | `3.12` | `4.30` | `1.15` | `判断` |
| Block 3 | `8.35` | `4.52` | `4.30` | `1.15` | `处理` |

Sample text:

- Title: `故障排查示例`
- Context: `先定位异常提示，再说明判断依据和处理动作。`
- Screenshot label: `异常提示区域`
- Diagnosis:
  - `现象` / `页面提示保存失败`
  - `判断` / `先确认配置和权限`
  - `处理` / `修正后重新提交`
- Note: `边界：本页只说明单个异常，复杂问题拆成多页排查。`

Text limits:

- Context line: <= 36 Chinese characters.
- Diagnosis body: 1-2 lines, each <= 20 Chinese characters.
- Note: one short sentence.

QA:

- Screenshot frame is the largest object; if its text is unreadable, crop the
  meaningful region or use an appendix screenshot page.
- Red annotation box must not cover important screenshot text.
- Each diagnosis block has an inner text area; no body text can spill outside
  the block background.
- Keep the right column and bottom note away from the logo.
- Use `PRB-01` instead when no screenshot evidence is needed.

## `ARC-01A` Left Explanation + Right Technical Diagram

Use when the explanation and the technical diagram have similar importance and
the diagram remains readable in a right-side slot.

Recommended geometry:

| Element | x | y | w | h | Notes |
|---|---:|---:|---:|---:|---|
| Title | `0.37` | `0.10` | `12.60` | `0.72` | Use the real title placeholder |
| Reading guide | `0.70` | `1.12` | `11.95` | `0.36` | One short conclusion |
| Explanation panel | `0.70` | `1.65` | `3.45` | `4.42` | 30-35% content width |
| Diagram panel | `4.55` | `1.65` | `8.10` | `4.42` | 60-65% content width |
| Bottom note strip | `0.70` | `6.24` | `11.95` | `0.36` | Optional fit rule |

Sample text:

- Title: `架构说明示例`
- Reading guide: `左侧先给阅读口径，右侧展示主链路。`
- Explanation title: `阅读口径`
- Explanation lines:
  - `明确对象边界`
  - `确认主链路方向`
  - `标出异常入口`
  - `写清交付结论`
- Diagram labels: `用户入口` / `服务网关` / `核心服务` / `数据存储`
- Note: `适用：说明文字和架构图同等重要；图特别宽时改用 ARC-02。`

Text limits:

- Explanation panel: 3-5 short lines.
- Diagram labels: <= 8 Chinese characters or accepted technical terms.
- Bottom note: one short sentence.

QA:

- The left panel and right diagram must be visually connected and aligned.
- Do not shrink a wide architecture diagram into this layout; use `ARC-02`
  when labels become hard to read.
- Keep source-specific diagrams out of the sample. Use neutral editable blocks.
- Use red only for boundaries, warnings, or important annotations.

## `ARC-02A` Full-Width Technical Diagram

Use when the diagram is the primary evidence and labels must remain readable.

Recommended geometry:

| Element | x | y | w | h | Notes |
|---|---:|---:|---:|---:|---|
| Title | `0.37` | `0.10` | `12.60` | `0.72` | Use the real title placeholder |
| Reading guide | `0.70` | `1.12` | `11.95` | `0.36` | One short conclusion |
| Diagram frame | `0.70` | `1.62` | `11.95` | `4.25` | Primary slot |
| Bottom note strip | `0.70` | `6.05` | `11.95` | `0.55` | 1-2 lines |

Sample text:

- Title: `技术架构示例`
- Reading guide: `先看主链路，再看边界条件。`
- Diagram labels: `入口层` / `服务层` / `数据层` / `外部系统`
- Note: `边界：本页只展示主要链路，不展开异常分支。`

Diagram placeholder guidance:

- Build the sample diagram from simple editable rectangles and connector lines.
- Use brand blue for major blocks, light gray for neutral groups, and red only
  for a risk or boundary annotation.
- Keep labels short and Chinese-first.
- Do not paste a raster image from a source deck into the sample.

QA:

- Diagram labels must remain readable after rendering.
- The diagram must occupy real page width; it should not look like a small image
  floating in white space.
- The bottom note strip must use an inner text box with padding. Text must wrap
  inside the strip and cannot extend beyond the visible fill.
- If the diagram needs more than one bottom note sentence, split the slide or
  move details to an appendix.

## `TBL-02A` Dense Evidence / Protocol Table

Use when a technical方案, protocol review, capability comparison, or evidence
review needs a dense but still slide-readable table.

Recommended geometry:

| Element | x | y | w | h | Notes |
|---|---:|---:|---:|---:|---|
| Title | `0.37` | `0.10` | `12.60` | `0.72` | Use the real title placeholder |
| Framing sentence | `0.70` | `1.12` | `11.95` | `0.36` | One short conclusion |
| Table | `0.70` | `1.72` | `11.95` | `3.38` | 6 columns, 4-6 body rows |
| Bottom note strip | `0.70` | `5.55` | `11.95` | `0.72` | Split-table rule |

Recommended column widths:

| Column | Width | Notes |
|---|---:|---|
| `类别` | `1.05 in` | Short grouping |
| `对象` | `1.50 in` | Object or module |
| `口径` | `2.05 in` | Measurement / matching rule |
| `证据` | `2.55 in` | Proof or source |
| `约束` | `2.20 in` | Boundary or risk |
| `结论` | `2.60 in` | Business-facing output |

Sample text:

- Title: `证据表说明示例`
- Framing sentence: `密集表格先统一口径，再压缩到可读范围。`
- Headers: `类别` / `对象` / `口径` / `证据` / `约束` / `结论`
- Note: `规则：超过 6 列或 8 行时优先拆表，不把正文缩到不可读。`

Text limits:

- Prefer 4-6 columns and 4-8 rows.
- Body cells should be short phrases. If a cell needs a paragraph, split the
  row or move detail into appendix.
- Body font can be `10.5-11.5 pt` only when rendered text remains readable.

QA:

- Use one horizontal alignment mode across the whole table. This sample uses
  all-left because cells are evidence/action phrases.
- Vertically middle-align cells by default.
- The table must not look like a pasted spreadsheet or source-data dump.
- Do not keep more columns by shrinking text below readable size; split the
  table instead.
- Keep the bottom note outside the table and above the logo-safe area.

## `TBL-03A` Metric / Evaluation Table

Use when a review or leadership-facing page needs a compact metric/evaluation
table.

Recommended geometry:

| Element | x | y | w | h | Notes |
|---|---:|---:|---:|---:|---|
| Title | `0.37` | `0.10` | `12.60` | `0.72` | Use the real title placeholder |
| Framing sentence | `0.70` | `1.12` | `11.95` | `0.36` | One short conclusion |
| Table | `0.70` | `1.72` | `11.95` | `4.10` | 4 columns, 4-6 body rows |
| Bottom note strip | `0.70` | `6.08` | `11.95` | `0.52` | Optional conclusion or next action |

Recommended column widths:

| Column | Width | Notes |
|---|---:|---|
| `指标` | `1.60 in` | Short metric name |
| `判断内容` | `3.10 in` | What is being evaluated |
| `通过标准` | `3.55 in` | Clear acceptance condition |
| `业务含义` | `3.70 in` | Why it matters |

Sample text:

- Title: `指标评估示例`
- Framing sentence: `先明确判断口径，再说明通过标准。`
- Headers: `指标` / `判断内容` / `通过标准` / `业务含义`
- Example rows:
  - `范围` / `是否限定对象边界` / `同一对象、同一时间窗` / `避免跨范围误判`
  - `质量` / `证据是否可解释` / `来源、口径、结果可追溯` / `支撑评审复核`
  - `时效` / `处理是否及时` / `关键状态按日更新` / `便于持续跟踪`
  - `风险` / `是否有异常兜底` / `异常场景有处理路径` / `降低交付风险`
- Note: `输出：通过标准不清晰时，先补口径，不急于填结论。`

Table formatting:

- Header row: brand-blue fill, white bold text, vertical-middle alignment.
- Body rows: white or very light fill, black/near-black text.
- Use thin gray grid lines.
- Default horizontal mode for this sample is all-left because body cells are
  sentence-like.
- Vertically middle-align every cell.
- Use `12-13 pt` body text and `13-14 pt` header text.

QA:

- Header and body must use one horizontal alignment mode consistently.
- Body text must not look like a pasted spreadsheet; split rows before shrinking
  below `11 pt`.
- Do not stretch row height just to fill space.
- Bottom note strip text must stay inside its visible frame.
- The table and note strip must not overlap the bottom-right logo.

## `SUM-02A` Decision Recap / Handoff

Use when the final page needs to make review decisions and next actions clear.

Recommended geometry:

| Element | x | y | w | h | Notes |
|---|---:|---:|---:|---:|---|
| Title | `0.37` | `0.10` | `12.60` | `0.72` | Use the real title placeholder |
| Conclusion strip | `0.70` | `1.18` | `11.95` | `0.68` | One sentence |
| Decision block 1 | `0.70` | `2.16` | `3.65` | `1.42` | `结论` |
| Decision block 2 | `4.84` | `2.16` | `3.65` | `1.42` | `责任` |
| Decision block 3 | `8.98` | `2.16` | `3.65` | `1.42` | `下一步` |
| Handoff table | `0.70` | `4.02` | `11.95` | `1.45` | Owner/date/action rows |
| Bottom note strip | `0.70` | `5.88` | `11.95` | `0.58` | Optional follow-up rule |

Sample text:

- Title: `决策复盘示例`
- Conclusion: `结论：方案可以进入试点，先补齐口径和责任边界。`
- Decision blocks:
  - `结论` / `同意按试点范围推进`
  - `责任` / `明确负责人和协同团队`
  - `下一步` / `完成口径确认和材料补齐`
- Table headers: `事项` / `负责人` / `时间` / `输出`
- Example rows:
  - `口径确认` / `业务团队` / `本周内` / `统一判断标准`
  - `试点验证` / `项目团队` / `下阶段` / `形成验证结果`
  - `复盘汇报` / `牵头团队` / `评审后` / `同步风险和结论`
- Note: `跟进：重要结论进入项目清单，避免只停留在会议纪要。`

Text limits:

- Conclusion strip: one short sentence.
- Decision block body: <= 2 short lines.
- Handoff table: 3-4 rows, short phrases.
- Bottom note: one short sentence.

QA:

- Final page must not be a decorative thank-you page.
- Decision blocks use fixed inner text zones; body text must not spill outside.
- Owner/date/action table uses consistent all-left alignment and vertical-middle
  cells.
- Keep the table and bottom note above the logo-safe area.
- If follow-up work needs more than four rows, split into a dedicated work-plan
  table instead of shrinking text.

## Asset Promotion Checklist

Before adding a cleaned sample slide to the V1 template:

- The slide uses the current V1 template master/layout chrome.
- The sample contains no source-deck content, screenshots, URLs, contacts,
  project names, customers, or real data.
- All placeholder text is neutral Chinese and fits inside its visible frame.
- Large placeholder frames should not use pure white fill on top of the white
  canvas; use light gray fills so QA does not mistake them for accidental cover
  panels.
- All text uses `微软雅黑` / `Microsoft YaHei`.
- Colors come from `references/theme-contract.md`.
- All visible frames have inner text zones; no text extends outside a frame.
- The bottom-right logo remains clear after render.
- The sample is rendered to image and visually checked.
- `scripts/pptx_quality_gate.py` reports no new blocker for the sample deck.

Do not add the next batch of sample variants until the current V1 sample set is
rendered and reviewed successfully. When adding variants, promote only the
layout shapes that solve repeated generation failures or recurring reference
patterns.
