from pathlib import Path
import sqlite3

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_CSV = BASE_DIR / "data" / "raw" / "customers_raw.csv"
DB_PATH = BASE_DIR / "data" / "db" / "analytics.db"


def load_csv_to_sqlite(csv_path: str | Path | None = None, db_path: str | Path | None = None) -> None:
    csv_path = Path(csv_path or RAW_CSV)
    db_path = Path(db_path or DB_PATH)

    db_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(csv_path)
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("DROP TABLE IF EXISTS customers_raw")
        conn.execute(
            """
            CREATE TABLE customers_raw (
                customer_id INTEGER,
                city TEXT,
                monthly_spend REAL,
                churned INTEGER
            )
            """
        )
        df.to_sql("customers_raw", conn, if_exists="append", index=False)
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    load_csv_to_sqlite()
