---
name: idtpptx
description: Use when creating or editing PowerPoint/PPTX files that should follow the company's IDT/Inspur pragmatic presentation style. This is an overlay skill that depends on the existing pptx skill for all PPTX file operations, and adds company-specific template selection, layout mapping, writing style, and visual QA rules.
---

# IDT PPTX

This skill creates and edits company-style PowerPoint decks using a simple, pragmatic Inspur/IDT visual language.

## Hard Dependency

This skill depends on an installed skill named `pptx`. It does not replace or reimplement PPTX mechanics.

Before any real `.pptx` file operation, load/read the installed `pptx` skill and follow its guidance:

- `pptx/SKILL.md`
- `pptx/editing.md` for template-based editing
- `pptx/pptxgenjs.md` only when creating from scratch is unavoidable

Use the base `pptx` skill for reading, thumbnailing, unpacking, slide duplication, XML editing, cleaning, packing, rendering, and QA. Use this `idtpptx` skill only for company style decisions, template selection, layout mapping, business wording, and company-specific QA.

If the `pptx` skill is not installed or cannot be found, stop and ask the user to install it before continuing. Do not silently fall back to ad hoc PPTX manipulation.

## Default Approach

Prefer template-based editing over drawing new slides from scratch.

1. Use `assets/templates/inspur-pragmatic-template-v1.pptx` as the first-choice template.
2. Analyze the target content and map each section to one of the reusable page types in `references/layout-map.md`.
3. Use the base `pptx` workflow to duplicate, delete, reorder, and edit slides.
4. Keep the deck visually quiet, operational, and content-first.
5. Run both base `pptx` QA and the company QA checklist in `references/qa-checklist.md`.

## What To Load

- For visual rules, read `references/style-guide.md`.
- For choosing pages, read `references/layout-map.md`.
- For wording and tone, read `references/writing-style.md`.
- Before final delivery, read `references/qa-checklist.md`.

## Template Policy

The V1 template was distilled from a practical internal training deck. The original training content is not part of the skill. Treat the template as a layout and brand-style source only.

Keep reusable elements:

- Inspur logo placement
- White background and blue brand accents
- Thin top divider line
- Small right-top blue corner marker
- Section divider bar with simple numbered structure
- Large screenshot/table content zones
- Dense but readable operational text layout

Do not preserve source-deck business content:

- Do not copy old training copy, URLs, email examples, screenshots, support contacts, or product-specific instructions unless the user explicitly asks for that exact content.
- Replace all placeholders with the user's current material.
- If a screenshot slot is not needed, remove the entire placeholder group instead of leaving empty boxes.

## Style Summary

The style is practical corporate training/reporting, not a marketing deck:

- White canvas, restrained blue accents, minimal decoration.
- Clear top title area, mostly left-aligned text.
- One idea per slide when possible, but moderate information density is acceptable for training/manual decks.
- Screenshots and tables are primary visual evidence.
- Avoid decorative gradients, large hero illustrations, icon-heavy marketing layouts, and overly stylized “AI generated” slides.

## Evolution Workflow

When the user provides a better company-style PPT later:

1. Analyze it with the base `pptx` skill.
2. Compare it against the current `references/` rules.
3. Add only reusable style principles, layout patterns, or QA rules.
4. Do not dump source-deck content into the skill.
5. If a new reference conflicts with old rules, update the rule and note the applicable scenario.
