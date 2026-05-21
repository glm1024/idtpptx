# Reference Deck Inventory

This file tracks company-internal PPT decks that can inform future `idtpptx`
layout assets. These decks are local-only reference material, not template
assets, and should not be committed or distributed with the skill.

Do not copy source business content into the skill. Extract only reusable
layout patterns, slot structures, density rules, and QA lessons that still fit
the fixed `IDT/Inspur Pragmatic` theme.

## Scan Scope

Local source folder:

`../ppt-reference/`

The local reference folder sits outside this skill repository and is not part of
the distributable skill. If this inventory is used on another machine, the
source decks may be absent; rely on the distilled patterns below and
`references/reference-layout-extraction.md` unless a local reference corpus has
been provided again.

Initial scan date: 2026-05-21

Method:

- Counted slides, editable text, images, tables, and charts with `python-pptx`.
- Rendered contact-sheet thumbnails with the base `pptx` skill's
  `scripts/thumbnail.py`.
- Visually reviewed page structures against `references/layout-map.md`,
  `references/theme-contract.md`, and `references/text-box-fit.md`.

## Deck Summary

| Deck | Slides | Strong Reference Value | Reusable Patterns | Cautions |
|---|---:|---|---|---|
| `ICOS v5资源池管理方案2.pptx` | 25 | Medium | Technical scheme pages, architecture diagrams, comparison tables, issue-summary pages | Some pages are content-dense and old-style; do not copy business diagrams directly |
| `InCloudOS SDN网络技术分享.pptx` | 48 | Medium | Technical comparison tables, network architecture diagrams, feature matrices, chapter separators | Decorative teal/graphic theme is not the current IDT default |
| `云智能助手架构和功能设计方案1015_副本.pptx` | 49 | High | Dense architecture pages, wide comparison tables, protocol/route tables, screenshot evidence pages | Many pages are too dense for default body slides; useful mainly as table/architecture references |
| `反向代理访问虚拟机控制台.pptx` | 31 | High | Simple corporate cover, numbered目录, topology explanation, problem/solution sequence, scheme comparison | Thick blue title band is useful as reference but should be adapted to current compact title system |
| `新邮箱系统使用培训-数据备份手册.pptx` | 54 | High | Operation-manual screenshot steps, screenshot sequence with red arrows, section divider, FAQ/problem pages | Screenshots and support details are source content; only absorb screenshot-step structure |
| `智能助手-资源-26年技术规划研讨-0.1_副本.pptx` | 14 | Medium | Planning/report structure, SWOT, evaluation metrics, roadmap-like tables | Text-heavy pages need stronger fit rules before becoming layout assets |
| `智能编码专项 - V2.2.pptx` | 51 | Medium | Large data panels, industry benchmark cards, chart pages, annual path, summary pages | Overall visual style is darker, more marketing-like, and more saturated than `idtpptx` default |
| `裸金属图形化控制台v1.0.pptx` | 40 | Medium | Problem/background pages, directory pages, simple tables, technical comparison pages | Many slides are sparse placeholders; do not absorb empty shell pages |
| `跨云迁移分享.pptx` | 28 | Medium | Directory progression, vendor comparison tables, migration architecture diagrams, key-system explanation | Older style and red/blue accent mix need adaptation |
| `跨资源池调度方案设计v1.0-孔维亭.pptx` | 32 | High | Strategic report pages, scenario diagrams, comparison tables, resource reconstruction diagrams, application-scenario pages | Green/gray accent system is not default; translate into blue/black theme before reuse |
| `附件2：持续改进优秀案例及优秀复制推广案例评选模板.pptx` | 21 | Low-Medium | Case template structure, format-requirement page, improvement-effect table, evidence-material placeholders | It is more of a submission template than a company-style report deck |

## First Absorption Candidates

These are the safest patterns to convert into registered `idtpptx` layout
variants first.

| Candidate ID | Source Inspiration | Target Registered Type | Why It Helps |
|---|---|---|---|
| `SS-02` | `新邮箱系统使用培训-数据备份手册.pptx` screenshot instruction pages | Screenshot Step Page | The deck has many practical UI walkthrough pages with screenshot slots and red-arrow sequencing |
| `TBL-02` | `云智能助手架构和功能设计方案1015_副本.pptx` protocol/route/comparison tables | Comparison Table Page | Adds a dense but controlled evidence-table variant for technical schemes |
| `ARC-01` | `跨资源池调度方案设计v1.0-孔维亭.pptx`, `反向代理访问虚拟机控制台.pptx`, `跨云迁移分享.pptx` | Process / Workflow Summary Page | Provides a native technical architecture/flow explanation page instead of forcing diagrams into cards |
| `PRB-02` | `反向代理访问虚拟机控制台.pptx`, `裸金属图形化控制台v1.0.pptx` | Problem/Solution Page | Useful for 背景 / 问题 / 方案 / 约束 style technical explanation |
| `DIR-01` | `反向代理访问虚拟机控制台.pptx`, `跨云迁移分享.pptx`, `裸金属图形化控制台v1.0.pptx` | Section Divider / Text Explanation Page | Numbered directory/progress page can support longer training decks |
| `RPT-01` | `智能助手-资源-26年技术规划研讨-0.1_副本.pptx` | Text Explanation Page / Comparison Table Page | Planning and evaluation pages can inform leadership-review variants |

