"""Validate executive metrics against cleaned dataset."""
import pandas as pd

df = pd.read_csv("data/processed/complaints_cleaned.csv", parse_dates=["Date received"])
amex = df[df["Company"] == "American Express"]

print("=== DATASET ===")
print(f"Total: {len(df):,} | Amex: {len(amex):,} | Share: {len(amex)/len(df)*100:.1f}%")
print(f"Date range: {df['Date received'].min()} to {df['Date received'].max()}")
print(f"Companies: {df['Company'].nunique()}")

print("\n=== COMPETITIVE RANK ===")
co = df["Company"].value_counts()
for i, (c, v) in enumerate(co.items(), 1):
    tag = " <-- AMEX" if c == "American Express" else ""
    print(f"{i}. {c}: {v:,} ({v/len(df)*100:.1f}%){tag}")

print("\n=== AMEX PRODUCT CLUSTERS ===")
for p, v in amex["Product"].value_counts().items():
    print(f"  {p}: {v:,} ({v/len(amex)*100:.1f}%)")

print("\n=== TOP 8 ISSUES ===")
issues = amex["Issue"].value_counts()
for i, (iss, cnt) in enumerate(issues.head(8).items(), 1):
    print(f"{i}. {iss}: {cnt:,} ({cnt/len(amex)*100:.1f}%)")
print(f"Top 5 Pareto: {issues.head(5).sum()/len(amex)*100:.1f}%")

print("\n=== PREPAID OUTLIER ===")
tuc_amex = len(amex[amex["Issue"] == "Trouble using the card"])
tuc_all = len(df[df["Issue"] == "Trouble using the card"])
print(f"Trouble using card - Amex: {tuc_amex:,} | Industry: {tuc_all:,} | Share: {tuc_amex/tuc_all*100:.1f}%")
pc_tuc = len(amex[(amex["Issue"] == "Trouble using the card") & (amex["Product"] == "Prepaid card")])
print(f"Prepaid card subset: {pc_tuc:,} ({pc_tuc/tuc_amex*100:.1f}% of Amex TUC)")

print("\n=== YOY TREND ===")
q1_25 = len(amex[(amex["Complaint Year"] == 2025) & (amex["Complaint Quarter"] == 1)])
q1_26 = len(amex[(amex["Complaint Year"] == 2026) & (amex["Complaint Quarter"] == 1)])
print(f"Q1 2025: {q1_25:,} | Q1 2026: {q1_26:,} | YoY: {(q1_26-q1_25)/q1_25*100:+.1f}%")
aug25 = len(amex[(amex["Complaint Year"] == 2025) & (amex["Complaint Month"] == 8)])
mar26 = len(amex[(amex["Complaint Year"] == 2026) & (amex["Complaint Month"] == 3)])
print(f"Aug 2025: {aug25:,} | Mar 2026: {mar26:,} | Change: {(mar26-aug25)/aug25*100:+.1f}%")

print("\n=== OPERATIONAL KPIs ===")
timely = df.groupby("Company")["Timely Response Flag"].mean() * 100
print(f"Amex timely: {timely['American Express']:.1f}% | Peer avg: {timely.drop('American Express').mean():.1f}%")
resp = amex["Company response to consumer"].value_counts(normalize=True) * 100
for r, p in resp.head(4).items():
    print(f"  {r}: {p:.1f}%")

print("\n=== TOP STATES (all vs filtered) ===")
print("All states:")
for s, v in amex["State"].value_counts().head(5).items():
    print(f"  {s}: {v:,}")
print("Excluding 'Not specified':")
for s, v in amex[amex["State"] != "Not specified"]["State"].value_counts().head(5).items():
    print(f"  {s}: {v:,}")

print("\n=== SUB-ISSUE: UNRESOLVED DISPUTES ===")
sub = amex[amex["Issue"] == "Problem with a purchase shown on your statement"]["Sub-issue"].value_counts()
print(sub.head(5))
