import logging
from typing import Optional, TYPE_CHECKING
from .budget_repository import BudgetRepository
from .budget_model import Budget
from .errors import BudgetNotFoundError, BudgetAmountError, DuplicateBudgetError
from .types import BudgetCreateParams, BudgetUpdateParams

if TYPE_CHECKING:
    from ..category.category_service import CategoryService

logger = logging.getLogger(__name__)


class BudgetService:
    def __init__(
        self,
        repository: Optional[BudgetRepository] = None,
        category_service: Optional["CategoryService"] = None,
    ):
        self._repo = repository or BudgetRepository()
        self._category_service = category_service

    def _get_category_service(self) -> "CategoryService":
        if self._category_service is None:
            from ..category.category_service import CategoryService
            self._category_service = CategoryService()
        return self._category_service

    def get_budgets(
        self,
        year: Optional[int] = None,
        month: Optional[int] = None,
        category_id: Optional[int] = None,
    ) -> list[Budget]:
        return self._repo.find_filtered(year=year, month=month, category_id=category_id)

    def get_budget(self, budget_id: int) -> Budget:
        budget = self._repo.find_by_id(budget_id)
        if budget is None:
            raise BudgetNotFoundError(budget_id)
        return budget

    def create_budget(self, params: BudgetCreateParams) -> Budget:
        # BR-BUD-01
        if params.amount <= 0:
            raise BudgetAmountError()
        # BR-BUD-02 and BR-BUD-03 are enforced by Marshmallow schema Range validators
        # BR-BUD-05: category must exist
        self._get_category_service().get_category(params.category_id)
        # BR-BUD-04: unique per category+year+month
        existing = self._repo.find_for_month(params.category_id, params.year, params.month)
        if existing is not None:
            raise DuplicateBudgetError(params.category_id, params.year, params.month, existing.id)

        budget = Budget(
            category_id=params.category_id,
            year=params.year,
            month=params.month,
            amount=params.amount,
        )
        self._repo.save(budget)
        logger.info("Created budget", extra={"budget_id": budget.id})
        return budget

    def update_budget(self, budget_id: int, params: BudgetUpdateParams) -> Budget:
        budget = self.get_budget(budget_id)
        # BR-BUD-01
        if params.amount <= 0:
            raise BudgetAmountError()
        budget.amount = params.amount
        self._repo.save(budget)
        logger.info("Updated budget", extra={"budget_id": budget_id})
        return budget

    def delete_budget(self, budget_id: int) -> None:
        budget = self.get_budget(budget_id)
        self._repo.delete(budget)
        logger.info("Deleted budget", extra={"budget_id": budget_id})
