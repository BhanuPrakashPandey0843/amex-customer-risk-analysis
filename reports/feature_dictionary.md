# Feature Dictionary
---

## Overview
Definitions of all engineered features.

---

## Engineered Features

| Feature Name | Definition | Formula | Business Purpose | Data Type | Example | Used In Later Analysis |
|--------------|------------|---------|------------------|-----------|---------|------------------------|
| Complaint Year | Year complaint received | Date received.year | Trend analysis over years | int | 2025 | EDA, Time Series |
| Complaint Quarter | Quarter complaint received | Date received.quarter | Seasonal trend analysis | int | 1 | EDA, Trends |
| Complaint Month | Month complaint received (1-12) | Date received.month | Monthly trend analysis | int | 1 | EDA, Time Series |
| Complaint Month Name | Month complaint received (name) | Date received.month_name() | Readable trend reporting | str | January | Executive Reporting |
| Complaint Week | ISO week of year | Date received.isocalendar().week | Weekly trend analysis | int | 1 | EDA |
| Complaint Day | Day of week (0=Monday, 6=Sunday) | Date received.dayofweek | Day-of-week patterns | int | 1 | EDA |
| Complaint Day Name | Day of week (name) | Date received.day_name() | Readable day-of-week reporting | str | Wednesday | Executive Reporting |
| Timely Response Flag | Binary indicator of timely response | (Timely response? == 'Yes').astype(int) | Response performance measurement | int | 1 | Dashboard, Benchmarking |
| Product Group | High-level product category | Custom mapping | Aggregated product analysis | str | Cards | EDA, Executive Insights |
