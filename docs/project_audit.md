# Project Audit Report

> Hiring-manager review | Generated 2026-06-27

## Overall Verdict

| Dimension | Before | After | Score |
|-----------|--------|-------|-------|
| Data pipeline | Strong cleaning code, notebooks unexecuted | Reproducible `run_pipeline.py` | ✅ |
| Analytics depth | 5 basic metrics | 9 charts, YoY, Pareto, regulatory mapping | ✅ |
| Insight quality | Static markdown | 6 structured insights with evidence chain | ✅ |
| Recommendations | Generic bullets | 4 full REC objects with KPI targets | ✅ |
| Risk register | 4 basic rows | 5 risks with likelihood/impact/owner | ✅ |
| SQL | Missing | 10 business queries with CTEs/windows | ✅ |
| Excel | Missing | 8-sheet executive workbook | ✅ |
| Power BI | Spec only | Implementation plan documented | ⚠️ |
| Presentation | Descriptive titles | Consulting-style insight titles | ✅ |
| Notebooks | Never run | Still need execution (pipeline is source of truth) | ⚠️ |

## Critical Issues Found & Fixed

### 1. Documentation without computation (CRITICAL)
**Finding:** 30+ markdown reports contained insights that were never computed from data.  
**Fix:** All 5 active reports now generated from `eda_metrics.json` via `build_reports.py`.

### 2. Notebooks never executed (HIGH)
**Finding:** All 6 notebooks have `execution_count: null`.  
**Fix:** `src/run_pipeline.py` is the reproducible execution path. Notebooks remain as documentation of methodology.

### 3. Stub notebooks 04–05 (HIGH)
**Finding:** Advanced analytics and risk framework notebooks are placeholders.  
**Fix:** Full logic implemented in `metrics_engine.py` with insights, recommendations, and risks.

### 4. Missing SQL (MEDIUM)
**Finding:** README references `sql/` folder but it didn't exist.  
**Fix:** `sql/01_business_analysis.sql` with 10 queries using CTEs, window functions, Pareto, YoY.

### 5. Missing Excel deliverable (MEDIUM)
**Finding:** Assessment allows Excel; none existed.  
**Fix:** `reports/CFPB_Executive_Analytics.xlsx` with KPI cards, pivot-style cross-tabs, risk register.

### 6. Weak presentation titles (MEDIUM)
**Finding:** Slides used descriptive titles ("Situation & Competitive Position").  
**Fix:** Insight-driven titles per consulting standard.

### 7. Unsupported impact estimates (LOW)
**Finding:** "15–25% reduction" claims lack historical baseline.  
**Status:** Retained as directional targets with explicit assumption in limitations. Not presented as computed forecasts.

### 8. No per-capita normalization (LOW — by design)
**Finding:** Volume comparisons don't adjust for card base.  
**Status:** Disclosed in every report and PDF appendix. Cannot fix without external data.

## Visualization Review

| Chart | Verdict | Action |
|-------|---------|--------|
| Competitive volume bar | Keep | Redesigned with insight title |
| Monthly trend | Keep | Added YoY annotations |
| Product pie | Redesign | Replaced with cluster-focused version |
| Top issues bar | Redesign | Replaced with Pareto + cumulative line |
| Prepaid outlier | Keep | Enhanced with industry context |
| Issue YoY | **New** | Shows which issues are growing |
| Timely benchmark | **New** | Supports "invest in prevention" insight |
| Geographic states | **New** | CA/FL/NY concentration |
| Regulatory exposure | **New** | FCRA dominance visualized |

## Assessment Rubric Compliance

| Criterion | Evidence |
|-----------|----------|
| Analytical approach | Pareto, YoY, competitive indexing, regulatory mapping |
| Quality of insights | 6 insights with Observation→Evidence→Impact→Recommendation→Outcome |
| Business recommendations | 4 REC objects with root cause, KPI target, timeline |
| Risk identification | 5-risk register with likelihood, impact, owner |
| Data storytelling | Consulting-style PDF with "SO WHAT" callouts |
| Clarity & conciseness | 2 content slides + appendix (per assessment rules) |

## Remaining Gaps (Honest)

1. **Power BI `.pbix` file** — Requires Power BI Desktop; plan documented, not built
2. **Notebook execution outputs** — Pipeline is source of truth; notebooks not re-run
3. **Raw Excel not in repo** — Likely gitignored; cleaned CSV is present
4. **Predictive modeling** — Correctly excluded per assessment instructions
