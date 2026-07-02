# Problem Statement

> The original assignment brief deliberately did not provide a predefined problem statement — it asked the analyst to explore the data and form one. This document is that response. The brief itself is preserved separately in [`assignment_brief.md`](assignment_brief.md).

## Business Context

American Express operates in a U.S. consumer financial services market where complaint volume reported to the Consumer Financial Protection Bureau (CFPB) is public, searchable, and increasingly used as an informal proxy for institutional trustworthiness — by regulators, journalists, and customers comparing card issuers. A complaint filed with the CFPB is not just a service ticket; it is a regulatory exposure event and a public data point simultaneously.

This creates a dual mandate for any complaints analysis: it has to serve **Customer Experience** (where is friction happening, and why) and **Risk/Compliance** (which complaint patterns carry regulatory weight under frameworks like FCRA, FDCPA, UDAAP, or Reg Z/FCBA) at the same time. A finding that looks minor from a CX lens can be material from a regulatory one, and vice versa.

## The Problem

Leadership does not currently have a single, evidence-based view that answers three linked questions:

1. **Where does American Express stand competitively** on CFPB complaint volume against the other 8 major institutions in this dataset (Capital One, JPMorgan Chase, Citibank, Wells Fargo, Bank of America, Synchrony Financial, U.S. Bank, Barclays)?
2. **Within Amex's own complaint base, which specific issues are concentrated, accelerating, or regulatorily exposed** enough to warrant executive attention — as opposed to the long tail of low-frequency, low-severity complaints that don't merit a leadership-level response?
3. **What should leadership actually do about it** — with enough specificity (root cause, owner, timeline, KPI target) that the recommendation is actionable rather than directional?

A raw complaint count answers none of these on its own. 196,835 rows of categorical data have to be turned into a small number of decisions.

## Scope

**In scope:**
- Jan 2025 – Mar 2026 CFPB complaint records for American Express and 8 named competitors
- Volume, trend, product, issue, geographic, and resolution-quality analysis
- Competitive benchmarking on a relative (not per-capita) basis
- Risk identification with regulatory-framework mapping (FCRA / FDCPA / UDAAP / Reg Z)
- Prioritized, evidence-backed recommendations with explicit root cause and KPI targets

**Out of scope** (see `reports/executive_limitations.md` for the full list and reasoning):
- Predictive modeling — explicitly excluded by the assignment brief, and not supportable by 15 months of categorical data without overfitting risk
- Per-capita / market-share normalization — the dataset contains no card-base or customer-count data (tracked as a gap in `data/external/README.md`)
- Root-cause analysis below the complaint-category level — the CFPB dataset has no operational or narrative data to diagnose *why* a process failed internally, only *that* a customer experienced friction
- Financial impact quantification — no revenue, cost, or customer-lifetime-value data is present

## Why This Framing, Not Another

The data could have been sliced many ways — by company response type, by state, by month. The framing chosen here (competitive position → issue concentration → regulatory exposure → recommendation) was selected because it mirrors how a Senior Leadership audience actually makes decisions: first establish whether there's a problem at all (competitive context), then localize it (which issues, how concentrated), then weight it (regulatory/reputational stakes), then act (specific, owned, time-bound recommendations). A purely descriptive walk through all 13 raw columns would have produced more charts and fewer decisions — see `reports/executive_kpis.md` for the KPI framework built specifically to support this decision path.

## Success Criteria

This analysis is successful if a Chief Risk Officer or Customer Experience executive can read `reports/executive_summary.md` in under two minutes and know:
1. Whether Amex's complaint position is improving or deteriorating, and how urgently
2. Which 2–3 issues deserve resourcing this quarter
3. What specifically to do, who owns it, and how success will be measured

Full traceability from this problem statement through to the computed numbers behind each recommendation is documented in `docs/project_dependency_map.md`.
