# Composition Grammar

Use this file after `references/component-system.md`. It turns registered page
types into composition recipes, so a deck can vary by content while staying
inside the IDT/Inspur style.

## Generation Order

1. Identify the page intent: cover, directory, explanation, table, screenshot,
   process, architecture, problem/solution, choice, or summary.
2. Inventory the material: number of screenshots, table columns/rows, process
   steps, architecture nodes, key conclusions, and density.
3. Pick a registered layout ID as a recipe, not as a slide to clone.
4. Choose components and slots from `references/component-system.md`.
5. Compose within the template content zone and reuse template chrome.
6. Run QA for overflow, logo safety, title system, theme drift, and template
   clone risk.

Do not start by duplicating every V1 sample slide that sounds close to the topic.
Duplicate a cleaned sample only when its recipe and density closely match the
current content, or when a low-risk fallback is needed.

## Recipe Selection

| Page Intent | Primary Recipes | Use When | Vary By |
|---|---|---|---|
| Cover | `COV-*` | title, subtitle, date, department | title scale, metadata count, subtitle presence |
| Directory | `DIR-*` / `SEC-*` | 3-6 chapters or chapter progress | active row, row count, section vs agenda |
| Explanation | `TXT-*` | scope, principle, background, conclusion setup | 1-3 text groups, note strip, key-value list |
| Table | `TBL-*` | criteria, metrics, responsibilities, evidence | column count, row count, left/center mode |
| Screenshot | `SS-*` | UI proof or operation steps | 1/2/3 slots, crop ratio, annotation density |
| Process | `PRC-*` | non-UI flow or phased path | card count, timeline vs step row, note placement |
| Architecture | `ARC-*` | topology, data path, system boundary | left/right vs full-width, node count, legend |
| Problem | `PRB-*` | FAQ, risk, issue handling | three-block diagnosis vs table |
| Choice | `CHO-*` | options and recommendation | two-column, three-option, recommended path |
| Summary | `SUM-*` | decision, owner, next action | field count, conclusion bar, action table |

## Density Rules

- Sparse material: use larger body text and fewer components. Do not leave tiny
  text floating in a large blank canvas.
- Medium material: use two-column, three-card, or table recipes.
- Dense material: prefer a table or split slides. Do not force dense material
  into cards or shrink text below readable size.
- Evidence-heavy material: give screenshots/tables/diagrams the largest slot.
- Conclusion-heavy material: use a conclusion bar or summary recipe, then keep
  supporting material compact.

## Variation Rules

Vary structure only when the content gives a reason:

- Change card count to match item count.
- Change table mode to match cell length.
- Change diagram orientation to keep labels readable.
- Change screenshot count and crop ratio to preserve evidence.
- Change title/subtitle split to keep the title band clean.
- Change note placement when the logo safe zone or screenshot slot requires it.

Do not vary:

- theme palette;
- font family;
- logo placement;
- page chrome;
- random decorative colors;
- page order just to look different.

## Anti-Clone Rules

A final deck should not read like the V1 sample template with new text.

Treat these as clone-risk warnings:

- The deck has the same page count and near-identical page sequence as the V1
  sample template.
- Most pages match the V1 sample slide geometry in the same order.
- A slide reuses a sample layout even though the content has a different
  material shape, such as using a roadmap for algorithm evidence or a card row
  for a dense table.
- A deck repeats the same card/table/process geometry across many unrelated
  pages.

When clone risk appears, do not add decoration. Re-plan the deck by content
shape and rebuild the affected pages from components.

## Planning Table

For non-trivial decks, draft this before editing:

| Page | Intent | Layout ID | Components | Material shape | Variant reason | Risk |
|---|---|---|---|---|---|---|
| 1 | Cover | `COV-02` | cover title, subtitle, metadata | title + 2 metadata rows | formal review | title fit |
| 2 | Explanation | `TXT-01` | title, key-value list, note strip | 3 conclusions | no screenshot/table needed | sparse text |
| 3 | Table | `TBL-03` | table header/body, conclusion note | 4x5 metric table | evaluation evidence | readability |

The planning table is a working artifact. Keep it outside the final deck unless
the user explicitly asks for a production appendix.

## Worked Decisions

- Three UI screenshots with arrows -> `SS-02`, not `PRC-01`.
- Four criteria with short pass/fail meanings -> `TBL-03`, not card grid.
- One wide data-chain diagram with many labels -> `ARC-02`, not `ARC-01`.
- Three open questions with short implications -> card composition under
  `PRB-01` or `TXT-01`, not a dense table.
- A final decision with owner/date/next step -> `SUM-02`, not a generic thank
  you page.
