# Methodology

> How the conclusions in this repository were produced, end to end — from raw CFPB export to executive PDF. For *what* was asked, see [`problem_statement.md`](problem_statement.md) and [`business_question.md`](business_question.md). For a visual trace of every file dependency described below, see [`project_dependency_map.md`](project_dependency_map.md).

## Design Principle

**Every number in every report and chart is computed once, in one place, and reused everywhere.** `src/metrics_engine.py` calculates a single `Findings` object from the cleaned dataset; that object is the only source for the markdown reports (`src/build_reports.py`), the Excel workbook (`src/build_excel.py`), the charts (`src/charts.py`), and the executive PDF (`src/executive_analysis.py`). Nothing downstream recomputes a number independently. This matters because it makes the project's biggest risk — *a stated number that doesn't match the underlying data* — structurally hard to introduce. If a figure is wrong, it's wrong in exactly one function, and fixing it there fixes it everywhere.

`sql/01_business_analysis.sql` independently re-derives the core metrics in SQL as a cross-check against the Python pipeline, rather than serving the pipeline.

## Phase-by-Phase Process

### 1. Data Audit (`notebooks/01_data_audit.ipynb`, `src/data_audit.py`)

Before any cleaning, the raw 196,835-row, 13-column extract was profiled for: row/column counts, date range, missing values by column, duplicate detection, and cardinality of categorical fields (companies, products, issues). This produced `reports/raw_data_profile.md`, `reports/metadata_report.md`, and `reports/data_quality_report.md` (baseline score: **7.5 / 10**, driven down primarily by a 44.86% missing rate on "Company public response" and the date field being stored as a string).

The audit phase exists to make sure cleaning decisions are evidence-based rather than assumed — for example, the decision *not* to drop or impute "Company public response" was made because the missingness pattern (a company simply choosing not to issue a public response) is informative, not random noise.

### 2. Data Cleaning (`notebooks/02_data_cleaning.ipynb`, `src/data_cleaning.py`)

- Parsed "Date received" from string to timezone-aware datetime (UTC)
- Standardized company name formatting for readability (e.g., consistent capitalization/legal-suffix handling)
- Handled missing values per-column based on the audit findings, documented in `reports/cleaning_report.md`
- Added **9 engineered features** (13 → 22 columns), including complaint year/quarter/month derived from the parsed date, used throughout the analytics layer for time-series and YoY/QoQ calculations

Result: **0 rows removed** — every record from the raw extract is preserved in `data/processed/complaints_cleaned.csv`. Post-cleaning quality score: **8.5 / 10** (+1.0), documented in `reports/quality_scoring_methodology.md`.

### 3. Exploratory Data Analysis (`notebooks/03_eda.ipynb`)

Foundational, business-question-framed EDA: total volume and trend, Amex-specific product/issue profile, competitor volume ranking, and timely-response/resolution-type breakdown by company. This phase establishes the descriptive baseline that later phases build on — it deliberately stops short of interpretation or recommendation, per the EDA discipline described in the project's phase plan (Phase 4: "discover patterns without making business conclusions").

### 4–5. Advanced Business Analytics (`notebooks/04_competitor_benchmarking.ipynb`, `05_customer_journey_analysis.ipynb`, `06_advanced_analytics.ipynb`)

This is where descriptive analytics becomes business intelligence:

- **Competitive benchmarking**: complaint volume, issue mix, and response-quality comparison across all 9 institutions in the dataset, ranking Amex on each dimension rather than reporting it in isolation
- **Customer journey mapping**: complaints categorized against the stage of the customer lifecycle they most plausibly originate from (acquisition, onboarding, account servicing, dispute resolution, account closure), using issue/sub-issue text as the mapping key
- **Pareto analysis**: identifying which 20% of issue categories account for 80%+ of complaint volume — the basis for "surgical intervention" framing in the recommendations
- **Regulatory exposure mapping**: each issue category mapped to the regulatory framework it falls under (FCRA, FDCPA/UDAAP, Reg Z/FCBA) per the `REGULATORY_ISSUES` dictionary in `src/metrics_engine.py`, so complaint counts can be read alongside regulatory stakes, not just volume
- **YoY / QoQ decomposition**: Q1 2025 vs. Q1 2026 comparison at both the aggregate and per-issue level, distinguishing issues that are growing from those that are flat or declining

### 6. Enterprise Risk Framework (`notebooks/07_risk_framework.ipynb`)

