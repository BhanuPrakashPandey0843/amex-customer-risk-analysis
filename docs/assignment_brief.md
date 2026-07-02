# Assignment Brief (Source Document)

> This is the original assessment brief as received, kept verbatim for reference and auditability. It previously lived in `docs/problem_statement.md` under the wrong filename — that file now contains the actual problem statement this project formulated *in response to* this brief. See [`problem_statement.md`](problem_statement.md) for the analytical framing, and [`methodology.md`](methodology.md) for how it was executed.

---

## Context

**Role:** Apprentice — Data Analytics
**Assignment:** Data Analytics Assessment Challenge
**Dataset provided:** CFPB Complaints Data (Jan 2025 – Mar 2026), covering American Express and its top U.S. competitors

## Brief, as received

> Thank you for your interest in the Apprentice role.
>
> As part of our selection process, we would like you to complete the assignment provided below. This exercise is intended to help us assess your problem-solving approach, technical understanding, and communication skills.
>
> You will be working with publicly available complaints data from the Consumer Financial Protection Bureau (CFPB), a U.S. financial regulator. The dataset contains consumer complaints submitted about American Express and its top competitors in the U.S. market.
>
> Rather than providing a predefined problem statement, we encourage you to explore the data, identify meaningful themes, and develop your own analytical narrative.
>
> **Objective:** Assume your audience is Senior Leadership. Identify key risks and opportunities for American Express and provide data-driven recommendations that support business decision-making.
>
> **Required components:**
> - Exploratory Data Analysis (EDA)
> - Key insights supported by data
> - Business recommendations
> - Potential risks for American Express and proposed mitigation strategies
>
> **Submission requirements:**
> - Maximum 2 content slides
> - Optional cover page, agenda, and appendix slides permitted
> - Submit in PDF format
> - Any tools allowed (Excel, Python, SQL, Tableau, Power BI, etc.)
>
> **Notes:**
> - No predefined "correct answer"
> - No expectation to build predictive models or use advanced statistical techniques
> - Evaluators are primarily interested in analytical thinking, business judgment, and communication
> - Focus on the most important findings, not exhaustive coverage
>
> **Evaluation criteria:**
> - Analytical approach and problem framing
> - Quality and relevance of insights
> - Business recommendations
> - Risk identification and mitigation thinking
> - Data storytelling and presentation quality
> - Clarity, structure, and conciseness of communication

## How this repository responds to the brief

| Brief requirement | Where it's addressed |
|---|---|
| EDA | `notebooks/01_data_audit.ipynb` – `03_eda.ipynb`, `reports/eda_summary.md` |
| Key insights supported by data | `reports/insights_register.md` (6 insights, each with an evidence chain) |
| Business recommendations | `reports/recommendations.md` (4 REC objects with KPI targets) |
| Risks and mitigations | `reports/risk_register.md` (5 risks with likelihood, impact, owner) |
| Max 2 content slides, PDF | `data/ppt/` (designed deck, confirmed submission) — compile status in `data/ppt/README.md`; `reports/executive_presentation.pdf` is a data-validation companion |
| Any tool | Python (pandas/matplotlib), SQL, Excel — see `methodology.md` |
