# Component System

`idtpptx` should produce variety by composing a limited set of company-style
components, not by cloning whole sample slides. The V1 template remains the
visual calibration source, but the normal generation unit is a component with a
clear slot, boundary, and QA rule.

## Core Principle

Keep the theme fixed and vary the composition.

- Fixed: colors, fonts, logo, title system, table language, screenshot fidelity,
  and restrained internal-report tone.
- Flexible: component count, component placement, row/column structure, diagram
  orientation, density, and emphasis hierarchy.
- Forbidden: random visual choice, one-off decorative styling, or generating a
  deck that follows the V1 sample slide sequence page by page when the content
  does not require it.

## Component Families

Use these component families before inventing a new full-slide template.

| Family | Components | Owns |
|---|---|---|
| Brand chrome | top rule, page marker, bottom-right logo, cover logo area | Template/master only |
| Title | compact content title, cover title, section bar title, subtitle | One title system per slide |
| Text | paragraph group, key-value list, note strip, conclusion bar, callout | Chinese-first business wording |
| Table | header row, body row, row stripe, footnote, conclusion note | Readable matrix/evidence structure |
| Card | side-stripe card, number badge, risk/status tag, three-column card row | Bounded short explanations |
| Process | step node, timeline axis, connector, phase block, boundary note | Ordered non-UI flow |
| Screenshot | screenshot slot, caption, red annotation box, arrow, zoom crop | UI evidence |
| Diagram | architecture node, lane, boundary box, connector, legend | Technical structure |
| Split | diagram zone, narrative zone, explanation strip, orientation rule | Diagram/text pages |
| Summary | decision field, owner/date field, next-action row | Handoff and closure |

## Component Contracts

### Brand Chrome

- Reuse the template master/layout chrome. Do not draw a second top rule, page
  marker, logo, footer, or slide frame inside the page.
- Content may use the space above and left of the bottom-right logo, but must
  not overlap the logo mark or its breathing margin.
- If a page needs a special cover/closing logo treatment, use a cover/summary
  recipe; do not insert another logo into a normal content page.

### Title Components

- Normal content title: compact top-left title, usually `24-30 pt`.
- Formal cover title: larger center title, usually `34-44 pt` only when the
  cover band has room.
- Section title: use a section bar or directory/progress component, not both a
  section bar and a normal top-left title.
- Delete unused PowerPoint title/subtitle placeholders before composing body
  content.

### Text Components

- Use black or near-black editable text by default.
- A note strip, conclusion bar, card, or callout owns an inner text box. The
  text box must be physically inside the visible frame.
- Prefer one clear sentence per note/callout. If a sentence cannot fit at
  readable size, shorten it, increase the frame height, split the component, or
  split the slide.

### Table Components

- Use a slide-native table structure, not a pasted spreadsheet look.
- Decide whether the table is the slide's primary table or an auxiliary matrix
  before styling it.
- Primary tables use the company table hierarchy: solid brand-blue header fill,
  white bold header text, light row striping, readable dark body text, and
  restrained light grid lines.
- Auxiliary matrices may use a light header fill only when another component is
  clearly the slide's main focus. Do not use a pale header for a full-slide
  primary comparison, review, risk, action, or metric table.
- Keep one main table hierarchy per slide. If two tables compete for attention,
  promote one, demote the other to a compact auxiliary matrix, or split the
  content.
- Header and body use one horizontal alignment mode for the table: all-left for
  explanations/evidence, all-center for compact categorical values.
- Cells are vertically middle-aligned by default.
- Dense tables should split by category before font size drops below readable
  limits.

### Card Components

- Cards are for short, parallel ideas. They are not a container for long
  narrative paragraphs.
- Every card needs separate title and body zones. If the title wraps to two
  lines, move the body down or shorten the title.
- Card rows should share one baseline, one width system, and consistent inner
  padding.

### Process Components

- Use process nodes for ordered steps, not decorative icons.
- A process step usually has a step label, title, and one short outcome line.
- If a process needs screenshots, switch to screenshot recipes. If it needs
  acceptance criteria, switch to table recipes.

### Screenshot Components

- Screenshot slots are decided before cropping or scaling.
- Preserve real UI evidence by default. Redesign screenshots only when the user
  asks or when the source image is unusable.
- Screenshot groups use one crop density, one ratio family, and one caption
  style.

### Diagram Components

- Diagrams should explain real structure: systems, layers, data paths, control
  paths, dependencies, or boundaries.
- Keep editable diagram nodes in theme colors. Use red/green/amber only for
  explicit risk/status meaning.
- If a source diagram is too dense, recreate the structure with fewer nodes
  rather than shrinking it into an unreadable image.

### Split Diagram / Text Components

- Use a split component when a technical diagram and a narrative explanation
  are both first-class slide content.
- Support both orientations:
  - diagram-left / text-right when the diagram is the reading entry;
  - text-left / diagram-right when the conclusion or boundary needs to be read
    before the diagram.
- The diagram zone should usually own 55-62% of the content width. The
  narrative zone should usually own 32-38% and contain 3-4 short strips/cards.
- Build each narrative strip/card as its own visible frame plus inner text box.
  Do not use one large text box that visually spills across the split.
- Keep the two zones aligned to a shared top and bottom line. If either side
  needs much more height, split the slide or switch to `ARC-02` / `TBL-*`.
- Use source diagrams as structure references only. Remove source-specific
  business labels before a split pattern becomes a reusable template specimen.

## Promotion Rule

Promote in this order:

1. Reusable component rule.
2. Composition recipe in `references/composition-grammar.md`.
3. Layout ID update in `references/layout-registry.md`.
4. Optional cleaned sample slide in the V1 template, only as a specimen and
   fallback.

Do not promote a full slide just because it looks good in one source deck. First
extract the components and the reason they work.
