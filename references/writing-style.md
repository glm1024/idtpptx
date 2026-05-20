# Writing Style

## Voice

Use natural internal-document Chinese. The tone should be clear, practical, and restrained.

Preferred:

- Direct business language.
- Short sentences.
- Clear action verbs.
- Operational wording that tells the reader what to do or how to judge.

Avoid:

- Marketing slogans.
- Abstract AI-sounding prose.
- Over-polished consulting language.
- Long paragraphs that bury the action.

## Titles

Titles should name the page's job.

Good patterns:

- `系统功能概述`
- `配置方式选择`
- `数据导出流程`
- `常见问题及处理`
- `方案对比`

Avoid:

- Vague titles like `背景介绍` when a more specific title is possible.
- Overly emotional or promotional titles.

## Body Structure

For operational content, prefer:

- `目标：`
- `范围：`
- `步骤：`
- `注意：`
- `结果：`

For problem pages, prefer:

- `问题：`
- `原因：`
- `解决：`

For recommendations, prefer:

- `推荐：`
- `适用场景：`
- `不适用场景：`
- `下一步：`

## Reader-Facing Content Only

Final slides should read like a document for the audience, not like an agent's work plan for making the PPT.

Default final-deck rule: delete the entire meta/setup page if its job is to explain why this PPT is an initial draft, what the generation pass will not cover, or how screenshots/data will be added later. Do not simply rewrite that page unless the user explicitly asked for a workshop agenda or discussion-scope slide.

Allowed:

- Business scope, delivery scope, implementation scope, and data-scope statements that the audience needs to know.
- Explicit assumptions, risks, open questions, or next steps that belong to the project itself.
- A version label such as `初版` when the user asked for a discussion draft or versioned handoff.

Not allowed in final slide text:

- How the agent planned to write the PPT.
- Statements that evidence, screenshots, or data will be filled in later because this generation pass did not include them.
- Visual-production caveats such as `本轮先不展开`, `不追求最终视觉定稿`, `先形成可讨论的结构草稿`, or `后续逐页补充数据和截图`.
- Meta-purpose titles or copy such as `初版目标与讨论范围`, `形成一版可讨论 PPT`, or `本轮先不展开` unless the user explicitly asks for that exact workshop framing.

Rewrite meta-process wording into audience-facing wording:

| Avoid | Use Instead |
|---|---|
| `用途：先形成可讨论的结构草稿，后续逐页补充数据和截图。` | `用途：用于对齐统计链路、归因口径和优化方向。` |
| `本轮先不展开` | `本页仅说明范围边界。` |
| `不追求最终视觉定稿` | Remove it; visual quality is still expected for every delivered deck. |
| `后续补充真实截图和数据` | `数据口径待确认` or `证据材料待补齐` only when that is a real project status the audience must see. |

## Content Density

This style accepts moderate density. It is acceptable for training/manual decks to carry more text than a sales deck, but each page should remain scannable.

If a slide needs more than 5-7 substantial bullets, split it.