## Useful Patterns By Page Type

### Cover

Useful references:

- `反向代理访问虚拟机控制台.pptx`
- `裸金属图形化控制台v1.0.pptx`
- `跨云迁移分享.pptx`

Absorb:

- Plain corporate cover with direct title and bottom-right logo.
- Minimal metadata, no decorative card stack.

Do not absorb:

- Full marketing-style AI hero image from `智能编码专项 - V2.2.pptx`.
- Decorative wave/teal graphics from `InCloudOS SDN网络技术分享.pptx`.

### Directory / Chapter Progression

Useful references:

- `反向代理访问虚拟机控制台.pptx`
- `跨云迁移分享.pptx`
- `裸金属图形化控制台v1.0.pptx`

Absorb:

- Numbered chapter list with one current chapter highlighted.
- Simple progress map for training or solution walkthrough decks.

Adaptation:

- Use current `idtpptx` blue/black theme.
- Avoid orange highlight unless it carries a documented warning/current-step meaning.

### Tables

Useful references:

- `云智能助手架构和功能设计方案1015_副本.pptx`
- `跨资源池调度方案设计v1.0-孔维亭.pptx`
- `ICOS v5资源池管理方案2.pptx`
- `智能助手-资源-26年技术规划研讨-0.1_副本.pptx`

Absorb:

- Wide technical comparison table.
- Protocol/API route table.
- Evaluation metric table.
- Decision matrix table.

Guardrails:

- Normalize to one horizontal alignment mode per table.
- Keep cell text vertically middle by default.
- Split overly dense tables rather than shrinking below readable size.
- Keep table styles consistent with `references/theme-contract.md`.

### Screenshot Steps

Useful references:

- `新邮箱系统使用培训-数据备份手册.pptx`
- `云智能助手架构和功能设计方案1015_副本.pptx`

Absorb:

- One to three screenshots per slide.
- Red arrows and compact step captions.
- Screenshot-first page design for operation manuals.

Guardrails:

- Preserve screenshot evidence by default.
- Standardize screenshot slots to avoid arbitrary image sizes.
- Remove support contacts, URLs, account examples, and source-specific details.

### Architecture / Flow

Useful references:

- `跨资源池调度方案设计v1.0-孔维亭.pptx`
- `反向代理访问虚拟机控制台.pptx`
- `跨云迁移分享.pptx`
- `InCloudOS SDN网络技术分享.pptx`

Absorb:

- Left explanation + right architecture diagram.
- Full-width technical topology with short notes.
- Before/after or current/target architecture comparison.

Guardrails:

- Register this as a company technical diagram variant before using it.
- Do not create decorative pipeline art.
- If a diagram is source-specific, use it only as a structure reference.

### Planning / Leadership Review

Useful references:

- `智能助手-资源-26年技术规划研讨-0.1_副本.pptx`
- `智能编码专项 - V2.2.pptx`
- `跨资源池调度方案设计v1.0-孔维亭.pptx`

Absorb:

- Evaluation metrics.
- Roadmap/path pages.
- Summary of current state, gap, and next action.

Guardrails:

- Keep the IDT white-background theme.
- Avoid dark blue full-page marketing panels unless the user explicitly asks for a non-default executive style.
- Do not invent KPIs or pseudo-data to fill the page.

## Not To Absorb

- Source deck business content, screenshots, customer names, URLs, email examples, contacts, and project-specific diagrams.
- Dark/high-saturation marketing theme from `智能编码专项 - V2.2.pptx`.
- Teal decorative wave/shape system from `InCloudOS SDN网络技术分享.pptx`.
- Empty section shells and sparse placeholder slides from older technical decks.
- `THANKS` / closing image pages as reusable company templates.
- Format-instruction pages marked as "成稿后本页删除".

## Recommended Next Step

Continue from the registered layout backlog instead of copying raw reference
slides into the `.pptx` template:

1. Refine the candidate IDs in `references/layout-registry.md`.
2. Pick 5-8 high-value reference slides and describe their slots in text.
3. Only after the slot rules are stable, rebuild the single official template:
   `assets/templates/inspur-pragmatic-template-v1.pptx`.

The current concrete layouts implemented in the V1 template are `COV-02`,
`DIR-01`, `PRC-03`, `SS-02`, `SS-03`, `ARC-01`, `ARC-02`, `TBL-02`, `TBL-03`,
and `SUM-02`. This covers formal covers, directory/progress pages, roadmaps,
screenshot operations, troubleshooting, left/right architecture explanations,
full-width diagrams, dense evidence tables, metric tables, and decision recap
pages.
