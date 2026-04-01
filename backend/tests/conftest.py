import pytest
import factory
from decimal import Decimal
from datetime import date
from app import create_app
from app.extensions import database
from app.modules.category.category_model import Category
from app.modules.expense.expense_model import Expense
from app.modules.budget.budget_model import Budget


@pytest.fixture(scope="session")
def app():
    application = create_app("testing")
    ctx = application.app_context()
    ctx.push()
    database.create_all()
    yield application
    database.drop_all()
    ctx.pop()


@pytest.fixture(scope="session")
def db(app):
    return database


@pytest.fixture(autouse=True)
def clean_tables(app):
    """Delete all rows after each test and remove the scoped session."""
    yield
    for table in reversed(database.metadata.sorted_tables):
        database.session.execute(table.delete())
    database.session.commit()
    database.session.remove()  # ensures next test gets a fresh session


@pytest.fixture
def client(app):
    return app.test_client()


# ---------------------------------------------------------------------------
# factory-boy factories
# ---------------------------------------------------------------------------

class CategoryFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Category
        sqlalchemy_session = database.session
        sqlalchemy_session_persistence = "commit"

    name = factory.Sequence(lambda n: f"Category {n}")
    color = "#6366f1"
    icon = None


class ExpenseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Expense
        sqlalchemy_session = database.session
        sqlalchemy_session_persistence = "commit"

    category = factory.SubFactory(CategoryFactory)
    category_id = factory.SelfAttribute("category.id")
    amount = Decimal("50.00")
    description = "Test expense"
    date = factory.LazyFunction(date.today)
    notes = None


class BudgetFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Budget
        sqlalchemy_session = database.session
        sqlalchemy_session_persistence = "commit"

    category = factory.SubFactory(CategoryFactory)
    category_id = factory.SelfAttribute("category.id")
    year = 2025
    month = 3
    amount = Decimal("500.00")
