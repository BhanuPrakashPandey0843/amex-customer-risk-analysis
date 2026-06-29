# American Express CFPB Risk Intelligence Analysis
---

## Overview
An enterprise-grade analytics project analyzing consumer complaint data from the Consumer Financial Protection Bureau (CFPB) to identify strategic risks, customer experience gaps, and business opportunities for American Express.

This project simulates a consulting engagement, delivering executive-level insights, a Power BI dashboard, and a concise executive presentation.

---

## Project Objectives
- **Business Objective**: Identify strategic risks and opportunities for American Express
- **Technical Objective**: Build a reproducible, production-quality analytics pipeline
- **Learning Objective**: Demonstrate end-to-end analytics and consulting capabilities
- **Portfolio Objective**: Showcase enterprise analytics for senior roles

---

## Audience
- Senior Leadership Team
- Chief Risk Officer
- Customer Experience executives
- Product Management
- Compliance & Regulatory teams

---

## Data Source
- **Provider**: Consumer Financial Protection Bureau (CFPB)
- **Period**: January 2025 – March 2026
- **Records**: 196,835 complaints
- **Columns**: 13 fields (dates, products, issues, companies, responses)

---

## Repository Structure
```
amex-cfpb-risk-intelligence/
├── data/
│   ├── raw/                # Original CFPB dataset
│   └── processed/          # Clean data and audit outputs
├── docs/
│   ├── ai_prompt/          # Enterprise AI Operating Manuals
│   ├── problem_statement.md
│   └── methodology.md
├── notebooks/              # Jupyter notebooks (audit, analysis)
├── src/                    # Modular Python code
├── reports/                # Audit, quality, and governance reports
├── sql/                    # SQL validation scripts
└── README.md
```

---

## Project Timeline (Sprint-based)
| Sprint | Phase | Status |
|--------|-------|--------|
| 1 | Project Foundation | ✅ Complete |
| 2 | Business Understanding | ✅ Complete |
| 3 | Data Audit | ✅ Complete |
| 4 | Data Cleaning | ✅ Complete |
| 5 | Exploratory Data Analysis | ✅ Complete |
| 6 | Strategic Business Analytics & Executive Intelligence | ✅ Complete |
| 7 | Executive Storytelling | ✅ Complete |
| 8 | Power BI Dashboard | ⏳ Upcoming |
| 9 | Executive Presentation | ✅ Complete |
| 10 | Final Review | ⏳ Upcoming |

---

## Key Deliverables
1. **Executive Presentation**: 2-slide PDF (max) for leadership
2. **Power BI Dashboard**: Executive KPIs, trends, competitive benchmarking
3. **Reproducible Notebooks**: All phases documented in Jupyter
4. **Enterprise Reports**: Data audit, quality, governance, risk register, cleaning reports
5. **Modular Codebase**: Python scripts for cleaning, analysis, visualization

---

## Data Quality Score
Overall Data Quality Score: **8.5 / 10**
- Completeness: 10.0
- Validity: 9.0
- Consistency: 9.5
- Uniqueness: 8.0

---

## Technology Stack
- **Data Analysis**: Python (Pandas, NumPy)
- **Notebooks**: Jupyter
- **Visualization**: Power BI
- **Version Control**: Git
- **Repository**: GitHub

---

## Getting Started

```powershell
pip install -r requirements.txt
python src/run_pipeline.py
```

### Submission Files
| Deliverable | Path |
|-------------|------|
| **Executive PDF (submit this)** | `reports/executive_presentation.pdf` |
| Excel workbook | `reports/CFPB_Executive_Analytics.xlsx` |
| SQL analysis | `sql/01_business_analysis.sql` |
| Computed metrics | `data/processed/eda_metrics.json` |
| Executive summary | `reports/executive_summary.md` |

### Pipeline Outputs
| Output | Description |
|--------|-------------|
| 9 charts | `reports/charts/` — publication-quality PNGs |
| 5 reports | Generated from computed metrics (not templates) |
| 6 insights | Observation → Evidence → Impact → Recommendation → Outcome |
| 4 recommendations | Full REC framework with KPI targets |
| 5 risks | Likelihood, impact, owner, mitigation |

---

## Project Principles
1. Business before technology
2. Every visualization answers a business question
3. Every recommendation supported by evidence
4. Think like an executive
5. Quality over quantity

---

## Data Cleaning Summary
- **Raw Rows**: 196,835
- **Cleaned Rows**: 196,835 (0 removed)
- **New Features Added**: 9
- **Key Improvements**:
  - Dates standardized to datetime UTC
  - Company names cleaned for readability
  - Missing values systematically handled
  - 9 engineered features for deeper analysis
- **Data Quality Score**: +1.0 improvement (7.5 → 8.5)

---

## License
For educational/assessment purposes only.
