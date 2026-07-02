# Business Questions

> Companion to [`problem_statement.md`](problem_statement.md). The problem statement establishes *why* this analysis exists; this document breaks it into the specific, answerable questions the pipeline was built to resolve. Every question below is answered with a cited number, not a generality — see the "Answered in" column.

## Primary Questions (Senior Leadership)

| # | Question | Answered in | Headline Answer |
|---|---|---|---|
| Q1 | How does American Express's CFPB complaint volume compare to its top 8 competitors? | `reports/competitive_scorecard.md`, `reports/charts/01_competitive_volume.png` | Rank 7 of 9, 6.9% share — below the peer average |
| Q2 | Is Amex's complaint trajectory improving or worsening? | `reports/executive_summary.md`, `reports/charts/02_amex_monthly_trend.png` | Worsening: +16.4% YoY (Q1 2025 → Q1 2026) |
| Q3 | Which specific issues drive the majority of Amex complaints? | `reports/eda_summary.md`, `reports/charts/03_pareto_issues.png` | Top 5 issues = 53% of all Amex complaints (Pareto concentration) |
| Q4 | Does Amex have any product-level outlier that peers don't share? | `reports/charts/04_prepaid_outlier.png` | Yes — Prepaid card "trouble using card" complaints: Amex holds 78% of the *entire industry's* volume in this category |
| Q5 | Is Amex's complaint volume growth broad-based or concentrated in specific issues? | `reports/insights_register.md` (INS-004) | Concentrated — Credit Reporting and Prepaid are the fastest-growing categories; not a uniform increase across all issues |
| Q6 | Where is Amex's complaint volume regulatorily exposed (vs. merely an experience issue)? | `reports/charts/08_regulatory_exposure.png` | FCRA-mapped issues (credit reporting) account for 3,236 complaints — the single largest regulatory category |
| Q7 | Is Amex's response *quality* (not just speed) competitive? | `reports/executive_kpis.md`, `reports/charts/06_timely_benchmark.png` | Timely response is already near-ceiling (99.0%, rank 8/9 — the gap to peers is marginal); resolution quality (73% closed with explanation) is a relative strength worth protecting, not fixing |
| Q8 | Where geographically are complaints concentrated? | `reports/charts/07_top_states.png` | CA, FL, and NY together account for roughly a third of Amex complaint volume |
| Q9 | What should leadership do, specifically? | `reports/recommendations.md` | 3 P1 actions (credit reporting reconciliation, billing dispute triage, prepaid task force) + 1 P2 (executive monitoring dashboard) |
| Q10 | What could go wrong if no action is taken? | `reports/risk_register.md` | 5 enterprise risks, 3 rated Critical severity, all with named owners and mitigation steps |

## Secondary / Supporting Questions

These don't appear on the 2-slide executive presentation (per the assignment's slide-count constraint) but were answered to support the primary questions above and are documented in the appendix charts and full report set:

- How does resolution type (closed with relief / closed with explanation / closed without relief) vary by issue category? → `reports/competitor_benchmark.md`
- Which Amex products drive which issues — is it concentrated in 1–2 products or spread across the portfolio? → `reports/charts/09_product_clusters.png`
- How does Amex's monetary relief rate compare to the peer average? → `eda_metrics.json` → `peer_benchmark_kpis`
- What does the quarter-over-quarter (not just year-over-year) trend look like, to catch more recent inflection points? → `eda_metrics.json` → `qoq_q4_to_q1_pct`

## Questions Deliberately Not Asked

Per `reports/executive_limitations.md`, this dataset cannot reliably answer (and so these were not pursued):
- "What is Amex's true market share of complaints, normalized by customer base?" — no card-base data available (tracked in `data/external/README.md`)
- "Will complaint volume continue rising next quarter?" — 15 months of data and no predictive modeling per assignment scope
- "What specific internal process failure caused each complaint?" — no operational or case-narrative data in the CFPB extract

## How These Map to the Project Phases

Questions Q1–Q2 were answered in the EDA phase (`notebooks/03_eda.ipynb`). Q3–Q6 required the advanced analytics layer (issue concentration, YoY decomposition, regulatory mapping — `notebooks/06_advanced_analytics.ipynb`). Q9–Q10 are the strategic synthesis layer (`notebooks/08_executive_insights.ipynb`, `reports/recommendations.md`, `reports/risk_register.md`).
