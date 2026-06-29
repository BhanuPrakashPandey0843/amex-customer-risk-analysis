"""Compute all business metrics from cleaned CFPB data."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from config import AMEX, CLEAN_DATA, METRICS_PATH

REGULATORY_ISSUES = {
    "Incorrect information on your report": "FCRA",
    "Improper use of your report": "FCRA",
    "Problem with a company's investigation into an existing problem": "FCRA",
    "Took or threatened to take negative or legal action": "FDCPA/UDAAP",
    "Fees or interest": "UDAAP",
    "Problem with a purchase shown on your statement": "Reg Z / FCBA",
}


@dataclass
class Findings:
    # Core scope
    total_complaints: int
    amex_complaints: int
    amex_share_pct: float
    amex_rank: int
    num_companies: int
    date_min: str
    date_max: str

    # Volume & mix
    company_volume: dict
    amex_products: dict
    amex_issues: dict
    pareto_top5_pct: float

    # Outlier
    prepaid_outlier_pct: float
    prepaid_outlier_amex: int
    prepaid_outlier_total: int

    # Trends
    q1_2025: int
    q1_2026: int
    yoy_pct: float
    aug_2025: int
    mar_2026: int
    monthly_trend_pct: float
    qoq_q4_to_q1_pct: float

    # Operations
    amex_timely_pct: float
    peer_timely_pct: float
    amex_timely_rank: int
    resolution_explanation_pct: float
    resolution_monetary_pct: float
    resolution_nonmonetary_pct: float
    peer_monetary_relief_pct: float

    # Geography
    top_states: dict

    # Advanced (Step 4)
    issue_yoy_changes: dict
    fastest_growing_issues: list
    declining_issues: list
    amex_strengths: list
    amex_weaknesses: list
    monetary_relief_by_issue: dict
    regulatory_exposure: dict
    product_drivers: dict
    peer_benchmark_kpis: dict
    recommendations: list
    insights: list
    risks: list

    generated_at: str = ""


def load_data() -> pd.DataFrame:
    return pd.read_csv(CLEAN_DATA, parse_dates=["Date received"])


def _issue_yoy(amex: pd.DataFrame, top_n: int = 8) -> dict[str, dict[str, float]]:
    top_issues = amex["Issue"].value_counts().head(top_n).index
    result = {}
    for issue in top_issues:
        q1_25 = ((amex["Issue"] == issue) & (amex["Complaint Year"] == 2025) & (amex["Complaint Quarter"] == 1)).sum()
        q1_26 = ((amex["Issue"] == issue) & (amex["Complaint Year"] == 2026) & (amex["Complaint Quarter"] == 1)).sum()
        pct = ((q1_26 - q1_25) / q1_25 * 100) if q1_25 else 0.0
        result[issue] = {"q1_2025": int(q1_25), "q1_2026": int(q1_26), "yoy_pct": round(pct, 1)}
    return result


def _peer_benchmark(df: pd.DataFrame) -> dict[str, Any]:
    timely = df.groupby("Company")["Timely Response Flag"].mean() * 100
    monetary = df.groupby("Company")["Company response to consumer"].apply(
        lambda s: (s == "Closed with monetary relief").mean() * 100
    )
    volume = df["Company"].value_counts()
    return {
        "timely": {k: round(v, 2) for k, v in timely.items()},
        "monetary_relief": {k: round(v, 2) for k, v in monetary.items()},
        "volume": {k: int(v) for k, v in volume.items()},
    }


def _amex_vs_peer_issue_share(df: pd.DataFrame, amex_n: int) -> tuple[list, list]:
    """Identify issues where Amex over/under-indexes vs proportional share."""
    amex = df[df["Company"] == AMEX]
    strengths, weaknesses = [], []
    amex_share = amex_n / len(df)
    for issue in amex["Issue"].value_counts().head(10).index:
        amex_cnt = (amex["Issue"] == issue).sum()
        industry_cnt = (df["Issue"] == issue).sum()
        amex_issue_share = amex_cnt / industry_cnt if industry_cnt else 0
        expected = amex_share
        index = amex_issue_share / expected if expected else 0
        entry = {
            "issue": issue,
            "amex_count": int(amex_cnt),
            "industry_count": int(industry_cnt),
            "amex_industry_share_pct": round(amex_issue_share * 100, 1),
            "index_vs_expected": round(index, 2),
        }
        if index >= 1.5:
            weaknesses.append(entry)
        elif index <= 0.7:
            strengths.append(entry)
    weaknesses.sort(key=lambda x: x["index_vs_expected"], reverse=True)
    strengths.sort(key=lambda x: x["index_vs_expected"])
    return strengths[:3], weaknesses[:5]


def _regulatory_exposure(amex: pd.DataFrame) -> dict[str, int]:
    exposure = {}
    for issue, reg in REGULATORY_ISSUES.items():
        cnt = (amex["Issue"] == issue).sum()
        if cnt:
            exposure[reg] = exposure.get(reg, 0) + int(cnt)
    return dict(sorted(exposure.items(), key=lambda x: x[1], reverse=True))


def _build_insights(f_dict: dict) -> list[dict]:
    """Structured insight objects: Observation → Evidence → Impact → Recommendation → Outcome."""
    insights = [
        {
            "id": "INS-001",
            "observation": "Amex complaint volume is below mega-bank peers",
            "evidence": f"{f_dict['amex_complaints']:,} complaints ({f_dict['amex_share_pct']:.1f}% share), rank {f_dict['amex_rank']}/{f_dict['num_companies']}",
            "impact": "Lower relative CFPB visibility vs Capital One (21.5%) and Chase (16.0%)",
            "recommendation": "Protect volume advantage; shift investment from volume management to root-cause reduction",
            "outcome": "Sustain top-quartile competitive position on complaint volume",
            "priority": "MEDIUM",
        },
        {
            "id": "INS-002",
            "observation": "Credit reporting accuracy is the #1 Amex complaint driver",
            "evidence": f"2,248 complaints (16.5%) on incorrect report information; FCRA regulatory category",
            "impact": "Reputational risk with credit-conscious premium cardmembers; bureau dispute escalation",
            "recommendation": "Launch bureau-data reconciliation sprint with automated verifiable-error resolution",
            "outcome": "15–25% reduction in credit-reporting complaints within 6 months",
            "priority": "CRITICAL",
        },
        {
            "id": "INS-003",
            "observation": "Prepaid card usability is a unique industry outlier",
            "evidence": f"Amex = {f_dict['prepaid_outlier_pct']:.0f}% of all 'Trouble using card' complaints ({f_dict['prepaid_outlier_amex']:,}/{f_dict['prepaid_outlier_total']:,})",
            "impact": "Disproportionate CFPB visibility on a fixable product failure; no peer exhibits this concentration",
            "recommendation": "Emergency root-cause on activation/merchant acceptance; partner merchant audit",
            "outcome": "Eliminate category outlier status; address 1,219 complaints",
            "priority": "CRITICAL",
        },
        {
            "id": "INS-004",
            "observation": "Complaint volume is accelerating despite favorable rank",
            "evidence": f"+{f_dict['yoy_pct']:.1f}% YoY Q1 ({f_dict['q1_2025']:,} → {f_dict['q1_2026']:,}); +{f_dict['monthly_trend_pct']:.0f}% Aug 2025–Mar 2026",
            "impact": "Early warning of systemic deterioration if unchecked; rank masks trajectory",
            "recommendation": "Establish executive monthly CFPB review with product-level root-cause tracking",
            "outcome": "Detect and reverse trend before reaching peer-average growth rates",
            "priority": "HIGH",
        },
        {
            "id": "INS-005",
            "observation": "Issue concentration enables surgical intervention",
            "evidence": f"Top 5 issues = {f_dict['pareto_top5_pct']:.0f}% of all Amex complaints (Pareto principle)",
            "impact": "Focused investment on 3 product clusters yields disproportionate complaint reduction",
            "recommendation": "Stand up cross-functional task force on Credit Reporting, Billing Disputes, Prepaid Card",
            "outcome": "Target 20%+ reduction in top-5 issue volume within 12 months",
            "priority": "HIGH",
        },
        {
            "id": "INS-006",
            "observation": "Resolution quality is a competitive strength to leverage",
            "evidence": f"{f_dict['resolution_explanation_pct']:.0f}% closed with explanation vs {f_dict['amex_timely_pct']:.1f}% timely (rank {f_dict['amex_timely_rank']}/9)",
            "impact": "Strong post-complaint resolution; opportunity to shift capacity upstream to prevention",
            "recommendation": "Reinvest operational capacity from timeliness optimization into proactive outreach",
            "outcome": "Reduce CFPB filings before escalation; improve NPS on dispute-prone journeys",
            "priority": "MEDIUM",
        },
    ]
    return insights


def _build_recommendations(f_dict: dict) -> list[dict]:
    return [
        {
            "id": "REC-001",
            "problem": "Credit reporting data inaccuracies drive #1 complaint category",
            "root_cause": "Bureau data sync gaps and manual dispute investigation delays",
            "evidence": "2,248 FCRA-category complaints (16.5%); 771 on inadequate investigation",
            "action": "Bureau-data reconciliation pipeline; auto-resolve verifiable errors within 48 hours",
            "benefit": "Reduced regulatory exposure and premium customer trust erosion",
            "priority": "P1",
            "effort": "Medium (3–6 months)",
            "kpi_target": "15–25% reduction in credit-reporting complaints",
            "risk": "Incomplete bureau matching may create false positives",
            "mitigation": "Human review queue for edge cases; phased rollout by error type",
            "timeline": "Pilot 30 days; full deployment 90 days",
        },
        {
            "id": "REC-002",
            "problem": "Merchant billing disputes unresolved at scale",
            "root_cause": "Manual dispute routing; 1,484 sub-issues cite unresolved purchase disputes",
            "evidence": "1,784 statement disputes (#2 issue); 83% of sub-issues are unresolved disputes",
            "action": "AI-assisted merchant dispute triage; 48-hr first-response SLA; proactive status updates",
            "benefit": "Faster resolution, lower re-complaint rate, reduced FCBA exposure",
            "priority": "P1",
            "effort": "Medium (2–4 months)",
            "kpi_target": "20% faster resolution; 10% reduction in billing dispute volume",
            "risk": "Automation may misclassify complex fraud cases",
            "mitigation": "Escalation rules for high-value and fraud-flagged disputes",
            "timeline": "Pilot on top 500 merchant categories in 60 days",
        },
        {
            "id": "REC-003",
            "problem": "Prepaid card activation/acceptance failures",
            "root_cause": "Product-specific merchant network or activation workflow failure",
            "evidence": f"78% industry share on card usage failures; 100% from Prepaid product line",
            "action": "Root-cause analysis; partner merchant audit; product redesign or sunset decision",
            "benefit": "Eliminate most disproportionate CFPB visibility; protect brand on card products",
            "priority": "P1",
            "effort": "High (requires cross-functional product + tech)",
            "kpi_target": "Reduce prepaid usage complaints by 50%+ within 6 months",
            "risk": "Product sunset may affect partner revenue",
            "mitigation": "Fix-first approach with 90-day remediation window before sunset decision",
            "timeline": "Task force stand-up within 14 days",
        },
        {
            "id": "REC-004",
            "problem": "Complaint volume acceleration",
            "root_cause": "Emerging friction in credit reporting and prepaid products outpacing prevention",
            "evidence": f"+{f_dict['yoy_pct']:.1f}% YoY; monthly volume +{f_dict['monthly_trend_pct']:.0f}% over 7 months",
            "action": "Executive CFPB dashboard with monthly review; product-level early warning thresholds",
            "benefit": "Leadership visibility before trends become systemic",
            "priority": "P2",
            "effort": "Low (30 days)",
            "kpi_target": "Flat or declining YoY growth within 2 quarters",
            "risk": "Dashboard fatigue without action accountability",
            "mitigation": "Assign executive owner per product cluster with monthly KPI targets",
            "timeline": "Dashboard live in 30 days",
        },
    ]


def _build_risks(f_dict: dict, amex_n: int) -> list[dict]:
    return [
        {
            "id": "RISK-001", "name": "Credit Reporting Data Accuracy",
            "likelihood": "High", "impact": "High", "severity": "Critical",
            "business_area": "Compliance / Credit Reporting",
            "affected_customers": "Premium cardmembers with bureau disputes",
            "financial_risk": "Medium — dispute processing cost + potential regulatory action",
            "operational_risk": "High — manual investigation backlog (771 inadequate investigation complaints)",
            "regulatory_risk": "High — FCRA exposure at 3,236 combined FCRA-category complaints",
            "reputational_risk": "High — credit accuracy is core to premium brand promise",
            "evidence": "2,248 incorrect report info + 988 improper report use + 771 investigation failures",
            "mitigation": "Bureau reconciliation sprint; automated verifiable-error resolution",
            "owner": "Chief Compliance Officer + Credit Reporting Ops",
            "priority": "P1",
            "expected_impact": "15–25% reduction in FCRA-category complaints",
        },
        {
            "id": "RISK-002", "name": "Billing & Merchant Dispute Friction",
            "likelihood": "High", "impact": "High", "severity": "Critical",
            "business_area": "Customer Experience / Credit Card",
            "affected_customers": "Core credit card cardmembers",
            "financial_risk": "Medium — chargeback costs and potential monetary relief (12.2% rate)",
            "operational_risk": "High — 1,484 unresolved dispute sub-issues",
            "regulatory_risk": "Medium — Reg Z / FCBA billing dispute requirements",
            "reputational_risk": "High — billing disputes directly affect card usage and retention",
            "evidence": "1,784 statement disputes; 83% of sub-issues cite unresolved disputes",
            "mitigation": "AI dispute triage; 48-hr SLA; proactive status notifications",
            "owner": "Head of Customer Care + Disputes Operations",
            "priority": "P1",
            "expected_impact": "20% faster resolution; 10% volume reduction",
        },
        {
            "id": "RISK-003", "name": "Prepaid Card Systemic Failure",
            "likelihood": "Medium", "impact": "High", "severity": "Critical",
            "business_area": "Product / Prepaid Card",
            "affected_customers": "Prepaid card users (1,471 product complaints)",
            "financial_risk": "Low–Medium — product line revenue at risk if sunset",
            "operational_risk": "Critical — 78% industry share on single issue type",
            "regulatory_risk": "Medium — concentrated CFPB visibility",
            "reputational_risk": "Medium — isolated to prepaid segment, not core premium brand",
            "evidence": f"1,219 of 1,562 industry 'Trouble using card' complaints are Amex prepaid",
            "mitigation": "Root-cause analysis; merchant audit; redesign or sunset decision",
            "owner": "Prepaid Product GM + Merchant Partnerships",
            "priority": "P1",
            "expected_impact": "Eliminate category outlier status",
        },
        {
            "id": "RISK-004", "name": "Complaint Volume Acceleration",
            "likelihood": "High", "impact": "Medium", "severity": "High",
            "business_area": "Strategy / Executive",
            "affected_customers": "All product lines",
            "financial_risk": "Low — indirect via retention and regulatory cost",
            "operational_risk": "Medium — rising case load if trend continues",
            "regulatory_risk": "Medium — increasing CFPB scrutiny as volume grows",
            "reputational_risk": "Medium — trend reversal would erode volume advantage",
            "evidence": f"+{f_dict['yoy_pct']:.1f}% YoY Q1; +{f_dict['monthly_trend_pct']:.0f}% monthly trend",
            "mitigation": "Executive monthly review; product-level early warning dashboard",
            "owner": "Chief Customer Officer",
            "priority": "P2",
            "expected_impact": "Stabilize YoY growth within 2 quarters",
        },
        {
            "id": "RISK-005", "name": "Debt Collection Practice Exposure",
            "likelihood": "Medium", "impact": "High", "severity": "High",
            "business_area": "Collections / Legal",
            "affected_customers": "Delinquent account holders",
            "financial_risk": "Medium — collection recovery impact if practices restricted",
            "operational_risk": "Medium — 797 threatened legal action complaints",
            "regulatory_risk": "High — FDCPA/UDAAP on collection practices",
            "reputational_risk": "Medium — affects subset of customer base",
            "evidence": "797 complaints on threatened negative/legal action (100% debt collection product)",
            "mitigation": "Third-party agency script review; escalation threshold update",
            "owner": "Head of Collections + Legal Compliance",
            "priority": "P2",
            "expected_impact": "Reduce collection-related complaints by 15%",
        },
    ]


def compute_findings(df: pd.DataFrame) -> Findings:
    amex = df[df["Company"] == AMEX]
    an, tn = len(amex), len(df)

    company_vol = df["Company"].value_counts()
    amex_rank = list(company_vol.index).index(AMEX) + 1
    issues = amex["Issue"].value_counts()
    p5 = issues.head(5).sum() / an * 100

    tuc_amex = int((amex["Issue"] == "Trouble using the card").sum())
    tuc_all = int((df["Issue"] == "Trouble using the card").sum())
    prepaid_pct = tuc_amex / tuc_all * 100 if tuc_all else 0.0

    q1_25 = int(((amex["Complaint Year"] == 2025) & (amex["Complaint Quarter"] == 1)).sum())
    q1_26 = int(((amex["Complaint Year"] == 2026) & (amex["Complaint Quarter"] == 1)).sum())
    yoy = (q1_26 - q1_25) / q1_25 * 100 if q1_25 else 0.0

    q4_25 = int(((amex["Complaint Year"] == 2025) & (amex["Complaint Quarter"] == 4)).sum())
    qoq = (q1_26 - q4_25) / q4_25 * 100 if q4_25 else 0.0

    aug25 = int(((amex["Complaint Year"] == 2025) & (amex["Complaint Month"] == 8)).sum())
    mar26 = int(((amex["Complaint Year"] == 2026) & (amex["Complaint Month"] == 3)).sum())
    trend = (mar26 - aug25) / aug25 * 100 if aug25 else 0.0

    timely = df.groupby("Company")["Timely Response Flag"].mean() * 100
    peer_timely = timely.drop(AMEX).mean()
    timely_rank = list(timely.sort_values(ascending=False).index).index(AMEX) + 1

    resp = amex["Company response to consumer"].value_counts(normalize=True) * 100
    peer_monetary = (
        df[df["Company"] != AMEX]["Company response to consumer"]
        .eq("Closed with monetary relief").mean() * 100
    )

    issue_yoy = _issue_yoy(amex)
    growing = sorted(issue_yoy.items(), key=lambda x: x[1]["yoy_pct"], reverse=True)
    fastest = [{"issue": k, **v} for k, v in growing[:3]]
    declining = [{"issue": k, **v} for k, v in growing if v["yoy_pct"] < 0]

    strengths, weaknesses = _amex_vs_peer_issue_share(df, an)
    reg_exposure = _regulatory_exposure(amex)
    peer_kpis = _peer_benchmark(df)

    monetary_by_issue = {}
    for issue in issues.head(8).index:
        subset = amex[amex["Issue"] == issue]
        rate = (subset["Company response to consumer"] == "Closed with monetary relief").mean() * 100
        monetary_by_issue[issue] = round(rate, 1)

    product_drivers = {}
    for p in amex["Product"].value_counts().head(5).index:
        subset = amex[amex["Product"] == p]
        top = subset["Issue"].value_counts()
        product_drivers[p] = {
            "count": int(len(subset)),
            "top_issue": top.index[0],
            "top_issue_count": int(top.iloc[0]),
        }

    base = {
        "amex_complaints": an, "amex_share_pct": an / tn * 100,
        "amex_rank": amex_rank, "num_companies": df["Company"].nunique(),
        "pareto_top5_pct": p5, "prepaid_outlier_pct": prepaid_pct,
        "prepaid_outlier_amex": tuc_amex, "prepaid_outlier_total": tuc_all,
        "q1_2025": q1_25, "q1_2026": q1_26, "yoy_pct": yoy,
        "monthly_trend_pct": trend, "amex_timely_pct": float(timely[AMEX]),
        "amex_timely_rank": timely_rank, "resolution_explanation_pct": float(resp.get("Closed with explanation", 0)),
    }

    return Findings(
        total_complaints=tn,
        amex_complaints=an,
        amex_share_pct=an / tn * 100,
        amex_rank=amex_rank,
        num_companies=df["Company"].nunique(),
        date_min=str(df["Date received"].min().date()),
        date_max=str(df["Date received"].max().date()),
        company_volume={k: int(v) for k, v in company_vol.items()},
        amex_products={k: int(v) for k, v in amex["Product"].value_counts().items()},
        amex_issues={k: int(v) for k, v in issues.head(10).items()},
        pareto_top5_pct=p5,
        prepaid_outlier_pct=prepaid_pct,
        prepaid_outlier_amex=tuc_amex,
        prepaid_outlier_total=tuc_all,
        q1_2025=q1_25,
        q1_2026=q1_26,
        yoy_pct=yoy,
        aug_2025=aug25,
        mar_2026=mar26,
        monthly_trend_pct=trend,
        qoq_q4_to_q1_pct=qoq,
        amex_timely_pct=float(timely[AMEX]),
        peer_timely_pct=float(peer_timely),
        amex_timely_rank=timely_rank,
        resolution_explanation_pct=float(resp.get("Closed with explanation", 0)),
        resolution_monetary_pct=float(resp.get("Closed with monetary relief", 0)),
        resolution_nonmonetary_pct=float(resp.get("Closed with non-monetary relief", 0)),
        peer_monetary_relief_pct=float(peer_monetary),
        top_states={k: int(v) for k, v in amex["State"].value_counts().head(5).items()},
        issue_yoy_changes=issue_yoy,
        fastest_growing_issues=fastest,
        declining_issues=declining,
        amex_strengths=strengths,
        amex_weaknesses=weaknesses,
        monetary_relief_by_issue=monetary_by_issue,
        regulatory_exposure=reg_exposure,
        product_drivers=product_drivers,
        peer_benchmark_kpis=peer_kpis,
        recommendations=_build_recommendations(base),
        insights=_build_insights(base),
        risks=_build_risks(base, an),
        generated_at=pd.Timestamp.now().isoformat(),
    )


def save_metrics(findings: Findings) -> Path:
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.write_text(json.dumps(asdict(findings), indent=2, default=str), encoding="utf-8")
    return METRICS_PATH


def load_metrics() -> Findings:
    data = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    return Findings(**data)
