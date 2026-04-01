from datetime import date
from decimal import Decimal
from typing import Optional
from ...application.base_repository import BaseRepository
from ...extensions import database
from .expense_model import Expense


class ExpenseRepository(BaseRepository[Expense]):
    model_class = Expense

    def find_paginated(
        self,
        page: int = 1,
        per_page: int = 20,
        category_id: Optional[int] = None,
        year: Optional[int] = None,
        month: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> tuple[list[Expense], int]:
        query = database.select(Expense).order_by(Expense.date.desc(), Expense.id.desc())
        if category_id is not None:
            query = query.where(Expense.category_id == category_id)
        if year is not None and month is not None:
            query = query.where(
                database.extract("year", Expense.date) == year,
                database.extract("month", Expense.date) == month,
            )
        elif year is not None:
            query = query.where(database.extract("year", Expense.date) == year)
        if start_date is not None:
            query = query.where(Expense.date >= start_date)
        if end_date is not None:
            query = query.where(Expense.date <= end_date)

        total = database.session.execute(
            database.select(database.func.count()).select_from(query.subquery())
        ).scalar()
        expenses = database.session.execute(
            query.limit(per_page).offset((page - 1) * per_page)
        ).scalars().all()
        return expenses, total

    def sum_for_month(self, category_id: int, year: int, month: int) -> Decimal:
        result = database.session.execute(
            database.select(database.func.sum(Expense.amount)).where(
                Expense.category_id == category_id,
                database.extract("year", Expense.date) == year,
                database.extract("month", Expense.date) == month,
            )
        ).scalar()
        return Decimal(str(result)) if result else Decimal("0")

    def count_for_month(self, category_id: int, year: int, month: int) -> int:
        return database.session.execute(
            database.select(database.func.count(Expense.id)).where(
                Expense.category_id == category_id,
                database.extract("year", Expense.date) == year,
                database.extract("month", Expense.date) == month,
            )
        ).scalar()

    def spending_by_category_for_month(self, year: int, month: int) -> dict[int, Decimal]:
        rows = database.session.execute(
            database.select(Expense.category_id, database.func.sum(Expense.amount))
            .where(
                database.extract("year", Expense.date) == year,
                database.extract("month", Expense.date) == month,
            )
            .group_by(Expense.category_id)
        ).all()
        return {row[0]: Decimal(str(row[1])) for row in rows}

    def spending_by_month(self, limit: int) -> list:
        return database.session.execute(
            database.select(
                database.extract("year", Expense.date).label("year"),
                database.extract("month", Expense.date).label("month"),
                database.func.sum(Expense.amount).label("total_spent"),
            )
            .group_by("year", "month")
            .order_by(database.desc("year"), database.desc("month"))
            .limit(limit)
        ).all()
