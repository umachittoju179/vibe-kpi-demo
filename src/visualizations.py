"""
Visualization module for KPI analysis across cities.
Creates charts for customer metrics, spending, and churn rates.
"""

from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "db" / "analytics.db"
OUTPUT_DIR = BASE_DIR / "visualizations"


def load_data() -> pd.DataFrame:
    """Load customer data from SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM customers_raw", conn)
    conn.close()
    return df


def create_output_dir():
    """Create output directory for visualizations."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def plot_customer_count_by_city(df: pd.DataFrame):
    """Create bar chart of customer count by city."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    customer_counts = df.groupby("city").size()
    customer_counts.plot(kind="bar", ax=ax, color="steelblue", edgecolor="black")
    
    ax.set_title("Customer Count by City", fontsize=16, fontweight="bold")
    ax.set_xlabel("City", fontsize=12)
    ax.set_ylabel("Number of Customers", fontsize=12)
    ax.grid(axis="y", alpha=0.3)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    
    plt.savefig(OUTPUT_DIR / "customer_count_by_city.png", dpi=300, bbox_inches="tight")
    print("✓ Saved: customer_count_by_city.png")
    plt.close()


def plot_avg_spend_by_city(df: pd.DataFrame):
    """Create bar chart of average monthly spend by city."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    avg_spend = df.groupby("city")["monthly_spend"].mean().sort_values(ascending=False)
    avg_spend.plot(kind="bar", ax=ax, color="green", edgecolor="black", alpha=0.7)
    
    ax.set_title("Average Monthly Spend by City", fontsize=16, fontweight="bold")
    ax.set_xlabel("City", fontsize=12)
    ax.set_ylabel("Average Spend ($)", fontsize=12)
    ax.grid(axis="y", alpha=0.3)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    
    plt.savefig(OUTPUT_DIR / "avg_spend_by_city.png", dpi=300, bbox_inches="tight")
    print("✓ Saved: avg_spend_by_city.png")
    plt.close()


