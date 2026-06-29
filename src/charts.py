"""Publication-quality chart generation."""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from config import AMEX, CHARTS_DIR, CHART_STYLE, COLORS
from metrics_engine import Findings, load_data


def _apply_style():
    plt.rcParams.update(CHART_STYLE)


def save_all_charts(df: pd.DataFrame, f: Findings) -> list[str]:
    _apply_style()
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    amex = df[df["Company"] == AMEX]
    saved = []

    # 01 Competitive volume
    fig, ax = plt.subplots(figsize=(10, 5.5))
    vol = pd.Series(f.company_volume).sort_values(ascending=True)
    colors = [COLORS["amex"] if c == AMEX else COLORS["gray"] for c in vol.index]
    bars = ax.barh(vol.index, vol.values, color=colors, height=0.7)
    ax.set_xlabel("CFPB Complaints")
    ax.set_title("Amex Ranks 7th of 9 — Volume Is a Relative Strength", fontweight="bold", color=COLORS["navy"])
    for bar, v in zip(bars, vol.values):
        ax.text(v + 400, bar.get_y() + bar.get_height() / 2, f"{v:,}", va="center", fontsize=8)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    p = CHARTS_DIR / "01_competitive_volume.png"
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)
    saved.append(str(p))

    # 02 Monthly trend with annotation
    monthly = amex.groupby(["Complaint Year", "Complaint Month"]).size().reset_index(name="count")
    monthly["period"] = pd.to_datetime(
        monthly["Complaint Year"].astype(str) + "-" + monthly["Complaint Month"].astype(str).str.zfill(2)
    )
    monthly = monthly.sort_values("period")
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.fill_between(monthly["period"], monthly["count"], alpha=0.15, color=COLORS["red"])
    ax.plot(monthly["period"], monthly["count"], color=COLORS["red"], linewidth=2.5, marker="o", markersize=4)
    ax.set_title(f"Complaint Volume Is Accelerating (+{f.yoy_pct:.0f}% YoY Q1)", fontweight="bold", color=COLORS["navy"])
    ax.set_ylabel("Amex Complaints")
    ax.annotate(f"Q1'25: {f.q1_2025:,}", xy=(monthly["period"].iloc[0], f.q1_2025 / 3),
                fontsize=8, color=COLORS["red"])
    ax.annotate(f"Q1'26: {f.q1_2026:,}", xy=(monthly["period"].iloc[-3], f.q1_2026 / 3),
                fontsize=8, color=COLORS["red"])
    ax.tick_params(axis="x", rotation=45)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    p = CHARTS_DIR / "02_amex_monthly_trend.png"
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)
    saved.append(str(p))

    # 03 Pareto with cumulative line
    top = pd.Series(f.amex_issues).head(8)
    cum_pct = top.cumsum() / f.amex_complaints * 100
    fig, ax1 = plt.subplots(figsize=(10, 5))
    x = range(len(top))
    short = [t[:30] + "…" if len(t) > 30 else t for t in top.index]
    ax1.bar(x, top.values, color=COLORS["navy"], alpha=0.85)
    ax1.set_xticks(x)
    ax1.set_xticklabels(short, rotation=45, ha="right", fontsize=7)
    ax1.set_ylabel("Complaints")
    ax2 = ax1.twinx()
    ax2.plot(x, cum_pct.values, color=COLORS["red"], marker="D", linewidth=2, label="Cumulative %")
    ax2.axhline(80, color=COLORS["amber"], linestyle="--", alpha=0.7, label="80% threshold")
    ax2.set_ylabel("Cumulative %")
    ax2.set_ylim(0, 105)
    ax1.set_title(f"Top 5 Issues = {f.pareto_top5_pct:.0f}% — Surgical Intervention Is Possible", fontweight="bold", color=COLORS["navy"])
    fig.tight_layout()
    p = CHARTS_DIR / "03_pareto_issues.png"
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)
    saved.append(str(p))

    # 04 Prepaid outlier
    others = f.prepaid_outlier_total - f.prepaid_outlier_amex
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar(["American Express", "All Other Peers"], [f.prepaid_outlier_amex, others],
           color=[COLORS["red"], COLORS["gray"]], width=0.5)
    ax.set_title(f"Prepaid Usability: Amex Holds {f.prepaid_outlier_pct:.0f}% of Industry Failures", fontweight="bold", color=COLORS["navy"])
    ax.set_ylabel("'Trouble Using Card' Complaints")
    for i, v in enumerate([f.prepaid_outlier_amex, others]):
        ax.text(i, v + 25, f"{v:,}", ha="center", fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    p = CHARTS_DIR / "04_prepaid_outlier.png"
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)
    saved.append(str(p))

    # 05 Issue YoY change
    if f.issue_yoy_changes:
        issues_sorted = sorted(f.issue_yoy_changes.items(), key=lambda x: x[1]["yoy_pct"], reverse=True)
        labels = [i[0][:25] + "…" if len(i[0]) > 25 else i[0] for i in issues_sorted]
        vals = [i[1]["yoy_pct"] for i in issues_sorted]
        colors_yoy = [COLORS["red"] if v > 0 else COLORS["green"] for v in vals]
        fig, ax = plt.subplots(figsize=(10, 4.5))
        ax.barh(labels[::-1], vals[::-1], color=colors_yoy[::-1])
        ax.axvline(0, color="black", linewidth=0.8)
        ax.set_xlabel("YoY Change (%) — Q1 2025 vs Q1 2026")
        ax.set_title("Credit Reporting and Prepaid Issues Are Growing Fastest", fontweight="bold", color=COLORS["navy"])
        ax.spines[["top", "right"]].set_visible(False)
        fig.tight_layout()
        p = CHARTS_DIR / "05_issue_yoy_change.png"
        fig.savefig(p, dpi=150, bbox_inches="tight")
        plt.close(fig)
        saved.append(str(p))

    # 06 Timely response benchmark
    timely = pd.Series(f.peer_benchmark_kpis["timely"]).sort_values(ascending=True)
    colors_t = [COLORS["amex"] if c == AMEX else COLORS["gray"] for c in timely.index]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(timely.index, timely.values, color=colors_t)
    ax.set_xlim(97.5, 100.2)
    ax.set_xlabel("Timely Response Rate (%)")
    ax.set_title("Timely Response Gap Is Minor — Invest in Prevention, Not Response Speed", fontweight="bold", color=COLORS["navy"])
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    p = CHARTS_DIR / "06_timely_benchmark.png"
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)
    saved.append(str(p))

    # 07 Geographic top states
    states = pd.Series(f.top_states)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(states.index, states.values, color=COLORS["amex"])
    ax.set_ylabel("Complaints")
    ax.set_title("Geographic Concentration: CA, FL, NY Drive 36% of Amex Complaints", fontweight="bold", color=COLORS["navy"])
    for i, v in enumerate(states.values):
        ax.text(i, v + 30, f"{v:,}", ha="center", fontsize=8)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    p = CHARTS_DIR / "07_top_states.png"
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)
    saved.append(str(p))

    # 08 Regulatory exposure
    reg = pd.Series(f.regulatory_exposure)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(reg.index, reg.values, color=[COLORS["red"], COLORS["amber"], COLORS["navy"]][:len(reg)])
    ax.set_ylabel("Amex Complaints")
    ax.set_title("FCRA Dominates Regulatory Exposure (3,236 Complaints)", fontweight="bold", color=COLORS["navy"])
    for i, v in enumerate(reg.values):
        ax.text(i, v + 30, f"{v:,}", ha="center", fontsize=9, fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    p = CHARTS_DIR / "08_regulatory_exposure.png"
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)
    saved.append(str(p))

    # 09 Product mix (replace old pie)
    products = pd.Series(f.amex_products).head(5)
    fig, ax = plt.subplots(figsize=(8, 5))
    wedges, texts, autotexts = ax.pie(
        products.values,
        labels=[f"{k.split()[0]}\n({v/f.amex_complaints*100:.0f}%)" for k, v in products.items()],
        autopct="%1.0f%%",
        colors=[COLORS["amex"], COLORS["navy"], COLORS["red"], COLORS["amber"], COLORS["gray"]],
        textprops={"fontsize": 8},
    )
    ax.set_title("Three Product Clusters Drive 83% of Amex Complaints", fontweight="bold", color=COLORS["navy"])
    p = CHARTS_DIR / "09_product_clusters.png"
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)
    saved.append(str(p))

    return saved
