"""Generate consulting-style executive presentation PDF."""
import sys
from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from analytics import run_eda
from config import COLORS
from metrics_engine import load_metrics

AB, AD, RD, GN, AM, NT = COLORS["amex"], COLORS["navy"], COLORS["red"], COLORS["green"], COLORS["amber"], "#5A6872"
OUT = ROOT / "reports"
CHARTS = OUT / "charts"


def _header(fig, title: str, subtitle: str):
    fig.patch.set_facecolor("white")
    fig.text(0.05, 0.94, title, fontsize=18, fontweight="bold", color=AD, wrap=True)
    fig.text(0.05, 0.885, subtitle, fontsize=9.5, color=NT, wrap=True)
    fig.add_artist(mpatches.Rectangle((0, 0.855), 1, 0.004, transform=fig.transFigure, color=AB, clip_on=False))


def build_pdf() -> Path:
    if not (CHARTS / "01_competitive_volume.png").exists():
        run_eda()
    f = load_metrics()
    pdf_path = OUT / "executive_presentation.pdf"

    slide1_title = "Amex Holds a Volume Advantage — But Three Issue Clusters Are Accelerating Toward Regulatory Risk"
    slide2_title = "Three P1 Actions Can Reduce 53% of Complaints and Eliminate Amex's Biggest Competitive Outlier"

    with PdfPages(pdf_path) as pdf:
        # Cover
        fig = plt.figure(figsize=(13.333, 7.5))
        fig.patch.set_facecolor(AD)
        fig.text(0.5, 0.60, "CFPB Consumer Complaints Intelligence", ha="center", fontsize=26, fontweight="bold", color="white")
        fig.text(0.5, 0.50, "Strategic Risk & Opportunity Assessment", ha="center", fontsize=16, color="#A8C8F0")
        fig.text(0.5, 0.38, "American Express  |  Senior Leadership Briefing", ha="center", fontsize=13, color="white")
        fig.text(0.5, 0.28, f"{f.date_min} – {f.date_max}  |  {f.total_complaints:,} Complaints  |  9 Competitors", ha="center", fontsize=10, color="#8899BB")
        fig.text(0.5, 0.08, "Data Analytics Assessment Submission", ha="center", fontsize=9, color="#667799")
        pdf.savefig(fig, bbox_inches="tight")
        plt.close()

        # Agenda
        fig = plt.figure(figsize=(13.333, 7.5))
        _header(fig, "Agenda", "Two content slides + supporting appendix")
        for i, t in enumerate([
            "1.  Amex Holds a Volume Advantage — But Risk Is Concentrated and Accelerating",
            "2.  Three P1 Actions Can Address 53% of Complaints and the Prepaid Outlier",
            "A.  Appendix — Methodology, Charts, and Data Limitations",
        ]):
            fig.text(0.08, 0.78 - i * 0.12, t, fontsize=13, color=AD)
        pdf.savefig(fig, bbox_inches="tight")
        plt.close()

        # SLIDE 1 — Content
        fig = plt.figure(figsize=(13.333, 7.5))
        _header(fig, f"Slide 1 — {slide1_title}", "Evidence from 196,835 CFPB complaints across 9 institutions")

        kpis = [
            (f"{f.amex_share_pct:.1f}%", f"Share (Rank {f.amex_rank}/9)", GN),
            (f"+{f.yoy_pct:.0f}%", "YoY Q1 Growth", RD),
            (f"{f.pareto_top5_pct:.0f}%", "Top 5 Issues", AM),
            (f"{f.prepaid_outlier_pct:.0f}%", "Prepaid Outlier", RD),
            (f"{f.amex_timely_pct:.1f}%", "Timely Response", AB),
        ]
        for i, (v, label, col) in enumerate(kpis):
            x = 0.04 + i * 0.19
            fig.add_artist(mpatches.FancyBboxPatch((x, 0.68), 0.17, 0.10, boxstyle="round,pad=0.01",
                transform=fig.transFigure, facecolor="#F4F8FC", edgecolor=col, linewidth=2))
            fig.text(x + 0.085, 0.735, v, ha="center", fontsize=16, fontweight="bold", color=col)
            fig.text(x + 0.085, 0.695, label, ha="center", fontsize=7.5, color=NT)

        ax1 = fig.add_axes([0.03, 0.30, 0.46, 0.34])
        ax1.imshow(mpimg.imread(CHARTS / "01_competitive_volume.png"))
        ax1.axis("off")
        ax2 = fig.add_axes([0.51, 0.30, 0.46, 0.34])
        ax2.imshow(mpimg.imread(CHARTS / "02_amex_monthly_trend.png"))
        ax2.axis("off")

        takeaway = (
            f"SO WHAT: Amex ranks {f.amex_rank}th of {f.num_companies} on volume — a strength. "
            f"But +{f.yoy_pct:.0f}% YoY growth and {f.pareto_top5_pct:.0f}% concentration in 5 issues mean "
            f"leadership must act on Credit Reporting ({f.amex_issues.get('Incorrect information on your report', 0):,}), "
            f"Billing Disputes ({f.amex_issues.get('Problem with a purchase shown on your statement', 0):,}), "
            f"and Prepaid ({f.prepaid_outlier_pct:.0f}% industry outlier) — not timeliness ({f.amex_timely_pct:.1f}%)."
        )
        fig.text(0.05, 0.06, takeaway, fontsize=8.5, color=AD,
                 bbox=dict(boxstyle="round,pad=0.4", facecolor=COLORS["light_blue"], edgecolor=AB))
        pdf.savefig(fig, bbox_inches="tight")
        plt.close()

        # SLIDE 2 — Content
        fig = plt.figure(figsize=(13.333, 7.5))
        _header(fig, f"Slide 2 — {slide2_title}", "Each action is supported by computed complaint data — not assumptions")

        recs = f.recommendations[:3]
        colors = [RD, AM, AB]
        for i, (rec, col) in enumerate(zip(recs, colors)):
            y = 0.66 - i * 0.19
            fig.add_artist(mpatches.FancyBboxPatch((0.04, y), 0.52, 0.16, boxstyle="round,pad=0.01",
                transform=fig.transFigure, facecolor="#FAFBFC", edgecolor=col, linewidth=1.5))
            fig.text(0.06, y + 0.12, f"{rec['id']}: {rec['problem'][:55]}", fontsize=10, fontweight="bold", color=col)
            fig.text(0.06, y + 0.07, f"Evidence: {rec['evidence'][:70]}", fontsize=8, color=NT)
            fig.text(0.06, y + 0.02, f"Action: {rec['action'][:65]}", fontsize=8, color=AD, fontweight="bold")
            fig.text(0.06, y - 0.02, f"Target: {rec['kpi_target']}", fontsize=8, color=GN)

        ax = fig.add_axes([0.58, 0.28, 0.38, 0.50])
        ax.imshow(mpimg.imread(CHARTS / "04_prepaid_outlier.png"))
        ax.axis("off")

        opp = (
            f"OPPORTUNITY: {f.resolution_explanation_pct:.0f}% close with explanation (strength). "
            f"Reinvest from minor timeliness gap ({f.amex_timely_pct:.1f}% vs {f.peer_timely_pct:.1f}% peers) "
            f"into prevention. Expected: stabilize YoY growth within 2 quarters."
        )
        fig.text(0.05, 0.06, opp, fontsize=8.5, color=AD,
                 bbox=dict(boxstyle="round,pad=0.4", facecolor="#E8F5E9", edgecolor=GN))
        pdf.savefig(fig, bbox_inches="tight")
        plt.close()

        # Appendix
        fig = plt.figure(figsize=(13.333, 7.5))
        _header(fig, "Appendix — Supporting Analysis", "All metrics computed from complaints_cleaned.csv via src/run_pipeline.py")

        charts_appendix = [
            ("03_pareto_issues.png", 0.03, 0.42, 0.30, 0.38),
            ("05_issue_yoy_change.png", 0.35, 0.42, 0.30, 0.38),
            ("08_regulatory_exposure.png", 0.67, 0.42, 0.30, 0.38),
            ("09_product_clusters.png", 0.03, 0.05, 0.30, 0.32),
            ("07_top_states.png", 0.35, 0.05, 0.30, 0.32),
            ("06_timely_benchmark.png", 0.67, 0.05, 0.30, 0.32),
        ]
        for fname, x, y, w, h in charts_appendix:
            ax = fig.add_axes([x, y, w, h])
            p = CHARTS / fname
            if p.exists():
                ax.imshow(mpimg.imread(p))
            ax.axis("off")

        fig.text(0.05, 0.01,
                 "Methods: EDA, Pareto, YoY/QoQ, competitive benchmarking, regulatory mapping | "
                 "Limitation: Self-reported; not normalized by card base",
                 fontsize=7.5, color=NT)
        pdf.savefig(fig, bbox_inches="tight")
        plt.close()

    return pdf_path


if __name__ == "__main__":
    p = build_pdf()
    print(f"PDF saved: {p} ({p.stat().st_size:,} bytes)")
