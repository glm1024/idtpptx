# IDT/Inspur Theme Contract

This is the source of truth for the default `idtpptx` visual theme. The theme is fixed unless the user provides a newer company template, brand guide, or style-correct reference deck.

## Default Theme

**Name:** IDT/Inspur Pragmatic

**Purpose:** internal training, operation manuals, solution reporting, data analysis, project reviews, and leadership updates.

This is not a multi-theme design system. Do not offer Ocean, Forest, Golden, Galaxy, dark tech, magazine, Swiss poster, or warm marketing themes as defaults. Use scenario variants to adjust density and layout, not to change the color or font system.

## Color Tokens

| Token | Hex | Use For | Do Not Use For |
|---|---|---|---|
| Canvas White | `FFFFFF` | Main slide background and quiet content areas | White cards placed on top of a white cover |
| Soft White | `FAFAFA` | Very light content panels when a panel is structurally necessary | Decorative boxes used only to make the slide look designed |
| Primary Blue | `0062AC` | Brand accents, header rule, section bars, selected states | Long paragraphs or large filled backgrounds on normal content slides |
| Deep Blue | `00518E` | Stronger title accents, section divider depth, small brand blocks | Replacing the white canvas with a dark slide theme |
| Dark Navy | `213261` | Title text, compact anchors, strong contrast on light backgrounds | Large dark tech backgrounds unless the user explicitly asks |
| Body Black | `000000` | Normal body, table text, captions, notes, and sources | None; this is the safest readable text color |
| Near Black | `111111` / `1F2933` / `202020` | Body text when pure black feels too hard | Decorative low-contrast text treatment |
| Rule Gray | `A4A3A4` | Thin rules, grid lines, separators, disabled structure | Normal editable text |
| Light Fill Gray | `F2F2F2` / `F2F4F7` / `EDEDED` | Table headers, subtle bands, disabled placeholders | Large empty panels, cover metadata boxes, or fake cards |
| Light Cyan | `BBE0E3` | Rare secondary highlight in template-compatible contexts | A second theme color for every card or step |
| Risk Red | `D93025` / `C00000` / `FF4B4B` / `FF0000` | Warnings, risks, key callouts, screenshot arrows and boxes | Ordinary category labels or decorative emphasis |
| Success Green | `2E7D32` / `70AD47` | Completed, healthy, accepted states | Decorative process steps |
| Caution Amber | `FFC000` / `D6B656` | Pending, caution, needs-confirmation states | General highlights or table striping |

Use colors as brand or meaning. A slide should usually read as white, black/near-black, and restrained blue. Red, green, and amber are semantic exceptions, not decoration.

## Font Contract

- Default editable font: `微软雅黑` / `Microsoft YaHei`.
- Use bold YaHei for titles, section labels, card headings, and table headers.
- Keep Chinese, English, numbers, and punctuation in the same YaHei rhythm unless a code/command snippet needs monospace.
- Code, SQL, commands, file paths, and API snippets may use `Consolas`, `Menlo`, `Monaco`, or `Courier New` at small sizes.
- Do not introduce DejaVu, FreeSans, FreeSerif, Aptos, Calibri, Arial, Songti, Fangsong, Kaiti, or generic theme-default fonts for normal editable content unless the user explicitly asks to match a source deck.
- Fonts inside screenshots stay as-is. Do not redraw a screenshot only to normalize fonts.

## Scenario Variants

Scenario variants adjust structure and density while keeping the same color and font contract.

| Scenario | Prefer | Avoid |
|---|---|---|
| Internal training | Section divider, Text Explanation, Process Summary | Marketing hero pages and large abstract illustrations |
| Operation manual | Screenshot Step, appendix large screenshots, concise numbered labels | Rebuilding real screenshots as decorative mockups |
| Solution reporting | Comparison Table, Choice/Recommendation, Problem/Solution | Multicolor cards and poster-style summaries |
| Data analysis | Tables, charts, numeric callouts, evidence captions | Decorative dashboards with unrelated colors |
| Project review | Process Summary, risk/decision tables, concise conclusions | Dense paragraphs without structure |
| Leadership update | Clear conclusion, restrained table or comparison, fewer details per slide | New theme colors used to make the deck feel executive |

## Custom Theme Boundary

Do not create a new theme from the topic alone. A custom or revised company theme is allowed only when the user provides one of these inputs:

- A company-approved PPTX template.
- A brand guide with colors, fonts, and usage rules.
- A style-correct reference deck and explicit instruction to update the skill.

When a new reference changes the theme, update this contract first, then update the style guide, QA rules, and any helper checks that depend on the tokens.
