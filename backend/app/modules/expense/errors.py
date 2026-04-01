from ...application.errors import NotFoundError, BusinessRuleError


class ExpenseNotFoundError(NotFoundError):
    def __init__(self, expense_id: int):
        super().__init__(
            f"Expense {expense_id} not found",
            details={"expense_id": expense_id},
        )


class ExpenseAmountError(BusinessRuleError):
    def __init__(self):
        super().__init__(
            "Expense amount must be greater than zero.",
            details={"field": "amount", "rule": "BR-EXP-01"},
        )


class ExpenseFutureDateError(BusinessRuleError):
    def __init__(self):
        super().__init__(
            "Expense date cannot be in the future.",
            details={"field": "date", "rule": "BR-EXP-02"},
        )


class ExpenseBlankDescriptionError(BusinessRuleError):
    def __init__(self):
        super().__init__(
            "Description must not be blank.",
            details={"field": "description", "rule": "BR-EXP-04"},
        )
