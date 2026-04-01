from typing import Optional
from ...application.base_repository import BaseRepository
from ...extensions import database
from .category_model import Category


class CategoryRepository(BaseRepository[Category]):
    model_class = Category

    def find_all_ordered(self) -> list[Category]:
        return database.session.execute(
            database.select(Category).order_by(Category.name)
        ).scalars().all()

    def find_by_name_ci(
        self, name: str, exclude_id: Optional[int] = None
    ) -> Optional[Category]:
        query = database.select(Category).where(
            database.func.lower(Category.name) == name.strip().lower()
        )
        if exclude_id is not None:
            query = query.where(Category.id != exclude_id)
        return database.session.execute(query).scalar_one_or_none()

    def expense_count(self, category_id: int) -> int:
        category = self.find_by_id(category_id)
        if category is None:
            return 0
        return category.expenses.count()