def plot_churn_rate_by_city(df: pd.DataFrame):
    """Create bar chart of churn rate by city."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    churn_rate = (df.groupby("city")["churned"].sum() / df.groupby("city").size() * 100).sort_values(ascending=False)
    colors = ["red" if rate > 40 else "orange" if rate > 25 else "green" for rate in churn_rate]
    churn_rate.plot(kind="bar", ax=ax, color=colors, edgecolor="black")
    
    ax.set_title("Churn Rate by City", fontsize=16, fontweight="bold")
    ax.set_xlabel("City", fontsize=12)
    ax.set_ylabel("Churn Rate (%)", fontsize=12)
    ax.set_ylim(0, 100)
    ax.grid(axis="y", alpha=0.3)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    
    plt.savefig(OUTPUT_DIR / "churn_rate_by_city.png", dpi=300, bbox_inches="tight")
    print("✓ Saved: churn_rate_by_city.png")
    plt.close()


def plot_spend_vs_churn(df: pd.DataFrame):
    """Create scatter plot of monthly spend vs churn status by city."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = {"Churned": "red", "Retained": "green"}
    churn_labels = df["churned"].map({1: "Churned", 0: "Retained"})
    
    for label, group in df.groupby(churn_labels):
        ax.scatter(
            group["monthly_spend"],
            group.index,
            label=label,
            alpha=0.6,
            s=100,
            color=colors[label],
            edgecolor="black"
        )
    
    ax.set_title("Monthly Spend vs Customer Status", fontsize=16, fontweight="bold")
    ax.set_xlabel("Monthly Spend ($)", fontsize=12)
    ax.set_ylabel("Customer ID", fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    
    plt.savefig(OUTPUT_DIR / "spend_vs_churn.png", dpi=300, bbox_inches="tight")
    print("✓ Saved: spend_vs_churn.png")
    plt.close()


def plot_dashboard(df: pd.DataFrame):
    """Create a comprehensive dashboard with multiple KPI visualizations."""
    fig = plt.figure(figsize=(16, 12))
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
    
    # 1. Customer count by city
    ax1 = fig.add_subplot(gs[0, 0])
    customer_counts = df.groupby("city").size()
    customer_counts.plot(kind="bar", ax=ax1, color="steelblue", edgecolor="black")
    ax1.set_title("Customer Count by City", fontsize=12, fontweight="bold")
    ax1.set_ylabel("Count")
    ax1.grid(axis="y", alpha=0.3)
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha="right")
    
    # 2. Average spend by city
    ax2 = fig.add_subplot(gs[0, 1])
    avg_spend = df.groupby("city")["monthly_spend"].mean().sort_values(ascending=False)
    avg_spend.plot(kind="bar", ax=ax2, color="green", edgecolor="black", alpha=0.7)
    ax2.set_title("Average Monthly Spend by City", fontsize=12, fontweight="bold")
    ax2.set_ylabel("Average Spend ($)")
    ax2.grid(axis="y", alpha=0.3)
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha="right")
    
    # 3. Churn rate by city
    ax3 = fig.add_subplot(gs[1, 0])
    churn_rate = (df.groupby("city")["churned"].sum() / df.groupby("city").size() * 100).sort_values(ascending=False)
    colors = ["red" if rate > 40 else "orange" if rate > 25 else "green" for rate in churn_rate]
    churn_rate.plot(kind="bar", ax=ax3, color=colors, edgecolor="black")
    ax3.set_title("Churn Rate by City (%)", fontsize=12, fontweight="bold")
    ax3.set_ylabel("Churn Rate (%)")
    ax3.set_ylim(0, 100)
    ax3.grid(axis="y", alpha=0.3)
    plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha="right")
    
    # 4. Distribution of monthly spend
    ax4 = fig.add_subplot(gs[1, 1])
    df["monthly_spend"].hist(bins=15, ax=ax4, color="skyblue", edgecolor="black")
    ax4.set_title("Distribution of Monthly Spend", fontsize=12, fontweight="bold")
    ax4.set_xlabel("Monthly Spend ($)")
    ax4.set_ylabel("Frequency")
    ax4.grid(axis="y", alpha=0.3)
    
    # 5. Spend by city (box plot)
    ax5 = fig.add_subplot(gs[2, 0])
    df.boxplot(column="monthly_spend", by="city", ax=ax5)
    ax5.set_title("Monthly Spend Distribution by City", fontsize=12, fontweight="bold")
    ax5.set_xlabel("City")
    ax5.set_ylabel("Monthly Spend ($)")
    plt.sca(ax5)
    plt.xticks(rotation=45, ha="right")
    
    # 6. Key metrics summary (text)
    ax6 = fig.add_subplot(gs[2, 1])
    ax6.axis("off")
    
    total_customers = len(df)
    total_churned = df["churned"].sum()
    overall_churn_rate = (total_churned / total_customers * 100)
    avg_spend_all = df["monthly_spend"].mean()
    
    summary_text = f"""
KEY METRICS SUMMARY

Total Customers: {total_customers}
Total Churned: {total_churned}
Overall Churn Rate: {overall_churn_rate:.1f}%
Average Monthly Spend: ${avg_spend_all:.2f}

Top Cities by Customer Count:
"""
    
    for city, count in customer_counts.nlargest(3).items():
        summary_text += f"\n  • {city}: {count} customers"
    
    ax6.text(0.1, 0.5, summary_text, fontsize=11, family="monospace", 
             verticalalignment="center", bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))
    
    fig.suptitle("KPI Analytics Dashboard", fontsize=18, fontweight="bold", y=0.995)
    plt.savefig(OUTPUT_DIR / "kpi_dashboard.png", dpi=300, bbox_inches="tight")
    print("✓ Saved: kpi_dashboard.png")
    plt.close()


def generate_all_visualizations():
    """Generate all visualizations."""
    print("\n📊 Generating KPI Visualizations...\n")
    
    create_output_dir()
    df = load_data()
    
    print(f"Loaded {len(df)} customer records from database\n")
    
    plot_customer_count_by_city(df)
    plot_avg_spend_by_city(df)
    plot_churn_rate_by_city(df)
    plot_spend_vs_churn(df)
    plot_dashboard(df)
    
    print(f"\n✅ All visualizations saved to: {OUTPUT_DIR}\n")


if __name__ == "__main__":
    generate_all_visualizations()
