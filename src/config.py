"""Project configuration and constants."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_DATA = ROOT / "data" / "raw" / "CFPB Complaints Data - Jan25 to Mar26.xlsx"
CLEAN_DATA = ROOT / "data" / "processed" / "complaints_cleaned.csv"
METRICS_PATH = ROOT / "data" / "processed" / "eda_metrics.json"
CHARTS_DIR = ROOT / "reports" / "charts"
REPORTS_DIR = ROOT / "reports"
SQL_DIR = ROOT / "sql"
EXCEL_PATH = REPORTS_DIR / "CFPB_Executive_Analytics.xlsx"

AMEX = "American Express"
PEERS = [
    "Capital One", "JPMorgan Chase", "Citibank", "Wells Fargo",
    "Bank of America", "Synchrony Financial", "U.S. Bank", "Barclays",
]

COLORS = {
    "amex": "#006FCF",
    "navy": "#00175A",
    "red": "#C41230",
    "green": "#2E7D32",
    "amber": "#F5A623",
    "gray": "#B0BEC5",
    "light_blue": "#E8F4FD",
}

CHART_STYLE = {
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": "#CCCCCC",
    "axes.labelcolor": "#333333",
    "xtick.color": "#333333",
    "ytick.color": "#333333",
    "font.family": "sans-serif",
    "font.size": 10,
}
