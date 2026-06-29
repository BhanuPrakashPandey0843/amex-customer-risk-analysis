"""Orchestrate EDA: compute metrics, save charts, export JSON."""
from metrics_engine import Findings, compute_findings, load_data, load_metrics, save_metrics
from charts import save_all_charts

AMEX = "American Express"
COLORS = __import__("config", fromlist=["COLORS"]).COLORS


def run_eda() -> tuple[Findings, list[str]]:
    df = load_data()
    findings = compute_findings(df)
    charts = save_all_charts(df, findings)
    save_metrics(findings)
    return findings, charts


if __name__ == "__main__":
    f, charts = run_eda()
    print(f"Amex: {f.amex_complaints:,} ({f.amex_share_pct:.1f}%) | YoY: {f.yoy_pct:+.1f}%")
    print(f"Charts: {len(charts)} | Insights: {len(f.insights)} | Risks: {len(f.risks)}")
