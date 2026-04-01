import logging
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional

from ..category.category_repository import CategoryRepository
from ..expense.expense_repository import ExpenseRepository
from ..budget.budget_repository import BudgetRepository

logger = logging.getLogger(__name__)

_MAX_TREND_MONTHS = 24


class DashboardService:
    def __init__(
        self,
        category_repository: Optional[CategoryRepository] = None,
        expense_repository: Optional[ExpenseRepository] = None,
        budget_repository: Optional[BudgetRepository] = None,
    ):
        self._category_repository = category_repository or CategoryRepository()
        self._expense_repository = expense_repository or ExpenseRepository()
        self._budget_repository = budget_repository or BudgetRepository()

    def get_summary(self, year: Optional[int] = None, month: Optional[int] = None) -> dict:
        now = datetime.now(timezone.utc)
        year = year or now.year
        month = month or now.month

        spent_by_category = self._expense_repository.spending_by_category_for_month(year, month)
        budget_by_category = self._budget_repository.amounts_by_category_for_month(year, month)

        all_category_ids = set(spent_by_category) | set(budget_by_category)
        categories_data = []
        total_spent = Decimal("0")
        total_budgeted = Decimal("0")
        categories_over_budget = 0
        unbudgeted_spending = Decimal("0")

        for category_id in sorted(all_category_ids):
            category = self._category_repository.find_by_id(category_id)
            if category is None:
                continue

            spent = Decimal(str(spent_by_category.get(category_id, 0) or 0))
            budgeted = Decimal(str(budget_by_category.get(category_id, 0) or 0))
            remaining = budgeted - spent
            is_over_budget = spent > budgeted and budgeted > 0
            percent_used = round(float(spent / budgeted * 100), 1) if budgeted > 0 else None

            expense_count = self._expense_repository.count_for_month(category_id, year, month)

            categories_data.append({
                "category_id": category_id,
                "category_name": category.name,
                "color": category.color,
                "icon": category.icon,
                "budgeted": str(budgeted),
                "spent": str(spent),
                "remaining": str(remaining),
                "percent_used": percent_used,
                "is_over_budget": is_over_budget,
                "expense_count": expense_count,
            })

            total_spent += spent
            total_budgeted += budgeted
            if is_over_budget:
                categories_over_budget += 1
            if budgeted == 0 and spent > 0:
                unbudgeted_spending += spent

        overall_percent = (
            round(float(total_spent / total_budgeted * 100), 1) if total_budgeted > 0 else None
        )

        return {
            "year": year,
            "month": month,
            "total_spent": str(total_spent),
            "total_budgeted": str(total_budgeted),
            "remaining": str(total_budgeted - total_spent),
            "percent_used": overall_percent,
            "categories": categories_data,
            "unbudgeted_spending": str(unbudgeted_spending),
            "categories_over_budget": categories_over_budget,
        }

    def get_trends(self, months: int = 6) -> list[dict]:
        months = min(months, _MAX_TREND_MONTHS)

        rows = self._expense_repository.spending_by_month(months)

        result = []
        for row in reversed(rows):
            year_value = int(row.year)
            month_value = int(row.month)
            total_budgeted = self._budget_repository.sum_for_month(year_value, month_value)
            result.append({
                "year": year_value,
                "month": month_value,
                "total_spent": str(row.total_spent),
                "total_budgeted": str(total_budgeted),
            })

        return result
