from dataclasses import dataclass
from typing import Optional


@dataclass
class DashboardSummaryParams:
    year: Optional[int] = None
    month: Optional[int] = None


@dataclass
class DashboardTrendsParams:
    months: int = 6
