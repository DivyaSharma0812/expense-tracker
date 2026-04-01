import pytest
from decimal import Decimal
from datetime import date
from freezegun import freeze_time
from app.modules.dashboard.dashboard_service import DashboardService
from tests.conftest import CategoryFactory, ExpenseFactory, BudgetFactory

service = DashboardService()


@freeze_time("2025-03-15")
def test_summary_defaults_to_current_month():
    summary = service.get_summary()
    assert summary["year"] == 2025
    assert summary["month"] == 3


def test_summary_empty_month():
    summary = service.get_summary(year=2024, month=1)
    assert Decimal(summary["total_spent"]) == Decimal("0")
    assert summary["categories"] == []


def test_summary_with_expenses_and_budget():
    cat = CategoryFactory(name="Food")
    BudgetFactory(category=cat, year=2025, month=3, amount=Decimal("500"))
    ExpenseFactory(category=cat, amount=Decimal("100"), description="e1", date=date(2025, 3, 10))
    ExpenseFactory(category=cat, amount=Decimal("150"), description="e2", date=date(2025, 3, 15))

    summary = service.get_summary(year=2025, month=3)
    assert Decimal(summary["total_spent"]) == Decimal("250")
    assert Decimal(summary["total_budgeted"]) == Decimal("500")
    assert len(summary["categories"]) == 1

    cat_data = summary["categories"][0]
    assert Decimal(cat_data["spent"]) == Decimal("250")
    assert Decimal(cat_data["budgeted"]) == Decimal("500")
    assert cat_data["is_over_budget"] is False
    assert cat_data["expense_count"] == 2


def test_summary_over_budget_flag():
    cat = CategoryFactory(name="Over Budget Cat")
    BudgetFactory(category=cat, year=2025, month=6, amount=Decimal("100"))
    ExpenseFactory(category=cat, amount=Decimal("150"), description="over", date=date(2025, 6, 10))

    summary = service.get_summary(year=2025, month=6)
    cat_data = summary["categories"][0]
    assert cat_data["is_over_budget"] is True
    assert summary["categories_over_budget"] == 1


def test_summary_unbudgeted_spending():
    cat = CategoryFactory(name="Unbudgeted Cat")
    ExpenseFactory(category=cat, amount=Decimal("75"), description="misc", date=date(2025, 7, 5))

    summary = service.get_summary(year=2025, month=7)
    assert Decimal(summary["unbudgeted_spending"]) == Decimal("75")


def test_summary_unbudgeted_spending_percent_used_is_none():
    cat = CategoryFactory(name="No Budget Cat")
    ExpenseFactory(category=cat, amount=Decimal("75"), description="misc", date=date(2025, 8, 5))

    summary = service.get_summary(year=2025, month=8)
    cat_data = summary["categories"][0]
    assert cat_data["percent_used"] is None
    assert Decimal(cat_data["spent"]) == Decimal("75")


def test_trends_returns_months():
    cat = CategoryFactory(name="Trend Cat")
    for m in [1, 2, 3]:
        ExpenseFactory(
            category=cat,
            amount=Decimal("100"),
            description=f"month {m}",
            date=date(2025, m, 15),
        )
    trends = service.get_trends(months=6)
    assert len(trends) <= 6
    years_months = [(t["year"], t["month"]) for t in trends]
    assert (2025, 1) in years_months
    assert (2025, 2) in years_months
    assert (2025, 3) in years_months


def test_trends_capped_at_24():
    trends = service.get_trends(months=100)
    assert len(trends) <= 24
