from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "db" / "analytics.db"


def city_kpi(city: str) -> dict:
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.execute(
            """
            SELECT COUNT(*), AVG(monthly_spend), AVG(churned)
            FROM customers_raw
            WHERE city = ?
            """,
            (city,),
        )
        row = cursor.fetchone()
    finally:
        conn.close()

    if row is None:
        return {"customer_count": 0, "avg_monthly_spend": None, "churn_rate": None}

    customer_count, avg_monthly_spend, churn_rate = row
    return {
        "customer_count": int(customer_count or 0),
        "avg_monthly_spend": round(float(avg_monthly_spend), 2) if avg_monthly_spend is not None else None,
        "churn_rate": round(float(churn_rate), 2) if churn_rate is not None else None,
    }


if __name__ == "__main__":
    print(city_kpi("Mumbai"))
    print(city_kpi("Mumbai' OR 1=1 --"))
