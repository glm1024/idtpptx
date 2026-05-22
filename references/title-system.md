# Title System And Placeholder Cleanup

Use this whenever a deck is created from a template, external deck, or generated code. Title mistakes are highly visible in PowerPoint edit mode, even when the slide looks acceptable in a PDF export.

## Core Decision

When a title looks wrong, do not solve it with only one lever. Use this order:

1. Remove or replace leftover placeholders and source-deck title elements.
2. Normalize the title zone to the registered template chrome.
3. Then choose the title font size based on page type and title length.

Do not enlarge a title just to fill an oversized placeholder box. Do not keep a tall title band just because the source layout had one.

## Placeholder Cleanup

- Final decks must not contain PowerPoint default prompts such as `单击此处添加标题`, `单击此处添加副标题`, `单击此处添加文本`, or `Click to add title`.
- If a placeholder is not needed, delete the whole placeholder shape. Do not only clear its text, because PowerPoint can show the default prompt again in edit mode.
- Every slide should have one audience-facing title system. Delete duplicate title placeholders, old subtitle placeholders, old agenda/title text, and any title copied from a source deck unless it was intentionally rewritten for the current audience.
- Section divider pages use the center blue bar as the title. They should not also keep a top-left title placeholder.
- Cover pages use one main title plus an optional real subtitle. A subtitle is not a second version of the title and must not overlap the main title.

## Title Zone Contract

Normal content slides:

- Keep the top title band compact: the title plus template divider rule should usually occupy the first `0.85-1.10 in` of the slide.
- Body content should usually start around `1.15-1.35 in` from the top, depending on whether the title is one or two lines.
- If the title area consumes more than about `1.25 in`, compress the title zone or move body content up before shrinking body content.
- Keep one top-left title box aligned to the template's left edge. Do not draw a second custom title bar inside the page.

Cover slides:

- Keep the blue cover header and white body. Do not preserve the old broad gray
  cover title band unless the user provides a new approved cover reference that
  explicitly uses it.
- Use plain metadata text on the canvas. Do not add a white metadata card just to balance the cover.

Section divider slides:

- Use only the center blue section bar and its section title/number block.
- Remove any top-left title placeholder inherited from a generic content layout.

## Title Font Size

Use these as starting points, then check the rendered slide:

| Page Type | Recommended Size | Notes |
|---|---:|---|
| Cover main title | `34-44 pt` | Use one dominant title. Avoid duplicate title/subtitle stacks. |
| Cover subtitle | `20-26 pt` | Use only for a real qualifier, version, or scope. |
| Normal content title | `24-30 pt` | Default to `26-28 pt` for most Chinese internal report pages. |
| Long content title | `22-26 pt` | Allow at most two lines; prefer shortening before shrinking below `22 pt`. |
| Section divider title | `22-30 pt` | White title inside the blue bar. |

If a normal content title is short but still looks small in the template band, raise it toward `26-28 pt`. If a long title does not fit, shorten it, split title/subtitle, or allow a two-line title at `22-26 pt`; do not leave PowerPoint's oversized default title prompt.

## QA Checks

- Text extraction contains no default placeholder prompts or template placeholder words.
- PowerPoint edit mode does not show dashed empty title/subtitle placeholders on final slides.
- Each slide has one visible title system, not a template title plus a manually drawn title.
- Normal content titles are visually balanced with the title band: not tiny in a large box and not oversized over the divider rule.
- Section divider slides have no top-left title placeholder.
