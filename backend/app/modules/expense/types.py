from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional


@dataclass
class ExpenseCreateParams:
    category_id: int
    amount: Decimal
    description: str
    date: date
    notes: Optional[str] = None


@dataclass
class ExpenseUpdateParams:
    category_id: Optional[int] = None
    amount: Optional[Decimal] = None
    description: Optional[str] = None
    date: Optional[date] = None
    notes: Optional[str] = None
