# data/external/

## Purpose

This directory is **intentionally empty** and reserved for one specific future input: **card-base / customer-count data per institution**, which would allow complaint volumes to be normalized on a per-capita basis (e.g., complaints per 100,000 cardholders) instead of raw counts.

## Why this matters

Every report in this project (`reports/executive_limitations.md`, `reports/data_governance.md`) discloses the same limitation: CFPB complaint *volume* is not the same as *market share* or *complaint rate*. American Express's 6.9% complaint share could mean either:

1. Amex genuinely generates fewer complaints per customer than peers, or
2. Amex simply has a smaller card base than Capital One, Chase, or Bank of America, and a smaller base will produce fewer raw complaints regardless of underlying quality.

The current dataset (`data/raw/`) contains no customer-count or card-base figures, so this ambiguity **cannot be resolved with the data on hand**. It is documented as a known limitation rather than silently assumed away.

## What would go here

If sourced in a future iteration, this directory would hold:

| File | Source | Purpose |
|------|--------|---------|
| `card_base_by_issuer.csv` | Public 10-K filings / Nilson Report / S&P Global Market Intelligence | Active card counts per institution, by year |
| `industry_complaint_benchmarks.csv` | CFPB aggregate statistics or trade association data | Industry-wide complaint rate baselines for context |

## Status

**Not populated.** No external data has been sourced or added. This README exists so the empty directory's purpose is documented rather than ambiguous, and so it is preserved in version control (Git does not track empty directories by default).
