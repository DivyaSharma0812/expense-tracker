from dataclasses import dataclass
from decimal import Decimal


@dataclass
class BudgetCreateParams:
    category_id: int
    year: int
    month: int
    amount: Decimal


@dataclass
class BudgetUpdateParams:
    amount: Decimal
