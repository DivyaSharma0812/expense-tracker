from ...application.base_model import BaseModel
from ...extensions import database


class Category(BaseModel):
    __tablename__ = "categories"

    name = database.Column(database.Text, nullable=False, unique=True)
    color = database.Column(database.Text, nullable=False, default="#6366f1")
    icon = database.Column(database.Text, nullable=True)

    expenses = database.relationship("Expense", back_populates="category", lazy="dynamic")
    budgets = database.relationship(
        "Budget", back_populates="category", cascade="all, delete-orphan", lazy="dynamic"
    )

    def __repr__(self) -> str:
        return f"<Category id={self.id} name={self.name!r}>"
