# Text Box Fit

Use this when a slide has cards, note bars, callouts, conclusion boxes, or any visible frame that owns text.

The rule is simple: text belongs to an inner text box, not to the whole slide. If the visible frame cannot contain the sentence in both directions, change the content or layout before delivery.

## Why This Fails

PowerPoint can wrap and autofit text, but those settings only operate inside the text shape's own bounding box. They do not know that a nearby gray rectangle or card border is the intended container unless the text shape is actually sized to that inner area.

Reference basis:

- PowerPoint `WordWrap` breaks lines to fit inside the shape.
- PowerPoint `AutoSize` can resize text or shape to fit text, but it is still scoped to the shape.
- DrawingML `bodyPr wrap` uses the bounding text box, and `lIns` / `rIns` / `tIns` / `bIns` are internal text margins.
- python-pptx exposes the same model through `TextFrame.word_wrap`, `auto_size`, `fit_text()`, margins, and vertical anchors.

Common failure modes:

- A card background is narrow, but the text box is as wide as the whole row.
- The title and body are separate text boxes, but the body starts before the wrapped title has finished.
- A long Chinese sentence is pasted into a card without pre-wrapping, so it visually runs into the next card.
- The generator relies on PowerPoint autofit, but the text box itself already extends outside the visible card.
- The text is technically inside a text box, but the estimated line count exceeds its height and PowerPoint clips or overprints it.

## Generation Contract

For every framed text component, calculate the frame first, then calculate the inner text zones.

```text
frame = visible card / callout / note bar
inner = frame minus padding
heading_box = inner top band
body_box = inner remaining band
```

Default inner padding:

| Component | Horizontal Padding | Vertical Padding |
|---|---:|---:|
| Process/card grid | 0.18-0.24 in | 0.16-0.22 in |
| Light-gray conclusion bar | 0.22-0.30 in | 0.12-0.18 in |
| Small note/callout | 0.16-0.22 in | 0.12-0.18 in |
| Dense table-side evidence box | 0.12-0.18 in | 0.10-0.16 in |

The text box `x`, `y`, `w`, and `h` must be inside this inner area. Do not make the text box wider than the visible frame and hope wrapping will happen visually.

## Fit Sequence

Use this order for each card, note, or callout:

1. Put the text box inside the frame's inner area.
2. Enable wrapping or use the generator's equivalent wrapped text behavior.
3. Estimate line count at the intended font size.
4. If it does not fit, shorten the sentence first.
5. If wording cannot be shortened, increase the frame height or reduce the number of cards per row.
6. If the page becomes cramped, split the slide or switch to a table.
7. Use shrink-to-fit only for small last-mile adjustment. Do not use it to hide overloaded content.

Minimum readable sizes still apply:

- Normal body text should stay at or above `12 pt`.
- Process/card body may go to `11 pt` only when the card is dense but still readable.
- Table body may go lower only under the table rules in `references/typography.md`.

## PptxGenJS Notes

When using PptxGenJS, set the text object's geometry to the inner box:

```js
slide.addText(body, {
  x: cardX + padX,
  y: cardY + headerH + gap,
  w: cardW - 2 * padX,
  h: cardH - headerH - gap - padY,
  fontFace: "Microsoft YaHei",
  fontSize: 12.5,
  color: "111111",
  margin: 0,
  autoFit: true,
  valign: "top",
});
```

PptxGenJS documents `autoFit` as "Fit to Shape" and also supports `margin` and manual line breaks. Use those after the inner box is correct; they cannot fix a text box that already extends across neighboring cards.

## python-pptx Notes

When using python-pptx, set the shape dimensions to the inner box and then set text-frame behavior:

```python
text_frame.word_wrap = True
text_frame.margin_left = Inches(0)
text_frame.margin_right = Inches(0)
text_frame.margin_top = Inches(0)
text_frame.margin_bottom = Inches(0)
text_frame.vertical_anchor = MSO_ANCHOR.TOP
text_frame.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
```

For already-filled shapes, use `fit_text()` only after the frame dimensions are final. If `SHAPE_TO_FIT_TEXT` or shape-resizing autofit is used inside a fixed card grid, the shape can grow out of the visible layout; prefer `TEXT_TO_FIT_SHAPE` or manual shortening for cards.

## QA Rules

Treat these as defects:

- Text shape starts inside a card but extends beyond the card's left, right, top, or bottom edge.
- Text appears inside a filled background but the text box is wider or taller than that background.
- A long sentence fits only because it overlaps another card, table, screenshot, title rule, page edge, or logo.
- A card body would require body text below `11 pt` to stay inside the frame.
- A wrapped title uses the body zone and collides with body text.

Run `scripts/pptx_quality_gate.py` and inspect every slide with container/text-box-fit warnings. The helper uses heuristics; the rendered slide is the final authority.
