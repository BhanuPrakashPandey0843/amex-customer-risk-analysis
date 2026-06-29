# Column Criticality Matrix
---

## Overview
Documenting business purpose, usage, and criticality of each field in the CFPB dataset.

---

## Criticality Levels
- **CRITICAL**: Required for core analysis; high risk if missing/incorrect
- **HIGH**: Important for analysis; medium risk if missing/incorrect
- **MEDIUM**: Useful but not essential; low risk if missing
- **LOW**: Optional; no significant risk if missing

---

## Criticality Matrix

| Column | Business Purpose | Used In | Business Question Addressed | Priority | Risk if Missing/Incorrect | Recommended Action |
|--------|------------------|---------|----------------------------|----------|--------------------------|-------------------|
| **Complaint ID** | Unique record identifier | All phases | N/A (technical key) | CRITICAL | Complete loss of record traceability | Keep as-is |
| **Date received** | Complaint timestamp | Trend analysis | How are complaint volumes changing over time? | CRITICAL | Cannot perform time-based analysis | Parse to datetime |
| **Company** | Financial institution | Benchmarking | How does American Express compare to competitors? | CRITICAL | Cannot perform competitor analysis | Standardize names |
| **Product** | Financial product category | Product analysis | Which products have highest complaints? | CRITICAL | Cannot segment by product | Standardize categories |
| **Issue** | Complaint category | Issue analysis | What are the top complaint drivers? | CRITICAL | Cannot identify problem areas | Standardize categories |
| **Company response to consumer** | Resolution type | Effectiveness | How effective are complaint resolutions? | HIGH | Cannot assess response quality | Standardize categories |
| **Timely response?** | Response timeliness | Operations | Are responses timely? | HIGH | Cannot measure response performance | Convert to boolean |
| **Sub-product** | Product detail | Granular product analysis | Which specific sub-products drive complaints? | HIGH | Less granular product insights | Standardize categories |
| **State** | Complainant location | Geographic analysis | Are there regional patterns? | MEDIUM | Cannot analyze geographic trends | Standardize 2-letter codes |
| **ZIP code** | Complainant location | Detailed geographic analysis | Can we identify local trends? | MEDIUM | Cannot do ZIP-level analysis | Keep as-is |
| **Submitted via** | Complaint channel | Channel analysis | Which channels drive complaints? | MEDIUM | Cannot analyze channel trends | Standardize categories |
| **Sub-issue** | Issue detail | Granular issue analysis | What specific issues drive complaints? | MEDIUM | Less granular issue insights | Impute missing with "Not specified" |
| **Company public response** | Public statement | Transparency | How do companies communicate publicly? | LOW | Limited impact on core analysis | Keep as-is, document limitation |

---

## Summary
- **CRITICAL**: 6 fields
- **HIGH**: 3 fields
- **MEDIUM**: 4 fields
- **LOW**: 1 field
