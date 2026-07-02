# data/raw/

## Purpose
This directory contains the **immutable raw source data** from the Consumer Financial Protection Bureau (CFPB) that the assignment provided.

## Immutability
**DO NOT MODIFY ANY FILES IN THIS DIRECTORY.
- The raw data is preserved exactly as received to ensure reproducibility and auditability. All transformations are applied in `src/data_cleaning.py` and applied to create `data/processed/`, never here.

## File Listing

| File | Description |
|------|-------------|
| `CFPB Complaints Data - Jan25 to Mar26.xlsx` | Original dataset containing 196,835 consumer complaints about 9 financial institutions (including American Express), January 2025 – March 2026 |

## Dataset Overview
- **Total Records**: 196,835
- **Companies**: 9 (American Express, Bank of America, Barclays, Capital One, Citibank, JPMorgan Chase, Synchrony Financial, U.S. Bank, Wells Fargo)
- **Time Period**: January 1, 2025 – March 31, 2026
- **Raw Columns**: ~13 fields (Product, Issue, Company, State, Timely Response, etc.)

## Data Dictionary
For full schema documentation, see:
- [`reports/data_dictionary.md`](../../reports/data_dictionary.md)
- [`reports/raw_data_profile.md`](../../reports/raw_data_profile.md)

## Data Quality (Raw)
- **Overall Score**: 7.5/10
- **Primary Issues**:
  - 44.86% missing values in "Company public response"
  - Date fields stored as strings instead of datetime
  - Inconsistent company name formatting
- Full details: [`reports/data_quality_report.md`](../../reports/data_quality_report.md)
