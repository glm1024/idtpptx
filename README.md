# idtpptx

`idtpptx` is an overlay skill for creating and editing practical IDT/Inspur-style PowerPoint decks.

It depends on the mature `pptx` skill for PPTX file operations. This skill adds company-specific style, template selection, layout mapping, writing guidance, and QA rules.

## Install

Install the base `pptx` skill first:

```bash
npx skills add anthropics/skills@pptx -g -y
```

Then install `idtpptx`:

```bash
npx skills add https://github.com/glm1024/idtpptx -g -y
```

## Use

Example prompts:

```text
Use idtpptx style to create a project report PPT from this outline.
```

```text
用 idtpptx 风格帮我做一份内部培训 PPT。
```

## What This Skill Provides

- A cleaned company-style PPTX template in `assets/templates/`
- Practical white-and-blue corporate visual rules
- Reusable page-type mapping for covers, section dividers, tables, screenshot walkthroughs, recommendations, and FAQ pages
- Chinese internal-document writing guidance
- Company-specific QA checks for placeholder cleanup, logo/layout consistency, and screenshot readability

## Notes

- `idtpptx` does not replace the base `pptx` skill.
- The base `pptx` skill handles reading, unpacking, slide duplication, XML editing, packing, rendering, and general PPTX QA.
- The bundled template may include company brand elements. Use it only in authorized contexts.