A standard Likelihood × Impact risk matrix (1–5 scale each dimension) applied to the issues surfaced in the prior phase. Each risk in `reports/risk_register.md` carries: likelihood, impact, derived severity, business area, mapped regulatory framework, supporting evidence (a specific complaint count, not a description), a named executive owner, a mitigation action, and a priority tier (P1/P2). Severity scoring follows the weighted composite formula documented in `reports/executive_kpis.md` ("Issue Severity Index").

### 7. Strategic Insights & Recommendations (`notebooks/08_executive_insights.ipynb`)

The synthesis layer. Every insight in `reports/insights_register.md` follows a fixed structure — **Observation → Evidence → Business Impact → Recommendation → Expected Outcome → Priority** — so that no insight exists without a corresponding action and no action exists without a quantified trigger. The 4 recommendations in `reports/recommendations.md` extend this further with root cause, effort estimate, a measurable KPI target, an identified execution risk, a mitigation for that risk, and a timeline. This structure was a deliberate choice over a looser "key findings" bullet list — it forces every claim to answer "so what should leadership do, and how will we know it worked."

### 8. Business Intelligence Dashboard (`dashboard/`)

Specified in full in `docs/power_bi_dashboard_plan.md` (data model, DAX measures, 8-page layout). **Not yet built** — this is the one deliverable in the repository that is genuinely incomplete, not just under-documented; see `dashboard/powerbi/README.md` for why and what's needed to finish it.

### 9. Executive Storytelling (`data/ppt/` — submission; `src/executive_analysis.py` → `reports/executive_presentation.pdf` — data-validation companion)

The final submission is the 5-slide designed deck in `data/ppt/` (cover, agenda, 2 content slides, closing) — built with Amex-blue branding, separately from this Python pipeline. `src/executive_analysis.py` generates a second, matplotlib-based deck (`reports/executive_presentation.pdf`) directly from `eda_metrics.json`; its purpose is not to compete with the designed deck but to provide an automated cross-check that every number on the designed slides matches the pipeline's output exactly, since it cannot drift from the computed metrics the way a manually-built deck can. See `data/ppt/README.md` for the designed deck's status.

The 2-content-slide constraint from the assignment brief was treated as a forcing function, not a limitation: it required compressing 6 insights and 5 risks down to the 3 that matter most. Both decks' slide titles state the conclusion, not the topic (e.g., *"Three P1 Actions Can Reduce 53% of Complaints..."* rather than *"Recommendations"*), following a consulting-deck convention where the headline carries the argument and the body carries the evidence.

### 10. Quality Assurance (`docs/project_audit.md`)

A self-audit was performed against the assignment's own evaluation criteria (analytical approach, insight quality, recommendations, risk identification, storytelling, clarity) before submission. This audit is what originally caught several of the gaps fixed in this documentation pass — it is kept in the repository deliberately, including the parts that were critical of earlier drafts, because a hiring reviewer auditing the same repository should reach the same conclusions independently.

## Tooling

| Layer | Tool | Why |
|---|---|---|
| Data manipulation | pandas, NumPy | Standard for tabular data at this scale (196,835 rows fits comfortably in memory) |
| Charts | matplotlib | Full control over consulting-style chart annotation (cumulative lines, threshold markers, direct value labels) — chosen over seaborn defaults for that reason |
| Excel | openpyxl | Programmatic workbook generation with styling, needed to keep the 8-sheet workbook in sync with `eda_metrics.json` automatically rather than built by hand |
| PDF | matplotlib `PdfPages` | Keeps the executive deck's charts pixel-identical to the appendix charts, generated from the same chart-rendering code |
| SQL | Plain SQL (CTEs, window functions) | Independent verification path — see `sql/01_business_analysis.sql` |
| Notebooks | Jupyter | Methodology documentation and step-by-step reasoning trail, not the execution path (see below) |

## A Disclosed Limitation: Notebooks Are Documentation, Not the Execution Path

The notebooks in `notebooks/` are not executed and re-run as part of producing the deliverables — `src/run_pipeline.py` is. This is a deliberate, disclosed tradeoff (see `docs/project_audit.md`, item 2): the notebooks exist to make the *reasoning* inspectable step-by-step in a familiar format, while the actual numbers are guaranteed reproducible by running one script. Treating the notebooks as the source of truth would risk the classic failure mode of analytics projects — a notebook that was run once, edited afterward, and never re-run, silently drifting from the numbers it claims to produce. `run_pipeline.py` cannot drift in that way, because every report depends on its output being current.

## Reproducing This Analysis

```powershell
pip install -r requirements.txt
python src/run_pipeline.py
```

This single command regenerates `data/processed/eda_metrics.json`, all 9 charts, 5 computed markdown reports, the Excel workbook, and the PDF — in that order, with each step depending only on the output of the step before it (see `docs/project_dependency_map.md` for the full dependency graph).
