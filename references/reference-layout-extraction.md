# Reference Layout Extraction

This document extracts reusable layout lessons from the local reference corpus
at `../ppt-reference/`.

The source PPTs are local-only research material. Do not copy their business
content, screenshots, customer/project details, or full visual themes into this
skill. Extract only repeatable page structures, typography rules, slot patterns,
and QA risks that fit `IDT/Inspur Pragmatic`.

## Analysis Scope

Local corpus:

`../ppt-reference/`

Current scan:

- 11 PowerPoint files.
- About 57 MB of local-only reference material.
- 413 slides total.

Analysis method:

- Counted slides, text shapes, fonts, font sizes, images, tables, and charts
  with `python-pptx`.
- Rendered contact sheets with the base `pptx` skill thumbnail workflow.
- Reviewed page structures by category: cover, directory, table, screenshot,
  technical diagram, process, planning/review, and summary.

## High-Level Findings

The reference corpus should influence `idtpptx` in this order:

1. Rules and slot contracts.
2. Layout IDs in `references/layout-registry.md`.
3. Cleaned sample slides in the single official V1 template.
4. QA checks.

Do not merge source-deck pages into the V1 template. Rebuild only cleaned,
neutral sample slides from registered layout specs.

## Typography Lessons

Observed font usage:

- The dominant editable Chinese font is `微软雅黑` / `Microsoft YaHei`.
- Several older technical decks mix default theme fonts such as `+mn-ea` and
  Latin fonts such as `Times New Roman`; do not inherit those as rules.
- `附件2：持续改进优秀案例及优秀复制推广案例评选模板.pptx` contains an explicit
  format page that is useful as a company-style clue, not as a full replacement
  for the current theme contract.

Useful format clues from the reference corpus:

- Full document uses `微软雅黑`.
- Page title around `30 pt` bold is acceptable for formal templates.
- First-level headings around `16 pt` bold are common.
- Body text around `16 pt` with roughly `1.5x` line spacing is acceptable in
  document-like report pages.
- Tables often use a blue header row with white header text, black body text,
  and vertical-middle alignment.

How to adapt this into `idtpptx`:

- Keep `references/theme-contract.md` as the authority: default editable font
  remains `微软雅黑 / Microsoft YaHei`.
- Keep normal slide title guidance at `24-30 pt`; allow `30 pt` for formal
  report templates, but do not let PowerPoint default oversized title boxes
  survive.
- Keep body text black or near-black. Do not adopt the reference template's
  phrase "正文统一使用白色" as a default; that only applies to white text on blue
  shapes in that source template.
- Strengthen table rules around blue header rows, vertical centering, and
  consistent horizontal alignment.

Recommended follow-up:

- Update `references/typography.md` after review to include the formal-template
  font clue: `30 pt` title / `16 pt` heading / `16 pt` body / `1.5x` line
  spacing for document-like report pages.

## Cover Patterns

Observed sources:

- `反向代理访问虚拟机控制台.pptx`
- `裸金属图形化控制台v1.0.pptx`
- `跨云迁移分享.pptx`
- `云智能助手架构和功能设计方案1015_副本.pptx`
- `智能编码专项 - V2.2.pptx`

Reusable patterns:

| Proposed ID | Pattern | When To Use | Asset Decision |
|---|---|---|---|
| `COV-01` | Simple corporate cover with title and logo | Default training/report cover | Registered fallback; no cleaned V1 sample yet |
| `COV-02` | Formal report cover with broad top/center title band and metadata | Leadership review, technical方案评审 | Promoted to registry; V1 template sample exists |
| `COV-03` | Visual hero cover with generated/product image | Marketing or special showcase only | Do not make default |

Rules to absorb:

- Cover should carry title, optional subtitle, date/version/department, and logo.
- Long purpose/scope text belongs on slide 2, not on the cover.
- Generated hero covers are not the default IDT/Inspur internal style.

## Directory / Chapter Progression

Observed sources:

