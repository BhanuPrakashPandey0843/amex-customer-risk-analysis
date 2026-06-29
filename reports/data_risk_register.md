# CFPB Dataset — Data Risk Register

---

## Risk Overview
| Risk ID | Risk Description | Likelihood | Business Impact | Technical Impact | Severity | Priority | Mitigation Strategy | Owner |
|---------|-----------------|-----------|----------------|-----------------|---------|---------|-------------------|-------|
| RISK-001 | Missing values in Company public response (44.86%) | High | Low (not required for core analysis) | Low | Low | Low | Keep as-is, document limitation | Data Analyst |
| RISK-002 | Missing values in Sub-issue (4.74%) | Medium | Low | Low | Low | Low | Impute with "Not specified" | Data Engineer |
| RISK-003 | Date field stored as string | Medium | Medium (impacts date operations) | Low | Medium | Medium | Convert to datetime during data cleaning | Data Engineer |
| RISK-004 | Inconsistent categorical values | Medium | Medium (may impact comparisons) | Medium | Medium | Medium | Standardize category values | Data Analyst |
| RISK-005 | State codes inconsistent format | Low | Medium | Low | Low | Low | Standardize to 2-letter codes | Data Analyst |
| RISK-006 | Unvalidated ZIP code field | Low | Low | Low | Low | Low | Document as-is, use for high-level geographic analysis only | Data Analyst |
| RISK-007 | No external validation of data accuracy | Medium | Medium | Medium | Medium | Medium | Note limitations in executive summary, triangulate insights | Lead Analyst |

---

## Risk Severity Matrix
- **High**: Immediate action required
- **Medium**: Plan for action in next sprint
- **Low**: Monitor or accept

---

## Top Risks for Executive Attention
1. **RISK-007**: No external accuracy validation (addressed via transparency)
2. **RISK-004**: Inconsistent categorical values (low impact for high-level analysis)

All risks are manageable and acceptable for this analysis!
