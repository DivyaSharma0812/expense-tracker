from ...application.errors import NotFoundError, ConflictError, BusinessRuleError


class CategoryNotFoundError(NotFoundError):
    def __init__(self, category_id: int):
        super().__init__(
            f"Category {category_id} not found",
            details={"category_id": category_id},
        )


class CategoryNameConflictError(ConflictError):
    def __init__(self, name: str):
        super().__init__(
            f"A category named '{name}' already exists.",
            details={"field": "name", "rule": "BR-CAT-01"},
        )


class CategoryHasExpensesError(ConflictError):
    def __init__(self, category_name: str, expense_count: int):
        super().__init__(
            f"Cannot delete category '{category_name}': it has {expense_count} expense(s). "
            "Delete or reassign the expenses first.",
            details={"expense_count": expense_count},
        )


class CategoryInvalidColorError(BusinessRuleError):
    def __init__(self, color: str):
        super().__init__(
            f"Invalid color '{color}'. Must be a 6-digit hex color (e.g. #6366f1).",
            details={"field": "color", "rule": "BR-CAT-03"},
        )