- `反向代理访问虚拟机控制台.pptx`
- `跨云迁移分享.pptx`
- `裸金属图形化控制台v1.0.pptx`
- `新邮箱系统使用培训-数据备份手册.pptx`

Reusable patterns:

| Proposed ID | Pattern | When To Use | Asset Decision |
|---|---|---|---|
| `DIR-01` | Numbered chapter list with one current item highlighted | Training deck, solution walkthrough | Promoted to registry; V1 template sample exists |
| `DIR-02` | Section opener with chapter number and short title | Operation manual modules | Candidate if current `SEC-01` is too sparse |

Rules to absorb:

- Use a directory/progress page for decks longer than roughly 12 slides.
- Highlight only the current chapter; do not turn all rows into colorful cards.
- Use restrained brand blue by default. Orange/amber should mean "current" or
  "warning", not decoration.

## Table Patterns

Observed sources:

- `云智能助手架构和功能设计方案1015_副本.pptx`
- `跨资源池调度方案设计v1.0-孔维亭.pptx`
- `ICOS v5资源池管理方案2.pptx`
- `智能助手-资源-26年技术规划研讨-0.1_副本.pptx`
- `附件2：持续改进优秀案例及优秀复制推广案例评选模板.pptx`

Reusable patterns:

| Proposed ID | Pattern | When To Use | Asset Decision |
|---|---|---|---|
| `TBL-01` | Compact categorical comparison table | Feature/option comparison | Replaced by cleaner V1 table variants |
| `TBL-02` | Dense evidence/protocol table | API, protocol, capability, route, constraint evidence | Promoted to registry; V1 template sample exists |
| `TBL-03` | Metric/evaluation table | 指标、阶段目标、评审标准、评分项 | Promoted to registry; V1 template sample exists |
| `TBL-04` | Plan/owner/date table | 工作计划、复制推广计划、收益计划 | Candidate registry addition |

Rules to absorb:

- Table header may use brand-blue fill with white bold text.
- Body cells should default to black text with no fill or very light fill.
- Vertical middle alignment is the default.
- Pick one horizontal alignment mode for the whole table:
  - center for short categorical matrix cells;
  - left for sentence/evidence/action cells.
- Dense technical tables may use smaller text only if still readable after
  rendering.

When to use left/right vs top/bottom:

- If the table is the primary evidence, make it the largest object on the page.
- If the table has 4-6 columns and 4-8 rows, use a full-width table.
- If a short table supports a diagram, place the table below or beside the
  diagram only when both remain readable.

QA risks:

- Many reference tables are effectively spreadsheets. Do not shrink them into a
  slide if they require tiny text.
- Split by category before going below readable size.

## Screenshot / Operation Manual Patterns

Observed sources:

- `新邮箱系统使用培训-数据备份手册.pptx`
- `云智能助手架构和功能设计方案1015_副本.pptx`

Reusable patterns:

| Proposed ID | Pattern | When To Use | Asset Decision |
|---|---|---|---|
| `SS-01` | One screenshot with explanation | Single UI evidence page | Registered fallback; no cleaned V1 sample yet |
| `SS-02` | Two/three screenshots with arrows and captions | Step-by-step operation manual | Promoted to registry; V1 template sample exists |
| `SS-03` | Troubleshooting screenshot plus problem/solution text | FAQ or exception handling with visual evidence | Promoted to registry; V1 template sample exists |

Rules to absorb:

- Operation-manual pages should be screenshot-first.
- Use 1-3 screenshots per slide; more than 3 usually becomes unreadable.
- Use same screenshot ratio and height within one screenshot group.
- Use red arrows/boxes only for sequence or annotation.
- Preserve screenshot fidelity unless the user explicitly asks for redesign.

When to use left/right vs top/bottom:

- Two screenshots: side-by-side works well if both are readable.
- Three screenshots: horizontal sequence works for simple UI states; otherwise
  use a 2+1 split or split into multiple slides.
- Long screenshots: crop into meaningful panels, never keep arbitrary long
  original ratio.

