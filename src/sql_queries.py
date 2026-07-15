"""
SQL Queries module for KPI analysis.
Generates detailed reports from the analytics database.
"""

from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "db" / "analytics.db"


def execute_query(query: str, description: str = "") -> pd.DataFrame:
    """Execute a SQL query and return results as DataFrame."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if description:
        print(f"\n{'='*80}")
        print(f"📊 {description}")
        print(f"{'='*80}\n")
    
    print(df.to_string(index=False))
    print()
    return df


def query_customer_count_by_city():
    """Get customer count grouped by city."""
    query = """
    SELECT 
        city,
        COUNT(*) as customer_count,
        ROUND(AVG(monthly_spend), 2) as avg_spend,
        ROUND(SUM(monthly_spend), 2) as total_spend,
        SUM(churned) as churned_count,
        ROUND(100.0 * SUM(churned) / COUNT(*), 2) as churn_rate_pct
    FROM customers_raw
    GROUP BY city
    ORDER BY customer_count DESC
    """
    return execute_query(query, "CUSTOMER METRICS BY CITY")


def query_churn_analysis():
    """Detailed churn analysis."""
    query = """
    SELECT 
        city,
        CASE 
            WHEN churned = 1 THEN 'Churned'
            ELSE 'Retained'
        END as status,
        COUNT(*) as count,
        ROUND(AVG(monthly_spend), 2) as avg_spend,
        MIN(monthly_spend) as min_spend,
        MAX(monthly_spend) as max_spend
    FROM customers_raw
    GROUP BY city, churned
    ORDER BY city, churned DESC
    """
    return execute_query(query, "CHURN ANALYSIS BY CITY AND STATUS")


def query_top_spenders():
    """Get top 10 customers by monthly spend."""
    query = """
    SELECT 
        customer_id,
        city,
        monthly_spend,
        CASE 
            WHEN churned = 1 THEN 'Churned'
            ELSE 'Retained'
        END as status
    FROM customers_raw
    ORDER BY monthly_spend DESC
    LIMIT 10
    """
    return execute_query(query, "TOP 10 HIGHEST SPENDERS")


def query_spend_distribution():
    """Get spending distribution statistics."""
    query = """
    SELECT 
        'Overall' as segment,
        COUNT(*) as total_customers,
        ROUND(MIN(monthly_spend), 2) as min_spend,
        ROUND(MAX(monthly_spend), 2) as max_spend,
        ROUND(AVG(monthly_spend), 2) as avg_spend,
        ROUND((SELECT monthly_spend FROM customers_raw ORDER BY monthly_spend LIMIT 1 OFFSET (COUNT(*)-1)/2) 
              FROM customers_raw, 2) as median_spend
    FROM customers_raw
    """
    return execute_query(query, "SPENDING DISTRIBUTION STATISTICS")


def query_city_performance():
    """Comprehensive city performance metrics."""
    query = """
    SELECT 
        city,
        COUNT(*) as total_customers,
        SUM(CASE WHEN churned = 1 THEN 1 ELSE 0 END) as lost_customers,
        SUM(CASE WHEN churned = 0 THEN 1 ELSE 0 END) as active_customers,
        ROUND(100.0 * SUM(CASE WHEN churned = 1 THEN 1 ELSE 0 END) / COUNT(*), 1) as churn_rate_pct,
        ROUND(SUM(monthly_spend), 2) as total_revenue,
        ROUND(AVG(monthly_spend), 2) as avg_revenue_per_customer
    FROM customers_raw
    GROUP BY city
    ORDER BY total_revenue DESC
    """
    return execute_query(query, "CITY PERFORMANCE RANKING")


def query_spending_segments():
    """Segment customers by spending level."""
    query = """
    SELECT 
        CASE 
            WHEN monthly_spend >= 1400 THEN 'Premium (≥$1400)'
            WHEN monthly_spend >= 1200 THEN 'Standard ($1200-$1399)'
            WHEN monthly_spend >= 1000 THEN 'Basic ($1000-$1199)'
            ELSE 'Economy (<$1000)'
        END as spending_segment,
        COUNT(*) as customer_count,
        ROUND(AVG(monthly_spend), 2) as avg_spend,
        SUM(churned) as churned_count,
        ROUND(100.0 * SUM(churned) / COUNT(*), 2) as churn_rate_pct
    FROM customers_raw
    GROUP BY spending_segment
    ORDER BY avg_spend DESC
    """
    return execute_query(query, "CUSTOMER SEGMENTATION BY SPENDING")


def query_high_risk_customers():
    """Identify high-risk customers (churned with decent spending)."""
    query = """
    SELECT 
        customer_id,
        city,
        monthly_spend,
        churned as status,
        'HIGH RISK' as risk_level
    FROM customers_raw
    WHERE churned = 1 AND monthly_spend >= 1000
    ORDER BY monthly_spend DESC
    """
    return execute_query(query, "HIGH-RISK CUSTOMERS (CHURNED WITH HIGH SPEND)")


def query_summary_statistics():
    """Get overall summary statistics."""
    query = """
    SELECT 
        'Database Summary' as metric,
        COUNT(*) as value
    FROM customers_raw
    
    UNION ALL
    
    SELECT 
        'Total Customers',
        COUNT(*)
    FROM customers_raw
    
    UNION ALL
    
    SELECT 
        'Total Churned',
        SUM(churned)
    FROM customers_raw
    
    UNION ALL
    
    SELECT 
        'Total Active',
        COUNT(*) - SUM(churned)
    FROM customers_raw
    
    UNION ALL
    
    SELECT 
        'Total Revenue ($)',
        ROUND(SUM(monthly_spend), 2)
    FROM customers_raw
    
    UNION ALL
    
    SELECT 
        'Unique Cities',
        COUNT(DISTINCT city)
    FROM customers_raw
    """
    return execute_query(query, "OVERALL SUMMARY STATISTICS")


def query_detailed_customer_report():
    """Get detailed customer report with all information."""
    query = """
    SELECT 
        customer_id,
        city,
        monthly_spend,
        CASE 
            WHEN churned = 1 THEN 'Churned'
            ELSE 'Retained'
        END as status,
        CASE 
            WHEN monthly_spend >= 1400 THEN 'Premium'
            WHEN monthly_spend >= 1200 THEN 'Standard'
            WHEN monthly_spend >= 1000 THEN 'Basic'
            ELSE 'Economy'
        END as segment
    FROM customers_raw
    ORDER BY monthly_spend DESC
    """
    return execute_query(query, "DETAILED CUSTOMER REPORT")


def generate_all_reports():
    """Generate all SQL query reports."""
    print("\n" + "="*80)
    print("🔍 KPI SQL QUERY ANALYSIS REPORTS")
    print("="*80)
    
    # Execute all queries
    query_summary_statistics()
    query_customer_count_by_city()
    query_city_performance()
    query_spending_segments()
    query_churn_analysis()
    query_top_spenders()
    query_high_risk_customers()
    query_detailed_customer_report()
    
    print("\n" + "="*80)
    print("✅ ALL REPORTS GENERATED SUCCESSFULLY")
    print("="*80 + "\n")


if __name__ == "__main__":
    generate_all_reports()
