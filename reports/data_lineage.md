# Data Lineage Report
---

## Overview
Data lineage for the American Express CFPB Risk Intelligence Analysis project.

---

## Lineage Flow

```
CFPB Consumer Complaint Database
(Regulatory Source)
    ↓
Raw Data File: CFPB Complaints Data - Jan25 to Mar26.xlsx
(Stored in: data/raw/)
    ↓
Phase 3: Data Audit
(Validation & Quality Assessment)
Outputs: audit reports, data dictionary, quality scores
    ↓
Phase 4: Data Cleaning
(Planned Transformations)
• Date parsing & standardization
• Missing value handling
• Categorical standardization
• Outlier detection
    ↓
Clean Data File
(Planned: data/processed/clean_complaints.csv)
    ↓
Phase 5: Exploratory Data Analysis (EDA)
(Planned)
• Volume trends
• Product breakdown
• Company comparisons
• Issue categorization
    ↓
Phase 6: Advanced Analytics
(Planned)
• Risk scoring
• Competitor benchmarking
• Customer journey mapping
    ↓
Analytical Datasets
(Planned: risk_scores.csv, benchmarking.csv)
    ↓
Phase 7: Power BI Dashboard
(Planned)
Executive KPIs
Complaint trends
Competitive position
Risk profile
    ↓
Phase 8: Executive Presentation
(Final Deliverable)
2-slide executive deck
PDF format
```

---

## Transformation Details

### Phase 3 — Audit (Completed)
| Column | Transformation | Rationale |
|--------|---------------|-----------|
| (None) | Raw data only | No cleaning during audit phase |

### Phase 4 — Planned Cleaning
| Column | Planned Transformation |
|--------|----------------------|
| Date received | Convert to datetime UTC, extract month/quarter/year |
| State | Standardize to 2-letter codes |
| Sub-issue | Impute missing with "Not specified" |
| Company public response | Keep as-is, document limitation |
| All categoricals | Standardize whitespace/formatting |
| Complaint ID | Keep as primary key |

---

## Traceability
All outputs will link back to raw data via:
- Reproducible notebooks
- Documented code
- Audit trails
- Version control in GitHub
