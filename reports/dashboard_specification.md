# Power BI Dashboard Specification

## Date Prepared
June 27, 2026 — Revised June 29, 2026

## Overview

This document is the **page-by-page visual specification** for the American Express CFPB Risk Intelligence Power BI Dashboard — what each page shows, exactly which visual type, and what interaction it supports. For the underlying data model, DAX measures, and build instructions, see [`docs/power_bi_dashboard_plan.md`](../docs/power_bi_dashboard_plan.md), which this document complements rather than repeats.

**Status:** Specification complete; `.pbix` not yet built — see [`dashboard/powerbi/README.md`](../dashboard/powerbi/README.md).

## Page-by-Page Visual Specification

### Page 1 — Executive Summary
| Element | Visual Type | Fields / Measure |
|---|---|---|
| Headline KPI row | 5 card visuals | Total Complaints, Amex Share %, YoY Growth %, Top-5 Issue Concentration %, Prepaid Outlier % |
| Trend | Line chart | Monthly complaint count, Amex vs. peer average, conditional color (red if YoY > 0) |
| Top 3 risks | Table, sorted by Severity descending | Risk ID, Risk Name, Severity, Owner — pulled from `risk_register.md` rows |
| Filter context | Slicer (collapsed by default) | Date range |

### Page 2 — Competitive Benchmark
| Element | Visual Type | Fields / Measure |
|---|---|---|
| Volume by institution | Clustered horizontal bar | Company on Y-axis, Complaint count on X-axis, Amex highlighted in brand blue (`#006FCF`), peers in gray |
| Timely response benchmark | Horizontal bar, axis truncated to 97.5–100% | Forces visual separation despite all institutions clustering near-ceiling |
| Drill-through | Right-click on any company bar | Filters Page 3 (Issue Analysis) to that company |

### Page 3 — Issue Analysis
| Element | Visual Type | Fields / Measure |
|---|---|---|
| Pareto | Combo chart: bar + line | Bars = issue count, line = cumulative %, reference line at 80% |
| YoY change by issue | Diverging horizontal bar | Red = growing YoY, green = declining YoY, sorted by magnitude |
| Filter | Issue category slicer | Multi-select |

### Page 4 — Product Deep Dive
| Element | Visual Type | Fields / Measure |
|---|---|---|
| Product × Issue matrix | Matrix visual with heatmap conditional formatting | Top 5 products × top 8 issues, cell color intensity = complaint count |
| Product share | Treemap | Product on hierarchy, size = complaint count |

### Page 5 — Geographic
| Element | Visual Type | Fields / Measure |
|---|---|---|
| State concentration | Filled map | State field, color saturation = complaint count |
| Top 10 states | Horizontal bar | Ranked, with % of total Amex volume labeled |

### Page 6 — Operations
| Element | Visual Type | Fields / Measure |
|---|---|---|
| Resolution mix | Donut chart | Closed with relief / closed with explanation / closed without relief |
| Timely response trend | Line chart | Monthly timely % vs. 95% internal target reference line |

### Page 7 — Risk Dashboard
| Element | Visual Type | Fields / Measure |
|---|---|---|
| Risk matrix | Scatter plot | X = Likelihood (1–5), Y = Impact (1–5), bubble size = complaint count, color = priority tier |
| Risk register | Table | Full `risk_register.md` content, sortable by severity |

### Page 8 — Recommendations
| Element | Visual Type | Fields / Measure |
|---|---|---|
| Recommendation tracker | Table with conditional icons | REC ID, Priority, Action, KPI Target, Timeline, Status (manually updated post-launch) |

## Cross-Page Behavior

- **Global filters:** Company (default = American Express), Date range, Product, Issue — apply to all 8 pages per `docs/power_bi_dashboard_plan.md`
- **Bookmarks:** "Amex Focus," "Industry View," and "P1 Risks Only," as defined in the technical plan, are accessible from a bookmark navigator on every page
- **Tooltips:** Every chart's default tooltip is replaced with a report-page tooltip showing the underlying complaint count, the comparison value (peer average or prior period), and the source issue category — so a viewer never has to leave the page to understand a data point

## Design Constraints

- Color palette and typography match `src/config.py`'s `COLORS` dictionary exactly (`#006FCF` Amex blue, `#00175A` navy, `#C41230` red, `#2E7D32` green), so the dashboard is visually consistent with the static charts in `reports/charts/` and the PDF
- No 3D visuals, no decorative icons — every visual answers one of the business questions in `docs/business_question.md`, consistent with this project's stated principle: "every visualization answers a business question"
