import pytest
from decimal import Decimal
from datetime import date
from freezegun import freeze_time
from app.modules.expense.expense_service import ExpenseService
from app.modules.expense.types import ExpenseCreateParams, ExpenseUpdateParams
from app.modules.expense.errors import (
    ExpenseNotFoundError,
    ExpenseAmountError,
    ExpenseFutureDateError,
    ExpenseBlankDescriptionError,
)
from app.application.errors import NotFoundError
from tests.conftest import CategoryFactory, BudgetFactory, ExpenseFactory

service = ExpenseService()


def test_create_expense_success():
    category = CategoryFactory()
    expense, warnings = service.create_expense(ExpenseCreateParams(
        category_id=category.id,
        amount=Decimal("25.50"),
        description="Lunch",
        date=date.today(),
    ))
    assert expense.id is not None
    assert expense.amount == Decimal("25.50")
    assert warnings == {}


def test_get_expense_raises_not_found():
    with pytest.raises(ExpenseNotFoundError):
        service.get_expense(99999)


def test_BR_EXP_01_amount_must_be_positive():
    category = CategoryFactory()
    with pytest.raises(ExpenseAmountError) as exc_info:
        service.create_expense(ExpenseCreateParams(
            category_id=category.id, amount=Decimal("0"), description="desc", date=date.today()
        ))
    assert "BR-EXP-01" in str(exc_info.value.details)


def test_BR_EXP_01_negative_amount_rejected():
    category = CategoryFactory()
    with pytest.raises(ExpenseAmountError):
        service.create_expense(ExpenseCreateParams(
            category_id=category.id, amount=Decimal("-10"), description="desc", date=date.today()
        ))


@freeze_time("2025-03-15")
def test_BR_EXP_02_future_date_rejected():
    category = CategoryFactory()
    with pytest.raises(ExpenseFutureDateError) as exc_info:
        service.create_expense(ExpenseCreateParams(
            category_id=category.id, amount=Decimal("10"), description="desc", date=date(2025, 3, 16)
        ))
    assert "BR-EXP-02" in str(exc_info.value.details)


@freeze_time("2025-03-15")
def test_BR_EXP_02_today_is_allowed():
    category = CategoryFactory()
    expense, _ = service.create_expense(ExpenseCreateParams(
        category_id=category.id, amount=Decimal("10"), description="desc", date=date(2025, 3, 15)
    ))
    assert expense.date == date(2025, 3, 15)


def test_BR_EXP_03_invalid_category_raises_not_found():
    with pytest.raises(NotFoundError):
        service.create_expense(ExpenseCreateParams(
            category_id=99999, amount=Decimal("10"), description="desc", date=date.today()
        ))


def test_BR_EXP_04_blank_description_rejected():
    category = CategoryFactory()
    with pytest.raises(ExpenseBlankDescriptionError) as exc_info:
        service.create_expense(ExpenseCreateParams(
            category_id=category.id, amount=Decimal("10"), description="   ", date=date.today()
        ))
    assert "BR-EXP-04" in str(exc_info.value.details)


def test_BR_EXP_04_description_stripped():
    category = CategoryFactory()
    expense, _ = service.create_expense(ExpenseCreateParams(
        category_id=category.id, amount=Decimal("10"), description="  hello  ", date=date.today()
    ))
    assert expense.description == "hello"


def test_BR_EXP_05_over_budget_warning():
    category = CategoryFactory()
    today = date.today()
    BudgetFactory(category=category, year=today.year, month=today.month, amount=Decimal("100"))
    # First expense: under budget, no warning
    _, first_warnings = service.create_expense(ExpenseCreateParams(
        category_id=category.id, amount=Decimal("50"), description="half", date=today
    ))
    assert not first_warnings.get("over_budget")
    # Second expense: pushes over budget
    _, second_warnings = service.create_expense(ExpenseCreateParams(
        category_id=category.id, amount=Decimal("60"), description="over", date=today
    ))
    assert second_warnings.get("over_budget") is True


def test_BR_EXP_05_no_budget_no_warning():
    category = CategoryFactory()
    _, warnings = service.create_expense(ExpenseCreateParams(
        category_id=category.id, amount=Decimal("999"), description="no budget", date=date.today()
    ))
    assert warnings == {}


def test_get_expenses_pagination():
    category = CategoryFactory()
    today = date.today()
    for i in range(5):
        ExpenseFactory(category=category, amount=Decimal("10"), description=f"exp {i}", date=today)
    expenses, total = service.get_expenses(page=1, per_page=3)
    assert total >= 5
    assert len(expenses) == 3


def test_delete_expense():
    expense = ExpenseFactory()
    expense_id = expense.id
    service.delete_expense(expense_id)
    with pytest.raises(ExpenseNotFoundError):
        service.get_expense(expense_id)


def test_update_expense_fields():
    category = CategoryFactory()
    expense = ExpenseFactory(category=category, amount=Decimal("10.00"), description="Original")
    updated, warnings = service.update_expense(
        expense.id,
        ExpenseUpdateParams(amount=Decimal("99.99"), description="Updated"),
    )
    assert updated.amount == Decimal("99.99")
    assert updated.description == "Updated"
    assert warnings == {}


def test_BR_EXP_01_update_zero_amount_rejected():
    expense = ExpenseFactory()
    with pytest.raises(ExpenseAmountError):
        service.update_expense(expense.id, ExpenseUpdateParams(amount=Decimal("0")))


@freeze_time("2025-03-15")
def test_BR_EXP_02_update_future_date_rejected():
    expense = ExpenseFactory(date=date(2025, 3, 15))
    with pytest.raises(ExpenseFutureDateError):
        service.update_expense(expense.id, ExpenseUpdateParams(date=date(2025, 3, 16)))


def test_BR_EXP_04_update_blank_description_rejected():
    expense = ExpenseFactory()
    with pytest.raises(ExpenseBlankDescriptionError):
        service.update_expense(expense.id, ExpenseUpdateParams(description="   "))


def test_BR_EXP_05_over_budget_warning_on_update():
    category = CategoryFactory()
    today = date.today()
    BudgetFactory(category=category, year=today.year, month=today.month, amount=Decimal("100"))
    expense = ExpenseFactory(category=category, amount=Decimal("50"), date=today)
    # Updating to an amount that exceeds the budget should return a warning
    _, warnings = service.update_expense(
        expense.id,
        ExpenseUpdateParams(amount=Decimal("150")),
    )
    assert warnings.get("over_budget") is True
