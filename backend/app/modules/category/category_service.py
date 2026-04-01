import re
import logging
from .category_repository import CategoryRepository
from .category_model import Category
from .errors import (
    CategoryNotFoundError,
    CategoryNameConflictError,
    CategoryHasExpensesError,
    CategoryInvalidColorError,
)
from .types import CategoryCreateParams, CategoryUpdateParams

logger = logging.getLogger(__name__)

_HEX_COLOR_PATTERN = re.compile(r"^#[0-9a-fA-F]{6}$")


class CategoryService:
    def __init__(self, repository: CategoryRepository | None = None):
        self._repo = repository or CategoryRepository()

    def get_all_categories(self) -> list[Category]:
        return self._repo.find_all_ordered()

    def get_category(self, category_id: int) -> Category:
        category = self._repo.find_by_id(category_id)
        if category is None:
            raise CategoryNotFoundError(category_id)
        return category

    def create_category(self, params: CategoryCreateParams) -> Category:
        self._validate_color(params.color)
        self._assert_name_unique(params.name)
        category = Category(name=params.name.strip(), color=params.color, icon=params.icon)
        self._repo.save(category)
        logger.info("Created category", extra={"category_id": category.id, "category_name": category.name})
        return category

    def update_category(self, category_id: int, params: CategoryUpdateParams) -> Category:
        category = self.get_category(category_id)
        if params.color is not None:
            self._validate_color(params.color)
            category.color = params.color
        if params.name is not None:
            self._assert_name_unique(params.name, exclude_id=category_id)
            category.name = params.name.strip()
        if params.icon is not None:
            category.icon = params.icon
        self._repo.save(category)
        logger.info("Updated category", extra={"category_id": category_id})
        return category

    def delete_category(self, category_id: int) -> None:
        category = self.get_category(category_id)
        count = self._repo.expense_count(category_id)
        if count > 0:
            raise CategoryHasExpensesError(category.name, count)
        self._repo.delete(category)
        logger.info("Deleted category", extra={"category_id": category_id})

    def _validate_color(self, color: str) -> None:
        if not _HEX_COLOR_PATTERN.match(color):
            raise CategoryInvalidColorError(color)

    def _assert_name_unique(self, name: str, exclude_id: int | None = None) -> None:
        existing = self._repo.find_by_name_ci(name, exclude_id=exclude_id)
        if existing is not None:
            raise CategoryNameConflictError(name)
