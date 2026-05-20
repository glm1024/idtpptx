# Theme Preview Guide

Use this as a visual calibration guide before creating or reviewing an `idtpptx` deck. The preview mechanism exists to keep agents aligned to the IDT/Inspur company style; it is not a theme picker.

## Preview Principle

`idtpptx` has one default theme: `IDT/Inspur Pragmatic`. Do not show users a multi-theme showcase or ask them to choose from generic palettes. If a user wants a different style, treat that as an explicit style exception or a future company-theme update, not as the default flow.

## Standard Preview Set

A useful preview should include these five slide types:

| Preview Slide | What It Should Demonstrate |
|---|---|
| Cover | White/gray canvas, restrained blue band, one clean title/subtitle system, plain metadata text, no redundant white card |
| Text Explanation | Compact top-left title, no leftover title placeholder, black body text, restrained blue accents, readable line spacing |
| Comparison Table | Quiet grid, middle-aligned cells, one table-wide horizontal alignment mode, black text, light header fill, no heavy color blocks |
| Screenshot Step | Real UI evidence in standard image slots, red annotations only where needed |
| Process Summary | Simple blue/black structure, clear stages, no multicolor infographic styling |

## How To Use It

- For template work, render `assets/templates/inspur-pragmatic-template-v1.pptx` or the working deck and inspect the contact sheet.
- For final QA, compare high-risk slides against the preview set: cover, table, screenshot, generated image, process, and external copied pages.
- If a page no longer feels like the preview set, diagnose whether the cause is theme drift, wrong page type, wrong material slot, spacing, or logo-safe-zone misuse.

## What Not To Do

- Do not copy `theme-factory/theme-showcase.pdf`.
- Do not add a generic 10-theme showcase to this skill.
- Do not import `theme-factory/themes/*.md`.
- Do not let generated images include their own title, footer, page number, logo, border, deck frame, or external theme treatment.
- Do not treat preview pages as content to copy into deliverable decks; they are a calibration reference.