## Technical Diagram / Architecture Patterns

Observed sources:

- `跨资源池调度方案设计v1.0-孔维亭.pptx`
- `反向代理访问虚拟机控制台.pptx`
- `跨云迁移分享.pptx`
- `InCloudOS SDN网络技术分享.pptx`
- `ICOS v5资源池管理方案2.pptx`

Reusable patterns:

| Proposed ID | Pattern | When To Use | Asset Decision |
|---|---|---|---|
| `ARC-01` | Left explanation + right diagram | Diagram needs narrative context | Promoted to registry; V1 template sample exists |
| `ARC-02` | Full-width technical diagram with bottom notes | Diagram is the primary evidence | Promoted to registry; V1 template sample exists |
| `ARC-03` | Current vs target architecture comparison | Before/after topology or migration方案 | Candidate registry addition |

Rules to absorb:

- Technical diagrams need readable labels more than decorative polish.
- If the diagram is complex, give it the full page width and move notes below.
- If the diagram is simple, left explanation + right diagram is efficient.
- If comparing two architectures, use a mirrored left/right structure with one
  clear arrow or divider.

When to use left/right vs top/bottom:

- Left/right: use when the explanation is as important as the diagram and both
  fit at readable size.
- Top/bottom: use when the diagram is wide or label-heavy.
- Full-page diagram: use when the diagram itself is the evidence; keep notes to
  a short bottom strip.

QA risks:

- Do not paste a dense architecture image as a small figure.
- Do not copy source-specific customer/project diagrams into the skill.
- Normalize diagram colors back to brand blue/black unless a status color is
  semantically necessary.

## Process / Roadmap Patterns

Observed sources:

- `智能编码专项 - V2.2.pptx`
- `智能助手-资源-26年技术规划研讨-0.1_副本.pptx`
- `跨资源池调度方案设计v1.0-孔维亭.pptx`
- `反向代理访问虚拟机控制台.pptx`

Reusable patterns:

| Proposed ID | Pattern | When To Use | Asset Decision |
|---|---|---|---|
| `PRC-01` | Horizontal process summary | 4-6 simple process stages | Registered fallback; no cleaned V1 sample yet |
| `PRC-02` | Grouped process blocks | Several stages with subpoints | Candidate registry addition |
| `PRC-03` | Roadmap / month-by-month path | Project plan, rollout plan, annual path | Promoted to registry; V1 template sample exists |

Rules to absorb:

- A process page should explain real sequence, not decorative steps.
- If each step has subpoints, use grouped blocks or a table instead of tiny
  cards.
- If dates are important, use roadmap structure.
- If the process depends on UI evidence, switch to `SS-*`.

QA risks:

- Step-card titles and bodies often overlap when long terms wrap.
- Do not use multiple accent colors unless they encode phase/status.

## Planning / Leadership Review Patterns

Observed sources:

- `智能助手-资源-26年技术规划研讨-0.1_副本.pptx`
- `智能编码专项 - V2.2.pptx`
- `跨资源池调度方案设计v1.0-孔维亭.pptx`
- `附件2：持续改进优秀案例及优秀复制推广案例评选模板.pptx`

Reusable patterns:

| Proposed ID | Pattern | When To Use | Asset Decision |
|---|---|---|---|
| `RPT-01` | Current state / gap / action | Leadership review or technical planning | Registry backlog candidate |
| `RPT-02` | SWOT / four-look analysis | Planning workshop or strategy discussion | Candidate registry addition |
| `RPT-03` | Evaluation metric sheet | Review criteria or acceptance framing | Candidate registry addition, related to `TBL-03` |

Rules to absorb:

- Leadership review pages should lead with conclusion and then evidence.
- Do not use code-level identifiers when the audience is management unless
  they are essential terms.
- Keep dark or high-saturation marketing pages out of default `idtpptx`; use
  them only as exception style when explicitly requested.

## Summary / Closing Patterns

Observed sources:

