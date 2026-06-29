# CFPB Dataset — Data Quality Report

---

## Executive Summary
The CFPB Consumer Complaints Dataset (Jan 2025 – Mar 2026) has an **Overall Quality Score of 7.5 / 10**, making it suitable for executive-level analytics with minor data cleaning and preparation.

### Key Strengths
- No duplicate rows or columns
- No empty records
- Core critical columns have 0% missing values
- Complaint ID provides unique record identification
- Clean, consistent categorical values for most columns

### Key Challenges
- Company public response is missing 44.86% of records
- Sub-issue has 4.74% missing values
- Date field is stored as string instead of datetime

---

## Quality Scores by Column

| Column | Completeness Score | Uniqueness Score | Overall Score |
|--------|-------------------|-----------------|--------------|
| Complaint ID | 10 | 10 | 10 |
| Date received | 10 | 5 | 7.5 |
| Product | 10 | 5 | 7.5 |
| Sub-product | 10 | 5 | 7.5 |
| Issue | 10 | 5 | 7.5 |
| Sub-issue | 9.5 | 5 | 7.3 |
| Company | 10 | 5 | 7.5 |
| State | 9.9 | 5 | 7.5 |
| ZIP code | 10 | 5 | 7.5 |
| Submitted via | 10 | 5 | 7.5 |
| Company response to consumer | 10 | 5 | 7.5 |
| Timely response? | 10 | 5 | 7.5 |
| Company public response | 5.5 | 5 | 5.3 |

---

## Quality Dimensions

### Completeness
- **Score**: 9.0 / 10
- **Issues**: Company public response has high missing rate
- **Risk**: Medium

### Uniqueness
- **Score**: 8.0 / 10
- **Issues**: N/A (duplicates not present)
- **Risk**: Low

### Validity
- **Score**: 8.5 / 10
- **Issues**: Date field needs type conversion
- **Risk**: Low

### Consistency
- **Score**: 8.5 / 10
- **Issues**: Categorical standardization needed
- **Risk**: Low

### Accuracy
- **Score**: 8.0 / 10
- **Issues**: Not validated externally (assumed accurate from CFPB)
- **Risk**: Low

---

## Recommendations
1. Parse "Date received" to datetime format
2. Handle missing values in "Company public response" and "Sub-issue"
3. Standardize categorical column values
4. Normalize State and ZIP code fields
5. Validate company names for consistency
