# CFPB Consumer Complaints Dataset — Data Dictionary

## Dataset Overview
- **Source**: Consumer Financial Protection Bureau (CFPB)
- **Reporting Period**: January 2025 – March 2026
- **Total Rows**: 196,835
- **Total Columns**: 13

---

## Column Metadata

| Column Name | Data Type | Business Definition | Technical Description | Business Importance | Nullable | Example Values | Recommended Usage | Expected Transformations |
|-------------|-----------|---------------------|----------------------|--------------------|----------|----------------|------------------|--------------------------|
| **Date received** | str | Date when the complaint was received by CFPB | UTC timestamp string (ISO 8601) | Critical | No | 2025-01-02T19:16:49.000Z | Trend analysis, time-based patterns | Parse to datetime, extract date components (month, quarter, year) |
| **Product** | str | Financial product category associated with complaint | Categorical string with fixed values | Critical | No | "Credit card", "Checking or savings account" | Product-level analysis | Standardize text, group into higher-level categories as needed |
| **Sub-product** | str | Specific sub-category of product | Categorical string with fixed values | High | No | "General-purpose credit card or charge card" | Granular product analysis | Standardize text |
| **Issue** | str | Primary complaint issue category | Categorical string | Critical | No | "Managing an account", "Incorrect information on your report" | Issue-level analysis, identify top issues | Standardize text |
| **Sub-issue** | str | Specific sub-category of issue | Categorical string | High | Yes | "Problem with a credit reporting company's investigation into an existing problem" | Granular issue analysis | Handle missing values, standardize text |
| **Company public response** | str | Company's public-facing response | Text field | Medium | Yes | "Company has responded to the consumer and the CFPB and chooses not to provide a public response" | Response analysis | Handle missing values, categorize responses |
| **Company** | str | Name of financial institution | Categorical string | Critical | No | "AMERICAN EXPRESS", "JPMORGAN CHASE & CO." | Competitor benchmarking | Standardize names, map to consistent company identifiers |
| **State** | str | U.S. state of complainant | Two-letter state abbreviation or full name | High | Yes | "CA", "Texas" | Geographic analysis | Handle missing values, standardize to 2-letter codes |
| **ZIP code** | object | ZIP code of complainant | String or numeric field | Medium | No | "90210", "10001" | Geographic analysis | Standardize format, validate ZIP codes |
| **Submitted via** | str | Channel through which complaint was submitted | Categorical string | Medium | No | "Web", "Phone", "Fax" | Channel analysis | Standardize text |
| **Company response to consumer** | str | How the company responded | Categorical string | Critical | No | "Closed with explanation", "Closed with monetary relief" | Response quality analysis | Standardize categories |
| **Timely response?** | str | Whether response was timely | Yes/No categorical | Critical | No | "Yes", "No" | Operational performance | Convert to boolean |
| **Complaint ID** | int64 | Unique identifier for complaint | Integer, unique for each row | Critical | No | 11355363 | Record identification, deduplication | Use as primary key |

---

## Key Observations
- No missing values in core critical columns: Date received, Product, Issue, Company, Complaint ID
- Highest missing percentage in "Company public response" (44.86%)
- Sub-issue has manageable missing rate (4.74%)
- State has minimal missing values (0.66%)
