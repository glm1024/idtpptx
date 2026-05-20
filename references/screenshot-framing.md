# Screenshot And Image Framing

Use this whenever a deck includes product screenshots, UI walkthroughs, code screenshots, dashboard images, generated diagrams, or other visual evidence.

The goal is not to make decorative images. In this company PPTX style, screenshots and images are evidence that supports an internal training, report, or operation manual.

## Default Policy

- Preserve real screenshots by default. Do not redraw, beautify, or reinterpret them unless the user explicitly asks, or the original is unusable in a readable slot.
- Decide the slide page type and image slot before editing the image. Do not generate or crop images first and then force them into a slide.
- Use standard ratios instead of inheriting the screenshot's original odd ratio.
- Keep screenshots readable. If the whole screen becomes too small, crop to the meaningful area or split the walkthrough into multiple slides.
- Generated images are embedded materials, not slides. They must not include a PPT title, footer, page number, logo, border, deck chrome, or decorative frame inside the image itself.
- Keep the IDT/Inspur style: white canvas, restrained blue accents, black/near-black text, and red only for annotations, warnings, or key callouts.

## Slot Types

| Slot | Use For | Recommended Ratio | Notes |
|---|---|---|---|
| Single large screenshot | One primary UI state or dashboard | 16:9 or 16:10 | Crop to the meaningful region if full-screen text becomes unreadable. |
| Two-image comparison | Before/after, old/new, success/failure | Two matched 16:9 or 4:3 slots | Keep both screenshots the same visible size and crop density. |
| Three-step walkthrough | Operation manual flow | Three matched 4:3 or 16:9 slots | Use red arrows or short numbered labels between steps. |
| Table-side evidence | A table plus one proof screenshot | 4:3 or 1:1 | Keep the screenshot secondary; the table stays readable. |
| Appendix large screenshot | Reference evidence that needs inspection | 16:9 | Use a dedicated slide and avoid extra decoration. |
| Generated diagram | Concept, system relationship, or process visual | 16:9 or 16:10 | Use only when a real screenshot is not the evidence. |

Do not mix ratios inside one screenshot group. A row of screenshots should use one ratio, one crop density, and one caption style.

## Handling Real Screenshots

Use this decision order:

1. If the screenshot contains evidence that must stay accurate, keep it real.
2. If the screenshot ratio is close to the slot, crop or scale it into the slot.
3. If the screenshot is too busy, crop to the meaningful region instead of shrinking the whole screen.
4. If it is a long or narrow screenshot, split it into two or three same-size panels.
5. If sensitive text, accounts, avatars, or project names appear, ask or mask them before delivery.
6. Redesign or regenerate only when the original cannot be made readable or the user asks for a conceptual image.

For operation manuals, the step itself is more important than visual polish. Preserve the UI state, show the target control clearly, and use red boxes/arrows sparingly.

## Generated Image Rules

Generated images may be useful for system relationship diagrams, conceptual process visuals, or non-sensitive UI scenario illustrations. Keep them subordinate to the PPT slide structure.

Prompt requirements:

- Specify the final slot ratio, such as 16:9 or 16:10.
- Ask for a restrained corporate training/report style, not a magazine cover, Swiss poster, SaaS landing page, 3D render, or decorative tech background.
- Keep labels in the deck language. Chinese decks use Chinese labels.
- Ask for a clean white or near-white background unless the slide explicitly needs a transparent or screenshot-like asset.
- Prohibit slide chrome inside the image: no title, footer, page number, logo, watermark, border, or presentation frame.

Example prompt pattern:

```text
生成一张 16:9 横向信息图，用于公司内部 PowerPoint。主题是：[概念/流程]。
风格保持白底、黑色文字、少量蓝色强调，结构清晰、直角线框、无阴影、无渐变。
图中文字使用中文，标签要短。只生成核心图形本身，不要标题、页脚、页码、logo、水印、边框或 PPT 外壳。
```

## Cropping And Alignment

- Favor top or center crop based on the evidence. Admin pages usually need the top navigation and current page title; dashboards may need the central chart/table.
- Do not crop away the UI label, selected menu item, alert text, or target button being explained.
- Keep captions close to screenshots, usually `10-12 pt`, black or near-black.
- Keep screenshot groups left-to-right for process pages.
- Avoid placing important screenshot text under the bottom-right logo or near the slide edge.

## QA Checklist

Before delivery, verify:

- Every screenshot belongs to the current task, not the source template.
- The screenshot text is readable after rendering to slide images.
- All screenshots in a group use consistent ratio, crop density, and caption style.
- Red arrows/boxes point to the intended UI detail and do not hide important text.
- Generated images do not include deck chrome, fake logos, title bars, footers, or page numbers.
- No screenshot, generated image, caption, table, or annotation overlaps the bottom-right logo mark.
