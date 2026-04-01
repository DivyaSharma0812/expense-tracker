import pytest
from decimal import Decimal
from app.modules.budget.budget_service import BudgetService
from app.modules.budget.types import BudgetCreateParams, BudgetUpdateParams
from app.modules.budget.errors import BudgetNotFoundError, BudgetAmountError, DuplicateBudgetError
from app.application.errors import NotFoundError
from tests.conftest import CategoryFactory, BudgetFactory

service = BudgetService()


def test_create_budget_success():
    category = CategoryFactory()
    budget = service.create_budget(BudgetCreateParams(
        category_id=category.id, year=2025, month=3, amount=Decimal("500")
    ))
    assert budget.id is not None
    assert budget.amount == Decimal("500")


def test_get_budget_raises_not_found():
    with pytest.raises(BudgetNotFoundError):
        service.get_budget(99999)


def test_BR_BUD_01_amount_must_be_positive():
    category = CategoryFactory()
    with pytest.raises(BudgetAmountError) as exc_info:
        service.create_budget(BudgetCreateParams(
            category_id=category.id, year=2025, month=3, amount=Decimal("0")
        ))
    assert "BR-BUD-01" in str(exc_info.value.details)


def test_BR_BUD_01_negative_amount_rejected():
    category = CategoryFactory()
    with pytest.raises(BudgetAmountError):
        service.create_budget(BudgetCreateParams(
            category_id=category.id, year=2025, month=3, amount=Decimal("-100")
        ))


def test_BR_BUD_04_duplicate_budget_rejected():
    category = CategoryFactory()
    service.create_budget(BudgetCreateParams(category_id=category.id, year=2025, month=3, amount=Decimal("200")))
    with pytest.raises(DuplicateBudgetError) as exc_info:
        service.create_budget(BudgetCreateParams(category_id=category.id, year=2025, month=3, amount=Decimal("300")))
    assert "BR-BUD-04" in str(exc_info.value.details)


def test_BR_BUD_04_different_month_allowed():
    category = CategoryFactory()
    budget_march = service.create_budget(BudgetCreateParams(
        category_id=category.id, year=2025, month=3, amount=Decimal("200")
    ))
    budget_april = service.create_budget(BudgetCreateParams(
        category_id=category.id, year=2025, month=4, amount=Decimal("300")
    ))
    assert budget_march.id != budget_april.id


def test_BR_BUD_05_invalid_category_rejected():
    with pytest.raises(NotFoundError):
        service.create_budget(BudgetCreateParams(
            category_id=99999, year=2025, month=3, amount=Decimal("100")
        ))


def test_update_budget_amount():
    budget = BudgetFactory(amount=Decimal("200"))
    updated = service.update_budget(budget.id, BudgetUpdateParams(amount=Decimal("350")))
    assert updated.amount == Decimal("350")


def test_update_budget_BR_BUD_01_zero_rejected():
    budget = BudgetFactory()
    with pytest.raises(BudgetAmountError):
        service.update_budget(budget.id, BudgetUpdateParams(amount=Decimal("0")))


def test_delete_budget():
    budget = BudgetFactory()
    budget_id = budget.id
    service.delete_budget(budget_id)
    with pytest.raises(BudgetNotFoundError):
        service.get_budget(budget_id)


def test_get_budgets_filter_by_month():
    category = CategoryFactory()
    service.create_budget(BudgetCreateParams(category_id=category.id, year=2025, month=1, amount=Decimal("100")))
    service.create_budget(BudgetCreateParams(category_id=category.id, year=2025, month=2, amount=Decimal("200")))
    budgets = service.get_budgets(year=2025, month=1)
    assert len(budgets) == 1
    assert budgets[0].month == 1
