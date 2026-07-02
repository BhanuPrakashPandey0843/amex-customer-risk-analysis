# Executive Summary — Project Overview

> **Note on scope:** this document summarizes the *project* — what it is, what it demonstrates, and how to navigate it — for a reviewer (hiring manager, recruiter) opening this repository for the first time. For the *business* findings written for an American Express leadership audience, see [`reports/executive_summary.md`](../reports/executive_summary.md). For the formal submission deck, see [`data/ppt/`](../data/ppt/) (5-slide designed deck — the confirmed submission; see `data/ppt/README.md` for its compile-to-PDF status). `reports/executive_presentation.pdf` is a data-validation companion auto-generated from the same numbers, not a separate submission.

## What This Is

A response to a Data Analytics Apprentice assessment (full brief: [`assignment_brief.md`](assignment_brief.md)) that analyzes 196,835 CFPB consumer complaints filed against American Express and 8 competitors (Jan 2025 – Mar 2026), structured as a full analytics engagement rather than a single notebook: data audit → cleaning → EDA → competitive/risk analytics → strategic synthesis → executive deliverable.

## Headline Business Finding

American Express ranks 7th of 9 institutions on raw complaint volume (6.9% share) — a favorable relative position — but that position is **deteriorating** (+16.4% YoY) and is concentrated in three specific, addressable failure points: credit reporting accuracy, billing dispute resolution, and a 78% industry-share outlier in prepaid card usability. The full reasoning chain from data to recommendation is in [`reports/executive_summary.md`](../reports/executive_summary.md).

## What This Project Demonstrates

| Capability | Evidence |
|---|---|
| Reproducible engineering, not one-off scripts | `python src/run_pipeline.py` regenerates every deliverable from raw data in one command |
| Traceable claims | Every insight in `reports/insights_register.md` cites a specific computed figure, not a description |
| Self-critical review | `docs/project_audit.md` is a self-audit that found and fixed real gaps — kept in the repo unedited, including the critical parts |
| Honest disclosure of limitations | `reports/executive_limitations.md` states explicitly what this dataset *cannot* support, not just what it can |
| Multiple deliverable formats from one source of truth | Markdown reports, Excel workbook, SQL queries, and PDF all derive from the same `eda_metrics.json` — see `docs/methodology.md` |

## How to Verify the Numbers Yourself

1. Run `python src/run_pipeline.py` — regenerates `data/processed/eda_metrics.json`, all charts, all 5 computed reports, the Excel workbook, and the PDF
2. Spot-check any figure against `sql/01_business_analysis.sql`, which re-derives the same metrics independently in SQL
3. Open `reports/CFPB_Executive_Analytics.xlsx` to see the underlying cross-tabs (e.g., the Product × Issue matrix) that the headline numbers are aggregated from

## Where to Start Reading

- **2 minutes:** `data/ppt/` (the actual submission deck) or `reports/executive_presentation.pdf` (data-validation companion)
- **10 minutes:** `reports/executive_summary.md` + `reports/recommendations.md` + `reports/risk_register.md`
- **30 minutes, full methodology:** `docs/methodology.md`, then walk `notebooks/01` → `08` in order
- **Auditing the project itself:** `docs/project_audit.md` and `docs/project_dependency_map.md`
