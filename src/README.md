# src/

## Purpose
This directory contains production-grade Python modules that orchestrate the entire analysis pipeline end-to-end.

## Architecture Principle
**Single Source of Truth**: Every number in the final deliverables comes from exactly one place: `metrics_engine.py`'s `compute_findings()` function. No downstream module recomputes any metric independently. This ensures consistency and makes bugs easy to track down.

## Module Listing

| Module | Purpose | Key Functions/Classes |
|--------|---------|------------------------|
| `config.py` | Centralized configuration | Paths to data directories, constants (e.g., company name mappings) |
| `data_audit.py` | Data quality audit functions | Profiling, missing value analysis, duplicate detection |
| `data_cleaning.py` | Data cleaning and feature engineering | `clean_dataset()`, feature engineering functions |
| `metrics_engine.py` | **Critical**: Computes all business metrics | `compute_findings()`, `Findings` dataclass |
| `analytics.py` | Orchestrates EDA and chart generation | `run_eda()` returns findings + chart objects |
| `charts.py` | Matplotlib chart generation | Functions for each of the 9 publication-quality charts |
| `build_reports.py` | Generates Markdown reports | Builds all reports from `Findings` object |
| `build_excel.py` | Generates Excel workbook | Creates the 8-sheet executive Excel file |
| `executive_analysis.py` | Generates PDF presentation | Builds the matplotlib-based validation deck |
| `validate_metrics.py` | (Reserved) | Placeholder for future validation logic |
| `run_pipeline.py` | **Pipeline entrypoint** | `main()` runs the entire pipeline end-to-end |

## Pipeline Flow
```
run_pipeline.py
├─ analytics.run_eda()
│  ├─ metrics_engine.compute_findings()
│  └─ charts (generates 9 PNGs)
├─ build_reports (generates 30+ Markdown files)
├─ build_excel (generates Excel workbook)
└─ executive_analysis (generates PDF)
```

## How to Run
Execute the full pipeline with one command:
```bash
python src/run_pipeline.py
```

## Coding Standards
- **Type hints**: All functions have type annotations
- **Docstrings**: Every module, class, and function has docstrings
- **Modularity**: Each module does one thing well
- **No side effects**: Functions are pure where possible, with explicit inputs/outputs
- **Logging**: Clear progress reporting during pipeline execution
