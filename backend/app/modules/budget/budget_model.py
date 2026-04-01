from ...application.base_model import BaseModel
from ...extensions import database


class Budget(BaseModel):
    __tablename__ = "budgets"

    category_id = database.Column(
        database.Integer, database.ForeignKey("categories.id"), nullable=False
    )
    year = database.Column(database.Integer, nullable=False)
    month = database.Column(database.Integer, nullable=False)
    amount = database.Column(database.Numeric(10, 2), nullable=False)

    category = database.relationship("Category", back_populates="budgets")

    __table_args__ = (
        database.UniqueConstraint("category_id", "year", "month", name="uq_budget_category_month"),
        database.Index("ix_budgets_category_year_month", "category_id", "year", "month"),
    )

    def __repr__(self) -> str:
        return f"<Budget id={self.id} category_id={self.category_id} {self.year}-{self.month:02d}>"
