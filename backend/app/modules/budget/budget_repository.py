from decimal import Decimal
from typing import Optional
from ...application.base_repository import BaseRepository
from ...extensions import database
from .budget_model import Budget


class BudgetRepository(BaseRepository[Budget]):
    model_class = Budget

    def find_filtered(
        self,
        year: Optional[int] = None,
        month: Optional[int] = None,
        category_id: Optional[int] = None,
    ) -> list[Budget]:
        query = database.select(Budget).order_by(
            Budget.year.desc(), Budget.month.desc(), Budget.id
        )
        if year is not None:
            query = query.where(Budget.year == year)
        if month is not None:
            query = query.where(Budget.month == month)
        if category_id is not None:
            query = query.where(Budget.category_id == category_id)
        return database.session.execute(query).scalars().all()

    def find_for_month(
        self, category_id: int, year: int, month: int
    ) -> Optional[Budget]:
        return database.session.execute(
            database.select(Budget).where(
                Budget.category_id == category_id,
                Budget.year == year,
                Budget.month == month,
            )
        ).scalar_one_or_none()

    def sum_for_month(self, year: int, month: int) -> Decimal:
        result = database.session.execute(
            database.select(database.func.sum(Budget.amount)).where(
                Budget.year == year,
                Budget.month == month,
            )
        ).scalar()
        return Decimal(str(result)) if result else Decimal("0")

    def amounts_by_category_for_month(self, year: int, month: int) -> dict[int, Decimal]:
        rows = database.session.execute(
            database.select(Budget.category_id, Budget.amount).where(
                Budget.year == year,
                Budget.month == month,
            )
        ).all()
        return {row.category_id: Decimal(str(row.amount)) for row in rows}
