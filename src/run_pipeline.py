"""Orchestrate full CFPB analysis pipeline."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from analytics import run_eda
from build_excel import build_excel
from build_reports import build_reports
from executive_analysis import build_pdf


def main():
    print("=" * 65)
    print("  CFPB RISK INTELLIGENCE — FULL ANALYSIS PIPELINE")
    print("=" * 65)

    print("\n[1/4] Computing metrics + generating charts...")
    findings, charts = run_eda()
    print(f"      Amex: {findings.amex_complaints:,} ({findings.amex_share_pct:.1f}%) | YoY: {findings.yoy_pct:+.1f}%")
    print(f"      Charts: {len(charts)} | Insights: {len(findings.insights)} | Risks: {len(findings.risks)}")

    print("\n[2/4] Writing reports from computed metrics...")
    for p in build_reports(findings):
        print(f"      {p.name}")

    print("\n[3/4] Building executive Excel workbook...")
    xlsx = build_excel()
    print(f"      {xlsx.name} ({xlsx.stat().st_size:,} bytes)")

    print("\n[4/4] Generating executive PDF...")
    pdf = build_pdf()
    print(f"      {pdf.name} ({pdf.stat().st_size:,} bytes)")

    print("\n" + "=" * 65)
    print("  SUBMISSION READY")
    print(f"  PDF:    reports/executive_presentation.pdf")
    print(f"  Excel:  reports/CFPB_Executive_Analytics.xlsx")
    print(f"  SQL:    sql/01_business_analysis.sql")
    print(f"  Metrics: data/processed/eda_metrics.json")
    print("=" * 65)


if __name__ == "__main__":
    main()
