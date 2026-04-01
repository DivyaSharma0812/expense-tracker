from ...application.errors import NotFoundError, ConflictError, BusinessRuleError


class BudgetNotFoundError(NotFoundError):
    def __init__(self, budget_id: int):
        super().__init__(
            f"Budget {budget_id} not found",
            details={"budget_id": budget_id},
        )


class BudgetAmountError(BusinessRuleError):
    def __init__(self):
        super().__init__(
            "Budget amount must be greater than zero.",
            details={"field": "amount", "rule": "BR-BUD-01"},
        )


class DuplicateBudgetError(ConflictError):
    def __init__(self, category_id: int, year: int, month: int, existing_id: int):
        super().__init__(
            f"A budget already exists for category {category_id} in {year}-{month:02d}.",
            details={"rule": "BR-BUD-04", "existing_id": existing_id},
        )
