from datetime import date
from decimal import Decimal
from freezegun import freeze_time
from tests.conftest import CategoryFactory, ExpenseFactory, BudgetFactory


@freeze_time("2025-03-15")
def test_summary_defaults_to_current_month(client):
    res = client.get("/api/dashboard/summary")
    assert res.status_code == 200
    assert res.json["data"]["year"] == 2025
    assert res.json["data"]["month"] == 3


def test_summary_with_data(client):
    cat = CategoryFactory(name="Dash Cat")
    BudgetFactory(category=cat, year=2025, month=4, amount="300")
    ExpenseFactory(category=cat, amount="200", description="d", date=date(2025, 4, 10))
    res = client.get("/api/dashboard/summary?year=2025&month=4")
    assert res.status_code == 200
    data = res.json["data"]
    assert Decimal(data["total_spent"]) == Decimal("200")
    assert Decimal(data["total_budgeted"]) == Decimal("300")
    assert len(data["categories"]) == 1


def test_trends_endpoint(client):
    cat = CategoryFactory(name="Trends Cat")
    ExpenseFactory(category=cat, amount="50", description="t", date=date(2025, 2, 1))
    res = client.get("/api/dashboard/trends?months=3")
    assert res.status_code == 200
    assert isinstance(res.json["data"], list)


def test_summary_shape(client):
    res = client.get("/api/dashboard/summary?year=2030&month=1")
    assert res.status_code == 200
    data = res.json["data"]
    assert "total_spent" in data
    assert "total_budgeted" in data
    assert "remaining" in data
    assert "categories" in data
    assert "unbudgeted_spending" in data
    assert "categories_over_budget" in data
