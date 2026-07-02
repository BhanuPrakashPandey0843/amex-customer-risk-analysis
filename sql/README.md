# sql/

## Purpose
This directory contains SQL queries that independently validate all key metrics from the Python pipeline.

## Why SQL Validation?
The Python pipeline in `src/` is the source of truth, but the SQL queries provide an independent check to ensure:
- No calculation errors in pandas code
- Metrics are consistent across different tools
- Results are transparent and auditable

## File Listing

| File | Description |
|------|-------------|
| `01_business_analysis.sql` | All SQL validation queries in one file, organized by business question |

## Query Overview
The SQL file contains 10 queries, each answering a business question:

1. Competitive volume ranking with market share
2. Amex YoY and QoQ growth
3. Pareto analysis (top issues)
4. Prepaid card outlier share
5. Timely response benchmark
6. Monetary relief rate by company
7. Issue YoY change
8. Geographic concentration (top states)
9. Rolling 3-month average trend
10. Product-issue cross-tabulation

## How to Use
1. Load `data/processed/complaints_cleaned.csv` into a SQL database (SQLite, BigQuery, Snowflake, PostgreSQL, etc.)
2. Run the queries in `01_business_analysis.sql`
3. Verify that the results match the numbers in `data/processed/eda_metrics.json` and the reports

## Note
- The SQL queries are written to be dialect-agnostic (standard SQL with CTEs and window functions)
- Minor adjustments may be needed for specific databases (e.g., date functions)
- If there's a discrepancy between Python and SQL, trust the SQL and debug the Python code
