# Company PPT QA Checklist

Run this after the base `pptx` skill QA.

## Brand And Layout

- Normal content slides keep the top rule, top-right blue marker, and bottom-right logo unless intentionally using cover/closing style.
- New slides match the simple white-and-blue corporate style.
- Titles are compact and aligned consistently.
- Main content fits the center content area without crowding the logo.
- No decorative gradients, stock-photo hero compositions, or marketing-style cards were introduced.

## Content Hygiene

- No source-deck training text remains unless explicitly requested.
- No old URLs, support contacts, email addresses, screenshots, product names, or credentials remain as accidental placeholders.
- Placeholder words such as `项目名称`, `截图占位`, `说明`, `对比项`, or `方案 A` do not remain in final deliverables.
- Screenshots belong to the current task and are readable.

## Practical Readability

- Dense tables remain legible after rendering.
- Red arrows/boxes point to the intended UI detail and do not cover important text.
- Multi-step screenshot pages read left to right.
- Body copy uses direct internal-document Chinese.
- No text overlaps the logo, page edge, screenshot, or table.

## Final Verification

- Render slides to images using the base `pptx` skill workflow.
- Inspect affected slides visually.
- If a fix changes layout, re-render the affected slide.
