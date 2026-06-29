-- =============================================================================
-- CFPB Complaints Analysis — SQL Query Library
-- Dataset: complaints_cleaned (196,835 rows | Jan 2025 – Mar 2026 | 9 companies)
-- Business Question: Where should Amex leadership focus to reduce risk?
-- =============================================================================

-- Q1: Competitive volume ranking with market share
-- Answers: How does Amex rank vs peers on raw complaint volume?
WITH company_totals AS (
    SELECT
        "Company",
        COUNT(*) AS complaint_count
    FROM complaints_cleaned
    GROUP BY "Company"
),
ranked AS (
    SELECT
        "Company",
        complaint_count,
        ROUND(100.0 * complaint_count / SUM(complaint_count) OVER (), 2) AS share_pct,
        RANK() OVER (ORDER BY complaint_count DESC) AS volume_rank
    FROM company_totals
)
SELECT *
FROM ranked
ORDER BY volume_rank;


-- Q2: Amex YoY and QoQ growth
-- Answers: Is complaint volume accelerating?
WITH amex_quarterly AS (
    SELECT
        "Complaint Year",
        "Complaint Quarter",
        COUNT(*) AS complaints
    FROM complaints_cleaned
    WHERE "Company" = 'American Express'
    GROUP BY "Complaint Year", "Complaint Quarter"
)
SELECT
    "Complaint Year",
    "Complaint Quarter",
    complaints,
    LAG(complaints) OVER (ORDER BY "Complaint Year", "Complaint Quarter") AS prev_quarter,
    ROUND(
        100.0 * (complaints - LAG(complaints) OVER (ORDER BY "Complaint Year", "Complaint Quarter"))
        / NULLIF(LAG(complaints) OVER (ORDER BY "Complaint Year", "Complaint Quarter"), 0),
        1
    ) AS qoq_pct
FROM amex_quarterly
ORDER BY "Complaint Year", "Complaint Quarter";


-- Q3: Pareto analysis — top issues for Amex
-- Answers: Which 20% of issues drive 80% of complaints?
WITH amex_issues AS (
    SELECT
        "Issue",
        COUNT(*) AS cnt
    FROM complaints_cleaned
    WHERE "Company" = 'American Express'
    GROUP BY "Issue"
),
cumulative AS (
    SELECT
        "Issue",
        cnt,
        ROUND(100.0 * cnt / SUM(cnt) OVER (), 2) AS pct,
        ROUND(100.0 * SUM(cnt) OVER (ORDER BY cnt DESC) / SUM(cnt) OVER (), 2) AS cumulative_pct,
        ROW_NUMBER() OVER (ORDER BY cnt DESC) AS issue_rank
    FROM amex_issues
)
SELECT *
FROM cumulative
WHERE issue_rank <= 10
ORDER BY issue_rank;


-- Q4: Prepaid card outlier — Amex share of industry issue
-- Answers: Where is Amex uniquely weak?
SELECT
    "Company",
    COUNT(*) AS trouble_using_card_complaints,
    ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
        1
    ) AS industry_share_pct
FROM complaints_cleaned
WHERE "Issue" = 'Trouble using the card'
GROUP BY "Company"
ORDER BY trouble_using_card_complaints DESC;


-- Q5: Timely response benchmark across all companies
-- Answers: Does Amex lag peers on operational response?
SELECT
    "Company",
    COUNT(*) AS total,
    SUM("Timely Response Flag") AS timely_count,
    ROUND(100.0 * AVG("Timely Response Flag"), 2) AS timely_pct,
    RANK() OVER (ORDER BY AVG("Timely Response Flag") DESC) AS timely_rank
FROM complaints_cleaned
GROUP BY "Company"
ORDER BY timely_rank;


-- Q6: Resolution outcomes — monetary relief rate by company
-- Answers: Which companies provide monetary relief most often?
SELECT
    "Company",
    COUNT(*) AS total,
    SUM(CASE WHEN "Company response to consumer" = 'Closed with monetary relief' THEN 1 ELSE 0 END) AS monetary_relief,
    ROUND(
        100.0 * SUM(CASE WHEN "Company response to consumer" = 'Closed with monetary relief' THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS monetary_relief_pct
FROM complaints_cleaned
GROUP BY "Company"
ORDER BY monetary_relief_pct DESC;


-- Q7: Issue YoY change for Amex (Q1 2025 vs Q1 2026)
-- Answers: Which issues are growing fastest?
WITH amex_q1 AS (
    SELECT
        "Issue",
        "Complaint Year",
        COUNT(*) AS cnt
    FROM complaints_cleaned
    WHERE "Company" = 'American Express'
      AND "Complaint Quarter" = 1
      AND "Complaint Year" IN (2025, 2026)
    GROUP BY "Issue", "Complaint Year"
)
SELECT
    a."Issue",
    MAX(CASE WHEN a."Complaint Year" = 2025 THEN a.cnt END) AS q1_2025,
    MAX(CASE WHEN a."Complaint Year" = 2026 THEN a.cnt END) AS q1_2026,
    ROUND(
        100.0 * (
            MAX(CASE WHEN a."Complaint Year" = 2026 THEN a.cnt END)
            - MAX(CASE WHEN a."Complaint Year" = 2025 THEN a.cnt END)
        ) / NULLIF(MAX(CASE WHEN a."Complaint Year" = 2025 THEN a.cnt END), 0),
        1
    ) AS yoy_pct
FROM amex_q1 a
GROUP BY a."Issue"
HAVING MAX(CASE WHEN a."Complaint Year" = 2025 THEN a.cnt END) >= 50
ORDER BY yoy_pct DESC
LIMIT 10;


-- Q8: Geographic concentration — top states for Amex
-- Answers: Where are complaints geographically concentrated?
SELECT
    "State",
    COUNT(*) AS complaints,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS state_share_pct,
    RANK() OVER (ORDER BY COUNT(*) DESC) AS state_rank
FROM complaints_cleaned
WHERE "Company" = 'American Express'
  AND "State" != 'Not specified'
GROUP BY "State"
ORDER BY state_rank
LIMIT 10;


-- Q9: Rolling 3-month average — Amex complaint trend
-- Answers: What is the smoothed monthly trend?
WITH monthly AS (
    SELECT
        DATE_TRUNC('month', "Date received") AS month,
        COUNT(*) AS complaints
    FROM complaints_cleaned
    WHERE "Company" = 'American Express'
    GROUP BY DATE_TRUNC('month', "Date received")
)
SELECT
    month,
    complaints,
    ROUND(
        AVG(complaints) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW),
        0
    ) AS rolling_3mo_avg
FROM monthly
ORDER BY month;


-- Q10: Product-issue cross-tab for Amex
-- Answers: Which products drive which complaint types?
SELECT
    "Product",
    "Issue",
    COUNT(*) AS complaints,
    RANK() OVER (PARTITION BY "Product" ORDER BY COUNT(*) DESC) AS issue_rank_in_product
FROM complaints_cleaned
WHERE "Company" = 'American Express'
GROUP BY "Product", "Issue"
QUALIFY issue_rank_in_product <= 3
ORDER BY "Product", issue_rank_in_product;