- Several old decks end with `谢谢` image pages.
- `智能编码专项 - V2.2.pptx` includes a more promotional closing.

Reusable patterns:

| Proposed ID | Pattern | When To Use | Asset Decision |
|---|---|---|---|
| `SUM-01` | Restrained summary / next steps | Default ending for internal decks | Registry backlog already exists |
| `SUM-02` | Decision recap with owners and dates | Review handoff | Promoted to registry; V1 template sample exists |

Rules to absorb:

- Default closing should be reader-facing and useful: conclusion, decision, next
  steps, owner/date.
- Do not default to decorative `THANKS` pages or stock photos.

## Registry Promotion Decision

Promoted into `references/layout-registry.md` in this pass:

| Layout | Why |
|---|---|
| `SS-02` Two / Three Screenshot Step Sequence | Directly addresses screenshot-heavy training/manual decks |
| `ARC-02` Full-Width Technical Diagram | Gives architecture/topology diagrams enough width to keep labels readable |
| `TBL-03` Metric / Evaluation Table | Covers recurring metric, review, and acceptance tables |
| `COV-02` Formal Review Cover | Gives leadership/formal review decks a cleaner cover option |
| `DIR-01` Numbered Directory / Progress Map | Supports long training and solution decks with chapter orientation |
| `PRC-03` Roadmap / Rollout Path | Covers project plans, phased rollout, and leadership update timelines |
| `SS-03` Troubleshooting Screenshot | Gives FAQ/exception pages a stable screenshot + diagnosis structure |
| `ARC-01` Left Explanation + Right Technical Diagram | Covers architecture pages where explanation and diagram are equally important |
| `TBL-02` Dense Evidence / Protocol Table | Covers dense technical evidence tables without shrinking into spreadsheet style |
| `SUM-02` Decision Recap / Handoff | Replaces decorative closing pages with conclusion, owner, date, and action fields |

Remaining candidates should be reviewed before being added to
`references/layout-registry.md`:

| Candidate | Priority | Why |
|---|---|---|
| `PRB-02` Background / Constraint / Scheme | Medium | Useful for technical方案说明, but should wait until real decks show repeated four-block explanation needs |
| `TBL-04` Plan / Owner / Date Table | Medium | Useful for work plans, but should be distinct from `SUM-02` handoff tables |
| `ARC-03` Current vs Target Architecture | Medium | Useful for migration and before/after topology, but needs careful two-diagram readability rules |
| `RPT-01` Current State / Gap / Action | Low-Medium | Useful for leadership reviews, but may overlap with `PRB-02` and `TBL-03` |

Do not add all of them to the PPTX template at once. Promote one or two at a
time, starting with the layouts most likely to improve current output quality.

## Template Asset Status

The single official V1 template now contains the cleaned samples:

- `assets/templates/inspur-pragmatic-template-v1.pptx`
- Built by `scripts/build_template.py`
- Contains cleaned `COV-02A`, `DIR-01A`, `PRC-03A`, `SS-02A`, `SS-03A`, `ARC-01A`, `ARC-02A`, `TBL-02A`, `TBL-03A`, and `SUM-02A` sample slides.
- Contains no source screenshots or source-deck business content.

Do not keep a second PPT template for normal generation. The V1 template is the
single source for master chrome, brand calibration, sample specimens, and
fallback editing. Agents should normally compose final pages from registered
components and recipes instead of duplicating the sample sequence page by page.

## Next Concrete Step

Use the V1 template in real PPT generation/editing tasks and inspect whether
`COV-02A`, `DIR-01A`, `PRC-03A`, `SS-02A`, `SS-03A`, `ARC-01A`, `ARC-02A`,
`TBL-02A`, `TBL-03A`, and `SUM-02A` reduce cover, directory, roadmap,
screenshot, troubleshooting, architecture, table-page, and closing-page
failure modes without making every deck look like the same template tour.

Do not add more variants until these current samples have been used or reviewed
successfully. The next promotion should come from a repeated failure in real
deck generation, not from collecting attractive reference pages.
