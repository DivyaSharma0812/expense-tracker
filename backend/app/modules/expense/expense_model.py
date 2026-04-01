from ...application.base_model import BaseModel
from ...extensions import database


class Expense(BaseModel):
    __tablename__ = "expenses"

    category_id = database.Column(
        database.Integer, database.ForeignKey("categories.id"), nullable=False
    )
    amount = database.Column(database.Numeric(10, 2), nullable=False)
    description = database.Column(database.Text, nullable=False)
    date = database.Column(database.Date, nullable=False)
    notes = database.Column(database.Text, nullable=True)

    category = database.relationship("Category", back_populates="expenses")

    __table_args__ = (
        database.Index("ix_expenses_category_date", "category_id", "date"),
    )

    def __repr__(self) -> str:
        return f"<Expense id={self.id} amount={self.amount} date={self.date}>"
