# dashboard/

## Purpose
This directory is reserved for the Power BI executive dashboard and its exports.

## Status
The dashboard has been **designed and specified** but **not yet built**. See the "Future Work" section in the root README.md for the roadmap.

## Directory Structure
```
dashboard/
├── powerbi/           # Reserved for .pbix source file
└── exports/           # Reserved for static image exports of dashboard pages
```

## Dashboard Specification
Full specification (data model, DAX measures, 8-page layout) is in [`docs/power_bi_dashboard_plan.md`](../docs/power_bi_dashboard_plan.md).

## Planned Dashboard Pages
| Page | Purpose |
|------|---------|
| Executive Summary | KPI cards, monthly trend, top 3 risks |
| Competitive Benchmark | Peer comparison and ranking |
| Issue Analysis | Pareto and YoY trend by issue |
| Product Deep Dive | Product-specific issue breakdown |
| Geographic | State-level complaint concentration |
| Operations | Timely response and resolution quality |
| Risk Dashboard | Risk register and severity matrix |
| Recommendations | Prioritized action plan |

## Next Steps to Build
1. Open Power BI Desktop
2. Import `data/processed/complaints_cleaned.csv`
3. Build the data model and DAX measures (per spec)
4. Create the 8 pages
5. Save the `.pbix` file to `powerbi/`
6. Export static images to `exports/`
7. Update this README

See subdirectories for their individual READMEs.
