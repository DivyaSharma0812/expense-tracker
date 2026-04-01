from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CategoryCreateParams:
    name: str
    color: str = "#6366f1"
    icon: Optional[str] = None


@dataclass
class CategoryUpdateParams:
    name: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None
