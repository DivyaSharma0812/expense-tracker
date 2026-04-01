import logging
from datetime import date
from decimal import Decimal
from typing import Optional, TYPE_CHECKING

from ...extensions import database
from .expense_repository import ExpenseRepository
from .expense_model import Expense
from .errors import (
    ExpenseNotFoundError,
    ExpenseAmountError,
    ExpenseFutureDateError,
    ExpenseBlankDescriptionError,
)
from .types import ExpenseCreateParams, ExpenseUpdateParams

if TYPE_CHECKING:
    from ..category.category_service import CategoryService
    from ..budget.budget_repository import BudgetRepository

logger = logging.getLogger(__name__)


class ExpenseService:
    def __init__(
        self,
        repository: Optional[ExpenseRepository] = None,
        category_service: Optional["CategoryService"] = None,
        budget_repository: Optional["BudgetRepository"] = None,
    ):
        self._repo = repository or ExpenseRepository()
        self._category_service = category_service
        self._budget_repository = budget_repository

    def _get_category_service(self) -> "CategoryService":
        if self._category_service is None:
            from ..category.category_service import CategoryService
            self._category_service = CategoryService()
        return self._category_service

    def _get_budget_repository(self) -> "BudgetRepository":
        if self._budget_repository is None:
            from ..budget.budget_repository import BudgetRepository
            self._budget_repository = BudgetRepository()
        return self._budget_repository

    def get_expenses(
        self,
        page: int = 1,
        per_page: int = 20,
        category_id: Optional[int] = None,
        year: Optional[int] = None,
        month: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> tuple[list[Expense], int]:
        return self._repo.find_paginated(
            page=page,
            per_page=per_page,
            category_id=category_id,
            year=year,
            month=month,
            start_date=start_date,
            end_date=end_date,
        )

    def get_expense(self, expense_id: int) -> Expense:
        expense = self._repo.find_by_id(expense_id)
        if expense is None:
            raise ExpenseNotFoundError(expense_id)
        return expense

    def create_expense(self, params: ExpenseCreateParams) -> tuple[Expense, dict]:
        # BR-EXP-01
        if params.amount <= 0:
            raise ExpenseAmountError()
        # BR-EXP-02
        if params.date > date.today():
            raise ExpenseFutureDateError()
        # BR-EXP-04
        if not params.description.strip():
            raise ExpenseBlankDescriptionError()
        # BR-EXP-03 — raises CategoryNotFoundError if missing
        self._get_category_service().get_category(params.category_id)

        expense = Expense(
            category_id=params.category_id,
            amount=params.amount,
            description=params.description.strip(),
            date=params.date,
            notes=params.notes,
        )
        # Add and flush to get the id before the budget warning check,
        # then commit after the warning is computed (all in one transaction).
        database.session.add(expense)
        database.session.flush()

        warnings = self._check_budget_warning(
            params.category_id, params.date.year, params.date.month
        )

        database.session.commit()
        logger.info("Created expense", extra={"expense_id": expense.id, "amount": str(params.amount)})
        return expense, warnings

    def update_expense(self, expense_id: int, params: ExpenseUpdateParams) -> tuple[Expense, dict]:
        expense = self.get_expense(expense_id)

        if params.amount is not None:
            if params.amount <= 0:
                raise ExpenseAmountError()
            expense.amount = params.amount
        if params.date is not None:
            if params.date > date.today():
                raise ExpenseFutureDateError()
            expense.date = params.date
        if params.description is not None:
            if not params.description.strip():
                raise ExpenseBlankDescriptionError()
            expense.description = params.description.strip()
        if params.category_id is not None:
            # BR-EXP-03
            self._get_category_service().get_category(params.category_id)
            expense.category_id = params.category_id
        if params.notes is not None:
            expense.notes = params.notes

        warnings = self._check_budget_warning(
            expense.category_id, expense.date.year, expense.date.month
        )
        database.session.commit()
        logger.info("Updated expense", extra={"expense_id": expense_id})
        return expense, warnings

    def delete_expense(self, expense_id: int) -> None:
        expense = self.get_expense(expense_id)
        self._repo.delete(expense)
        logger.info("Deleted expense", extra={"expense_id": expense_id})

    def _check_budget_warning(self, category_id: int, year: int, month: int) -> dict:
        """BR-EXP-05: soft warning if total spending exceeds budget for the month."""
        budget = self._get_budget_repository().find_for_month(category_id, year, month)
        if budget is None:
            return {}
        total_spent = self._repo.sum_for_month(category_id, year, month)
        if total_spent > budget.amount:
            return {
                "over_budget": True,
                "budget_amount": str(budget.amount),
                "total_spent": str(total_spent),
                "rule": "BR-EXP-05",
            }
        return {}
