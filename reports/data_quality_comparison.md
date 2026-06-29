# Data Quality Comparison
---

## Overview
Compare dataset quality before and after cleaning.

---

## Comparison Table

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Total Rows | 196,835 | 196,835 | 0 |
| Missing Sub-issue | 9,321 (4.74%) | 0 | ✅ Imputed |
| Missing State | 1,296 (0.66%) | 0 | ✅ Imputed |
| Date Format | String | Datetime UTC | ✅ Standardized |
| Company Names | Formal | Clean | ✅ Standardized |
| Complaint IDs | Unique | Unique | ✅ Preserved |
| New Features | 0 | 9 | ✅ Added |

---

## Quality Score Change
- Before: 7.5/10
- After: 8.5/10
- Improvement: +1.0 (13%)
