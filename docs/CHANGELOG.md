# Changelog — Elite Submission Upgrade

> Every change with reason | 2026-06-27

## New Files

| File | Reason |
|------|--------|
| `src/config.py` | Centralize paths, colors, constants — eliminates hardcoded paths |
| `src/metrics_engine.py` | All business logic in one testable module with structured Findings dataclass |
| `src/charts.py` | Separated visualization from computation; 9 publication-quality charts |
| `src/build_excel.py` | Assessment allows Excel; creates 8-sheet executive workbook |
| `sql/01_business_analysis.sql` | 10 SQL queries with CTEs, windows, Pareto, YoY — answers business questions |
| `reports/executive_summary.md` | One-page leadership brief computed from data |
| `reports/recommendations.md` | Full REC framework with root cause, KPI target, timeline |
| `reports/CFPB_Executive_Analytics.xlsx` | Executive-ready Excel with KPIs, pivots, risks |
| `docs/project_dependency_map.md` | Step 1 deliverable — traceability map |
| `docs/project_audit.md` | Step 2 deliverable — hiring-manager audit |
| `docs/power_bi_dashboard_plan.md` | Step 3 deliverable — Power BI implementation spec |
| `docs/CHANGELOG.md` | Step 12 deliverable — this file |

## Modified Files

| File | Change | Reason |
|------|--------|--------|
| `src/analytics.py` | Refactored to thin orchestrator | Modular design best practice |
| `src/build_reports.py` | Rewritten to use Findings dataclass | Reports must come from computed metrics, not templates |
| `src/executive_analysis.py` | Complete rewrite | Consulting-style insight titles; uses new charts |
| `src/run_pipeline.py` | 4-step orchestration | Single command reproduces all deliverables |
| `README.md` | Updated pipeline instructions | Clarity for reviewers |

## New Charts (9 total)

| Chart | Business Question |
|-------|-------------------|
| `01_competitive_volume.png` | How does Amex rank vs peers? |
| `02_amex_monthly_trend.png` | Is volume accelerating? |
| `03_pareto_issues.png` | Which issues drive 80% of complaints? |
| `04_prepaid_outlier.png` | Where is Amex uniquely weak? |
| `05_issue_yoy_change.png` | Which issues are growing fastest? |
| `06_timely_benchmark.png` | Should we invest in timeliness? |
| `07_top_states.png` | Where are complaints concentrated? |
| `08_regulatory_exposure.png` | What regulatory frameworks are at risk? |
| `09_product_clusters.png` | Which products drive complaints? |

## New Metrics in `eda_metrics.json`

- `issue_yoy_changes` — per-issue Q1 YoY growth
- `fastest_growing_issues` / `declining_issues`
- `amex_strengths` / `amex_weaknesses` — competitive indexing
- `monetary_relief_by_issue` — relief rate by complaint type
- `regulatory_exposure` — FCRA/FDCPA/UDAAP mapping
- `product_drivers` — top issue per product
- `peer_benchmark_kpis` — timely + monetary relief by company
- `qoq_q4_to_q1_pct` — quarter-over-quarter growth
- `recommendations` — 4 structured REC objects
- `insights` — 6 structured INS objects
- `risks` — 5 enhanced RISK objects with owner/likelihood/impact

## Presentation Changes

| Before | After |
|--------|-------|
| "Slide 1 — Situation & Competitive Position" | "Amex Holds a Volume Advantage — But Three Issue Clusters Are Accelerating Toward Regulatory Risk" |
| "Slide 2 — Priority Risks & Strategic Recommendations" | "Three P1 Actions Can Reduce 53% of Complaints and Eliminate Amex's Biggest Competitive Outlier" |
| 5 basic charts embedded | 9 charts in appendix; best 4 on content slides |
| Generic KEY INSIGHT box | "SO WHAT" consulting callout with specific numbers |

## Intentionally NOT Changed

- Raw data cleaning logic (`data_cleaning.py`) — already correct
- Data audit logic (`data_audit.py`) — already correct
- Assessment constraint of 2 content slides — preserved
- No predictive modeling — per assessment instructions
- 25+ legacy markdown reports in `reports/` — kept as archive, not regenerated
