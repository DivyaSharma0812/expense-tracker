import pytest
from app.modules.category.category_service import CategoryService
from app.modules.category.types import CategoryCreateParams, CategoryUpdateParams
from app.modules.category.errors import (
    CategoryNotFoundError,
    CategoryNameConflictError,
    CategoryHasExpensesError,
    CategoryInvalidColorError,
)
from app.application.errors import NotFoundError, ConflictError, BusinessRuleError
from tests.conftest import CategoryFactory, ExpenseFactory

service = CategoryService()


def test_get_all_categories_returns_empty_list():
    result = service.get_all_categories()
    assert result == []


def test_create_and_get_category():
    category = service.create_category(CategoryCreateParams(name="Groceries", color="#ff0000"))
    fetched = service.get_category(category.id)
    assert fetched.name == "Groceries"
    assert fetched.color == "#ff0000"


def test_get_category_raises_not_found():
    with pytest.raises(CategoryNotFoundError):
        service.get_category(99999)


def test_BR_CAT_01_name_must_be_unique():
    service.create_category(CategoryCreateParams(name="Unique Name"))
    with pytest.raises(CategoryNameConflictError) as exc_info:
        service.create_category(CategoryCreateParams(name="unique name"))  # same name, different case
    assert "BR-CAT-01" in str(exc_info.value.details)


def test_BR_CAT_01_update_name_conflict():
    service.create_category(CategoryCreateParams(name="Alpha"))
    category_two = service.create_category(CategoryCreateParams(name="Beta"))
    with pytest.raises(CategoryNameConflictError):
        service.update_category(category_two.id, CategoryUpdateParams(name="Alpha"))


def test_BR_CAT_01_update_same_name_ok():
    category = service.create_category(CategoryCreateParams(name="SameName"))
    updated = service.update_category(category.id, CategoryUpdateParams(name="SameName"))
    assert updated.name == "SameName"


def test_BR_CAT_02_cannot_delete_category_with_expenses():
    expense = ExpenseFactory()
    category_id = expense.category_id
    with pytest.raises(CategoryHasExpensesError) as exc_info:
        service.delete_category(category_id)
    assert exc_info.value.details["expense_count"] == 1


def test_BR_CAT_02_can_delete_category_without_expenses():
    category = CategoryFactory()
    service.delete_category(category.id)
    with pytest.raises(CategoryNotFoundError):
        service.get_category(category.id)


def test_BR_CAT_03_invalid_color_rejected():
    with pytest.raises(CategoryInvalidColorError) as exc_info:
        service.create_category(CategoryCreateParams(name="Bad Color", color="red"))
    assert "BR-CAT-03" in str(exc_info.value.details)


def test_BR_CAT_03_valid_color_accepted():
    category = service.create_category(CategoryCreateParams(name="Good Color", color="#aabbcc"))
    assert category.color == "#aabbcc"


def test_update_category_fields():
    category = CategoryFactory(name="Old Name")
    updated = service.update_category(
        category.id, CategoryUpdateParams(name="New Name", color="#123456", icon="🏠")
    )
    assert updated.name == "New Name"
    assert updated.color == "#123456"
    assert updated.icon == "🏠"
