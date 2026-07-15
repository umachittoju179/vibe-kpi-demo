"""
Aggregate SQL Queries module.
Demonstrates COUNT, MAX, DISTINCT and other aggregation functions.
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


def query_count_basic():
    """Basic COUNT query."""
    query = """
    SELECT COUNT(*) as total_customers
    FROM customers_raw
    """
    return execute_query(query, "1. BASIC COUNT - Total Customers")


def query_count_by_city():
    """COUNT grouped by city."""
    query = """
    SELECT 
        city,
        COUNT(*) as customer_count
    FROM customers_raw
    GROUP BY city
    ORDER BY customer_count DESC
    """
    return execute_query(query, "2. COUNT BY CITY - Customers per City")


def query_count_distinct_cities():
    """COUNT DISTINCT cities."""
    query = """
    SELECT COUNT(DISTINCT city) as total_cities
    FROM customers_raw
    """
    return execute_query(query, "3. COUNT DISTINCT - Total Unique Cities")


def query_max_spend():
    """MAX spending."""
    query = """
    SELECT MAX(monthly_spend) as highest_spend
    FROM customers_raw
    """
    return execute_query(query, "4. MAX SPEND - Highest Monthly Spend")


def query_max_spend_by_city():
    """MAX spending by city."""
    query = """
    SELECT 
        city,
        MAX(monthly_spend) as max_spend
    FROM customers_raw
    GROUP BY city
    ORDER BY max_spend DESC
    """
    return execute_query(query, "5. MAX BY CITY - Highest Spend per City")


def query_max_spend_with_customer():
    """Find customer with MAX spend in each city."""
    query = """
    SELECT 
        city,
        customer_id,
        MAX(monthly_spend) as max_spend
    FROM customers_raw
    GROUP BY city
    ORDER BY max_spend DESC
    """
    return execute_query(query, "6. MAX SPEND CUSTOMER BY CITY")


def query_distinct_cities():
    """SELECT DISTINCT cities."""
    query = """
    SELECT DISTINCT city
    FROM customers_raw
    ORDER BY city
    """
    return execute_query(query, "7. DISTINCT CITIES - All Unique Cities")


def query_distinct_spend_levels():
    """DISTINCT spending levels."""
    query = """
    SELECT DISTINCT monthly_spend
    FROM customers_raw
    ORDER BY monthly_spend DESC
    """
    return execute_query(query, "8. DISTINCT SPENDING LEVELS")


def query_count_distinct_spend():
    """COUNT DISTINCT spending levels."""
    query = """
    SELECT COUNT(DISTINCT monthly_spend) as unique_spend_levels
    FROM customers_raw
    """
    return execute_query(query, "9. COUNT DISTINCT SPENDING LEVELS")


def query_count_churned():
    """COUNT customers by churn status."""
    query = """
    SELECT 
        CASE 
            WHEN churned = 1 THEN 'Churned'
            ELSE 'Retained'
        END as status,
        COUNT(*) as customer_count
    FROM customers_raw
    GROUP BY churned
    """
    return execute_query(query, "10. COUNT BY STATUS - Churned vs Retained")


def query_max_and_min_spend():
    """MAX and MIN spending."""
    query = """
    SELECT 
        MAX(monthly_spend) as max_spend,
        MIN(monthly_spend) as min_spend,
        COUNT(*) as total_customers
    FROM customers_raw
    """
    return execute_query(query, "11. MAX & MIN SPEND - Range Analysis")


def query_max_min_by_city():
    """MAX and MIN spending by city."""
    query = """
    SELECT 
        city,
        COUNT(*) as count,
        MAX(monthly_spend) as max_spend,
        MIN(monthly_spend) as min_spend,
        (MAX(monthly_spend) - MIN(monthly_spend)) as spend_range
    FROM customers_raw
    GROUP BY city
    ORDER BY spend_range DESC
    """
    return execute_query(query, "12. MAX/MIN SPEND BY CITY - Spending Range")


def query_count_and_distinct():
    """COUNT with DISTINCT."""
    query = """
    SELECT 
        COUNT(*) as total_records,
        COUNT(DISTINCT city) as unique_cities,
        COUNT(DISTINCT customer_id) as unique_customers,
        COUNT(DISTINCT monthly_spend) as unique_spend_values
    FROM customers_raw
    """
    return execute_query(query, "13. COUNT vs COUNT DISTINCT - Comparison")


def query_count_by_city_and_status():
    """COUNT grouped by city and status."""
    query = """
    SELECT 
        city,
        CASE WHEN churned = 1 THEN 'Churned' ELSE 'Retained' END as status,
        COUNT(*) as count
    FROM customers_raw
    GROUP BY city, churned
    ORDER BY city, churned DESC
    """
    return execute_query(query, "14. COUNT BY CITY & STATUS - Multi-level Grouping")


def query_max_count_city():
    """City with MAX customer count."""
    query = """
    SELECT 
        city,
        COUNT(*) as customer_count
    FROM customers_raw
    GROUP BY city
    HAVING COUNT(*) = (
        SELECT MAX(city_count)
        FROM (
            SELECT COUNT(*) as city_count
            FROM customers_raw
            GROUP BY city
        )
    )
    """
    return execute_query(query, "15. CITY WITH MAX CUSTOMER COUNT")


def query_distinct_and_count():
    """Complex: DISTINCT and COUNT together."""
    query = """
    SELECT 
        city,
        COUNT(DISTINCT customer_id) as unique_customers,
        COUNT(DISTINCT churned) as unique_statuses,
        COUNT(*) as total_rows
    FROM customers_raw
    GROUP BY city
    ORDER BY unique_customers DESC
    """
    return execute_query(query, "16. DISTINCT CUSTOMERS & COUNT BY CITY")


def query_customers_with_max_spend():
    """Find all customers with MAX spend."""
    query = """
    SELECT 
        customer_id,
        city,
        monthly_spend
    FROM customers_raw
    WHERE monthly_spend = (SELECT MAX(monthly_spend) FROM customers_raw)
    """
    return execute_query(query, "17. CUSTOMERS WITH HIGHEST SPEND")


def query_count_each_spend_amount():
    """COUNT how many customers at each spend level."""
    query = """
    SELECT 
        monthly_spend,
        COUNT(*) as customer_count
    FROM customers_raw
    GROUP BY monthly_spend
    ORDER BY monthly_spend DESC
    """
    return execute_query(query, "18. COUNT CUSTOMERS BY SPEND AMOUNT")


def query_count_cities_per_spend():
    """COUNT distinct cities for each spend amount."""
    query = """
    SELECT 
        monthly_spend,
        COUNT(DISTINCT city) as cities_with_this_spend
    FROM customers_raw
    GROUP BY monthly_spend
    ORDER BY monthly_spend DESC
    """
    return execute_query(query, "19. DISTINCT CITIES PER SPEND LEVEL")


def query_comprehensive_aggregation():
    """Comprehensive aggregation query."""
    query = """
    SELECT 
        'OVERALL' as segment,
        COUNT(*) as total_count,
        COUNT(DISTINCT city) as distinct_cities,
        COUNT(DISTINCT customer_id) as distinct_customers,
        MAX(monthly_spend) as max_spend,
        MIN(monthly_spend) as min_spend,
        COUNT(DISTINCT monthly_spend) as distinct_spend_levels,
        COUNT(DISTINCT CASE WHEN churned = 1 THEN customer_id END) as churned_customers
    FROM customers_raw
    """
    return execute_query(query, "20. COMPREHENSIVE AGGREGATION - All Functions")


def generate_all_aggregate_queries():
    """Generate all aggregate queries."""
    print("\n" + "="*80)
    print("🔍 SQL AGGREGATE FUNCTIONS: COUNT, MAX, DISTINCT")
    print("="*80)
    
    query_count_basic()
    query_count_by_city()
    query_count_distinct_cities()
    query_max_spend()
    query_max_spend_by_city()
    query_max_spend_with_customer()
    query_distinct_cities()
    query_distinct_spend_levels()
    query_count_distinct_spend()
    query_count_churned()
    query_max_and_min_spend()
    query_max_min_by_city()
    query_count_and_distinct()
    query_count_by_city_and_status()
    query_max_count_city()
    query_distinct_and_count()
    query_customers_with_max_spend()
    query_count_each_spend_amount()
    query_count_cities_per_spend()
    query_comprehensive_aggregation()
    
    print("\n" + "="*80)
    print("✅ ALL AGGREGATE QUERIES EXECUTED SUCCESSFULLY")
    print("="*80 + "\n")


if __name__ == "__main__":
    generate_all_aggregate_queries()
