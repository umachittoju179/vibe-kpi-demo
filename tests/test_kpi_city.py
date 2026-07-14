from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.etl_load_sqlite import load_csv_to_sqlite
from src.kpi_city import city_kpi


@pytest.fixture(autouse=True)
def setup_db():
    load_csv_to_sqlite()
    yield


def test_city_kpi_happy_path():
    result = city_kpi("Mumbai")

    assert result["customer_count"] == 3
    assert result["avg_monthly_spend"] == 1200.0
    assert result["churn_rate"] == 0.33


def test_city_kpi_injection_attempt_is_safe():
    result = city_kpi("Mumbai' OR 1=1 --")

    assert result["customer_count"] == 0
    assert result["avg_monthly_spend"] is None
    assert result["churn_rate"] is None
