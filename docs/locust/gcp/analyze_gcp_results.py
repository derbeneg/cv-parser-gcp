#!/usr/bin/env python3
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick # For percentage formatting
import seaborn as sns # Import seaborn

# Map folder → human-readable label
SCENARIOS = {
    "no_hpa":   "No HPA (10u_2r)",
    "hpa":      "HPA @50% (10u_2r)",
    "hpa2":     "HPA minPods=20 (10u_1r)",
}

BASE_DIR = os.path.join(os.path.dirname(__file__))

records = []
for sub, label in SCENARIOS.items():
    stats_csv = glob.glob(os.path.join(BASE_DIR, sub, "*_stats.csv"))
    if not stats_csv:
        print(f"⚠️  no stats.csv found in {sub}, skipping")
        continue
    df = pd.read_csv(stats_csv[0])
    # pick the Aggregated row if present, otherwise last row
    if "Name" in df.columns and "Aggregated" in df["Name"].values:
        agg = df[df["Name"] == "Aggregated"].iloc[0]
    else:
        agg = df.iloc[-1]

    # Use the exact column names from your _stats.csv file
    reqs_col     = "Request Count"
    fails_col    = "Failure Count"
    med_col      = "Median Response Time"
    reqs_sec_col = "Requests/s"

    total = int(agg[reqs_col])
    fails = int(agg[fails_col])
    med   = float(agg[med_col])
    rps   = float(agg[reqs_sec_col])

    records.append({
        "scenario":    label,
        "requests":    total,
        "failures":    fails,
        "failure_pct": fails / total * 100 if total > 0 else 0, # Handle division by zero
        "median_ms":   med,
        "req_per_s":   rps,
    })

# build dataframe
results = pd.DataFrame(records) # Keep 'scenario' as a column for seaborn plotting

# Set a consistent style for Seaborn plots
sns.set_theme(style="whitegrid", palette="pastel")

# --- Plot median latency ---
plt.figure(figsize=(9, 6)) # Larger figure for more space
ax1 = sns.barplot(x="scenario", y="median_ms", data=results, palette="Blues_d") # Blues_d for darker blues
plt.title("Median Response Time by Scenario", fontsize=16)
plt.ylabel("Latency (ms)", fontsize=13)
plt.xlabel("") # Remove x-axis label as scenarios are self-explanatory
plt.xticks(rotation=45, ha="right", fontsize=11) # Rotate for long labels
plt.yticks(fontsize=11)
# plt.grid(axis='y', linestyle='--', alpha=0.7) # Seaborn's whitegrid usually handles this well

# Add value labels on top of bars
for p in ax1.patches:
    ax1.annotate(f"{p.get_height():.0f}ms",
                 (p.get_x() + p.get_width() / 2., p.get_height()),
                 ha='center', va='center', xytext=(0, 10), textcoords='offset points',
                 fontsize=10, color='black')

plt.tight_layout() # Adjust layout to prevent labels from overlapping
plt.savefig(os.path.join(BASE_DIR, "median_latency.png"), dpi=300) # Higher DPI for better quality
plt.close()

# --- Plot failure rate ---
plt.figure(figsize=(9, 6)) # Consistent figure size
ax2 = sns.barplot(x="scenario", y="failure_pct", data=results, palette="Reds_d") # Reds_d for darker reds
plt.title("Failure Rate by Scenario", fontsize=16)
plt.ylabel("Failure %", fontsize=13)
plt.xlabel("")
plt.xticks(rotation=45, ha="right", fontsize=11)
plt.yticks(fontsize=11)
# plt.grid(axis='y', linestyle='--', alpha=0.7) # Seaborn's whitegrid usually handles this well

# Format y-axis as percentage
ax2.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100.0))

# Add value labels on top of bars
for p in ax2.patches:
    ax2.annotate(f"{p.get_height():.2f}%", # .2f for two decimal places
                 (p.get_x() + p.get_width() / 2., p.get_height()),
                 ha='center', va='center', xytext=(0, 10), textcoords='offset points',
                 fontsize=10, color='black')

plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, "failure_rate.png"), dpi=300) # Higher DPI for better quality
plt.close()

# --- Output summarized CSV ---
output_csv_path = os.path.join(BASE_DIR, "locust_gcp_summary.csv")
results.to_csv(output_csv_path, index=False) # Do not write the 'scenario' index as a column in CSV

print("\n✅ Charts written to:")
print("   ", os.path.join(BASE_DIR, "median_latency.png"))
print("   ", os.path.join(BASE_DIR, "failure_rate.png"))
print("\n✅ Summary CSV written to:")
print("   ", output_csv_path)