# dashboard/exports/

## Purpose

Static image exports of each Power BI dashboard page, for reviewers who don't have Power BI Desktop installed and want to see the dashboard without opening the `.pbix` file.

## Status: Not yet populated

This directory is empty because the source dashboard (`dashboard/powerbi/`) has not been built yet — see that folder's README for why. There is nothing to export until the `.pbix` exists.

## What goes here once the dashboard is built

| File | Description |
|------|--------------|
| `01_executive_summary.png` | Executive Summary page — KPI cards, trend line, top 3 risks |
| `02_competitive_benchmark.png` | Competitive Benchmark page |
| `03_issue_analysis.png` | Issue Analysis page — Pareto + YoY |
| `04_product_deep_dive.png` | Product Deep Dive page |
| `05_geographic.png` | Geographic page |
| `06_operations.png` | Operations page |
| `07_risk_dashboard.png` | Risk Dashboard page |
| `08_recommendations.png` | Recommendations page |

Page list and visual specs: [`docs/power_bi_dashboard_plan.md`](../../docs/power_bi_dashboard_plan.md).

## How to export

In Power BI Desktop: File → Export → Export to PDF, then convert each page to PNG, or use the Power BI "Copy as image" option on each page's right-click menu. Name the files per the table above so they sort correctly in a file browser.
