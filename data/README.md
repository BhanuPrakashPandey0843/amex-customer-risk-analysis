# data/

## Purpose
This directory contains all data artifacts for the American Express CFPB Risk Intelligence project: raw source data, cleaned/processed data, computed metrics, and the designed executive presentation.

## Directory Structure
```
data/
├── raw/                # Immutable raw CFPB source data
├── processed/          # Cleaned data + computed metrics
├── external/           # Reserved for future external data (card base, etc.)
└── ppt/                # Designed executive presentation (source images)
```

## Data Governance Principles
1. **Immutability**: Raw data in `raw/` is never modified
2. **Traceability**: Every processed artifact comes from raw data via documented pipelines
3. **Reproducibility**: All transformed data can be regenerated from raw data via `src/run_pipeline.py`
4. **Documentation**: Every directory and file has a clear purpose documented

## Data Flow
```
raw/ → src/data_cleaning.py → processed/complaints_cleaned.csv
processed/complaints_cleaned.csv → src/metrics_engine.py → processed/eda_metrics.json
processed/eda_metrics.json → reports/, charts/, Excel, PDF
```

## Key Files

### Raw Data
| File | Description |
|------|-------------|
| `raw/CFPB Complaints Data - Jan25 to Mar26.xlsx` | Original dataset from the assignment, Jan 2025 – Mar 2026 |

### Processed Data
| File | Description |
|------|-------------|
| `processed/complaints_cleaned.csv` | Analysis-ready cleaned dataset (196,835 rows, 22 columns) |
| `processed/eda_metrics.json` | Single source of truth for all computed metrics, insights, risks, recommendations |
| `processed/audit_summary.csv` | Summary of the initial data audit |
| `processed/cleaning_log.csv` | Log of all data cleaning transformations |
| `processed/metadata_summary.csv` | Metadata about the dataset |
| `processed/missing_values_analysis.csv` | Missing values breakdown per column |
| `processed/quality_scores.csv` | Data quality scores pre- and post-cleaning |

### Presentation
| File | Description |
|------|-------------|
| `ppt/1.jpg`–`5.jpg` | Designed executive presentation (see `ppt/README.md` for details) |

## Reserved for Future Use
- `external/`: For card base/customer count data to normalize complaint volumes (see `external/README.md`)

## Important Notes
- Never modify files in `raw/`
- If you re-run the pipeline, files in `processed/` may be overwritten
- `eda_metrics.json` is the single source of truth for all numbers in reports and visualizations
