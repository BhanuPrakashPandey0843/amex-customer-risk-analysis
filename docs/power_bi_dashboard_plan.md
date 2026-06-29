# Power BI Dashboard Implementation Plan

> Spec for building `.pbix` from computed metrics | Not included in repo (requires Power BI Desktop)

## Data Connection

- **Source:** `data/processed/complaints_cleaned.csv`
- **Refresh:** Manual or scheduled after `python src/run_pipeline.py`

## Recommended Model

```
complaints_cleaned (Fact)
├── Company (Dimension — 9 values)
├── Product (Dimension — 11 values)
├── Issue (Dimension — ~30 values)
├── State (Dimension — 51 + Not specified)
├── Date (Dimension — Complaint Year/Quarter/Month)
└── Response (Dimension — Company response to consumer)
```

## DAX Measures (Core)

```dax
Total Complaints = COUNTROWS(complaints_cleaned)

Amex Complaints = CALCULATE([Total Complaints], complaints_cleaned[Company] = "American Express")

Amex Share % = DIVIDE([Amex Complaints], [Total Complaints])

Timely Response % = DIVIDE(SUM(complaints_cleaned[Timely Response Flag]), [Total Complaints])

Monetary Relief % = DIVIDE(
    CALCULATE(COUNTROWS(complaints_cleaned),
        complaints_cleaned[Company response to consumer] = "Closed with monetary relief"),
    [Total Complaints]
)

YoY Growth Q1 = 
VAR CurrentQ1 = CALCULATE([Amex Complaints], complaints_cleaned[Complaint Quarter] = 1, complaints_cleaned[Complaint Year] = 2026)
VAR PriorQ1 = CALCULATE([Amex Complaints], complaints_cleaned[Complaint Quarter] = 1, complaints_cleaned[Complaint Year] = 2025)
RETURN DIVIDE(CurrentQ1 - PriorQ1, PriorQ1)

Pareto Cumulative % = 
VAR IssueCount = CALCULATE([Amex Complaints])
VAR TotalAmex = [Amex Complaints]
RETURN DIVIDE(RunningTotal, TotalAmex)  -- use SUMX with FILTER for running total
```

## Dashboard Pages

| Page | Visuals | Business Question |
|------|---------|-------------------|
| **Executive Summary** | 5 KPI cards, trend line, top 3 risks | What should leadership know in 10 seconds? |
| **Competitive Benchmark** | Clustered bar (volume), timely % bar | How does Amex compare? |
| **Issue Analysis** | Pareto bar + line, YoY change bar | Where to focus intervention? |
| **Product Deep Dive** | Treemap, product×issue matrix | Which products drive complaints? |
| **Geographic** | Filled map (State), top 10 bar | Where are hotspots? |
| **Operations** | Timely response, resolution donut | Response quality vs prevention? |
| **Risk Dashboard** | Risk matrix (likelihood × impact) | What are P1 risks? |
| **Recommendations** | Table with priority, timeline | What actions to take? |

## Filters (All Pages)

- Company (default: American Express)
- Date range (Year, Quarter)
- Product
- Issue

## Bookmarks

1. "Amex Focus" — filter to American Express
2. "Industry View" — all 9 companies
3. "P1 Risks Only" — filter to top 3 issue categories

## Theme

- Primary: `#006FCF` (Amex Blue)
- Secondary: `#00175A` (Navy)
- Alert: `#C41230` (Red)
- Positive: `#2E7D32` (Green)
- Font: Segoe UI

## Build Instructions

1. Open Power BI Desktop
2. Get Data → Text/CSV → `complaints_cleaned.csv`
3. Create Date table from Complaint Year/Month columns
4. Add DAX measures above
5. Build 8 pages per spec
6. Import KPI values from `eda_metrics.json` for validation
7. Cross-check totals: Amex = 13,665, Total = 196,835
