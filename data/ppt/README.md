# data/ppt/

## What this is

Five source images (`1.jpg`–`5.jpg`) making up a fully designed executive slide deck — cover, agenda, 2 content slides, and a closing/contact slide — built with custom American Express–blue branding (distinct from, and more visually polished than, the matplotlib-generated deck at `reports/executive_presentation.pdf`).

| File | Slide | Content |
|---|---|---|
| `1.jpg` | Cover | Title, author (Bhanu Prakash Pandey), GitHub link |
| `2.jpg` | Agenda | 6-section overview (Business Objective → Executive Conclusion) |
| `3.jpg` | Content 1 — "Objective / Scope / Outcome" | EDA summary, key insights, recommendations, and risks compressed into one info-dense slide with the monthly trend, Pareto, and product-mix charts |
| `4.jpg` | Content 2 — "Strategic Assessment" | Business impact matrix, opportunities, expected outcomes by KPI, and an executive takeaway |
| `5.jpg` | Closing | Contact details and three summary stat circles (196,835 complaints analyzed, 53% top-5 concentration, 4 strategic priorities) |

This satisfies the assignment's "maximum 2 content slides, optional cover/agenda/appendix" rule (slides 3–4 are the 2 content slides; 1, 2, and 5 are the permitted optional pages).

## Known issue

**Slide 3** (`3.jpg`) has a text-rendering overlap under the product-mix pie chart: the caption "*Three priority product clusters... drive ~83% of Amex's CFPB complaint volume*" overlaps with a duplicated, garbled fragment ("...categories shown)meh80% within the categories shown"). This looks like two text boxes were placed on top of each other in the original design file. **This needs to be fixed in the source design tool** (Canva/PowerPoint/Figma — whichever was used) and re-exported; it cannot be fixed by editing the `.jpg` directly without redoing the layout.

## Resolved: this is the submission

This deck — not `reports/executive_presentation.pdf` — is the confirmed final submission. `reports/executive_presentation.pdf` is retained as a data-validation companion (it's auto-generated from `eda_metrics.json`, so it's a useful cross-check that every number on this deck matches the pipeline), not as a competing deliverable.

## Remaining steps to finish this deliverable

1. **Fix the slide 3 overlap** in the original source design file (Canva/PowerPoint/Figma — whichever was used to build these 5 images). The garbled text sits underneath the pie-chart caption; it needs to be deleted or repositioned in the layer/text-box layer, not edited on the flattened `.jpg`.
2. **Re-export** all 5 slides as either updated images or directly as a PDF from the design tool.
3. **Compile to a single PDF** — most design tools (Canva, PowerPoint, Keynote, Figma) have a "Download as PDF" or "Export → PDF" option that combines all slides into one file in order. If only images are available, any image-to-PDF tool works, provided slide order is preserved (1 → 5).
4. **Save the result** as `reports/executive_presentation.pdf`, replacing the matplotlib-generated version, or as a new file (e.g. `reports/executive_presentation_final.pdf`) if you'd rather keep both side by side — update the root `README.md`'s Key Deliverables table to match whichever path you choose.
5. **Spot-check the numbers** on the recompiled PDF against `data/processed/eda_metrics.json` before final submission — the figures on these slides (13,665 Amex complaints, 16.4% YoY, 53% top-5 concentration, 78% prepaid outlier) were correct as of when these slides were built, but if the pipeline is re-run on updated data, they should be re-verified.
