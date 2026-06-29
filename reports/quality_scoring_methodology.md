# Quality Scoring Methodology
---

## Overview
This document defines the methodology used to calculate data quality scores for the CFPB Consumer Complaints Dataset. Scores are designed to assess fitness for executive-level decision-making.

---

## Quality Dimensions

| Dimension | Weight | Definition |
|-----------|--------|------------|
| Completeness | 40% | % of non-missing values |
| Validity | 25% | Values conform to expected formats/types |
| Uniqueness | 15% | No duplicates where uniqueness expected |
| Timeliness | 10% | Data is current for business needs |
| Consistency | 10% | Values are consistent across related fields |

---

## Calculation Formula
```
Column Score = (Completeness × 0.4) + (Validity × 0.25) + (Uniqueness × 0.15) + (Timeliness × 0.1) + (Consistency × 0.1)
```

### Scoring Scale
All scores are normalized to a **1–10 scale** where:
- 10 = Excellent (No issues)
- 7–9 = Good (Minor issues)
- 4–6 = Fair (Moderate issues)
- 1–3 = Poor (Critical issues)

---

## Dimensional Scoring Rules

### Completeness Score
- **10**: 0% missing
- **9**: <1% missing
- **7**: 1–5% missing
- **5**: 5–25% missing
- **3**: 25–50% missing
- **1**: >50% missing

### Validity Score
- **10**: All values valid
- **7**: <5% invalid
- **5**: 5–15% invalid
- **3**: >15% invalid

### Uniqueness Score
- **10**: Unique ID fields have 100% uniqueness
- **5**: Categorical fields (no uniqueness expectation)
- **7**: Text fields with expected uniqueness

### Timeliness Score
- **10**: Data covers current business period (Jan 2025–Mar 2026)
- **5**: Data is stale (>1 year old)

### Consistency Score
- **10**: All categories standardized
- **7**: Minor standardization needed
- **5**: Significant standardization needed

---

## Examples
### Complaint ID (Critical Field)
- Completeness: 10, Validity:10, Uniqueness:10, Timeliness:10, Consistency:10 → **10.0**

### Company public response
- Completeness: 5.5 (44.86% missing), Validity:10, Uniqueness:5, Timeliness:10, Consistency:10 → **7.2**

### Overall Dataset Score
Average of all column scores, weighted by business criticality.
