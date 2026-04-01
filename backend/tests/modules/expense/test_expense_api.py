from datetime import date
from freezegun import freeze_time
from tests.conftest import CategoryFactory, ExpenseFactory, BudgetFactory


def test_list_expenses_empty(client):
    res = client.get("/api/expenses")
    assert res.status_code == 200
    assert res.json["data"] == []
    assert "meta" in res.json


def test_create_expense(client):
    cat = CategoryFactory()
    res = client.post("/api/expenses", json={
        "category_id": cat.id,
        "amount": "25.50",
        "description": "Coffee",
        "date": str(date.today()),
    })
    assert res.status_code == 201
    assert res.json["data"]["description"] == "Coffee"
    assert res.json["data"]["amount"] == "25.50"


def test_create_expense_invalid_category(client):
    res = client.post("/api/expenses", json={
        "category_id": 99999,
        "amount": "10",
        "description": "X",
        "date": str(date.today()),
    })
    assert res.status_code == 404


def test_create_expense_negative_amount(client):
    cat = CategoryFactory()
    res = client.post("/api/expenses", json={
        "category_id": cat.id,
        "amount": "-5",
        "description": "X",
        "date": str(date.today()),
    })
    assert res.status_code == 422


@freeze_time("2025-03-15")
def test_create_expense_future_date(client):
    cat = CategoryFactory()
    res = client.post("/api/expenses", json={
        "category_id": cat.id,
        "amount": "10",
        "description": "X",
        "date": "2025-03-16",
    })
    assert res.status_code == 422


def test_create_expense_blank_description(client):
    cat = CategoryFactory()
    res = client.post("/api/expenses", json={
        "category_id": cat.id,
        "amount": "10",
        "description": "  ",
        "date": str(date.today()),
    })
    assert res.status_code == 422


def test_create_expense_over_budget_warning(client):
    cat = CategoryFactory()
    today = date.today()
    BudgetFactory(category=cat, year=today.year, month=today.month, amount="50")
    res = client.post("/api/expenses", json={
        "category_id": cat.id,
        "amount": "100",
        "description": "Over budget",
        "date": str(today),
    })
    assert res.status_code == 201
    assert res.json.get("warnings", {}).get("over_budget") is True


def test_get_expense(client):
    exp = ExpenseFactory(description="My expense")
    res = client.get(f"/api/expenses/{exp.id}")
    assert res.status_code == 200
    assert res.json["data"]["description"] == "My expense"


def test_get_expense_not_found(client):
    res = client.get("/api/expenses/99999")
    assert res.status_code == 404


def test_update_expense(client):
    exp = ExpenseFactory(description="Before", amount="20.00")
    res = client.put(f"/api/expenses/{exp.id}", json={"description": "After", "amount": "35.00"})
    assert res.status_code == 200
    assert res.json["data"]["description"] == "After"
    assert res.json["data"]["amount"] == "35.00"


def test_update_expense_no_fields(client):
    exp = ExpenseFactory()
    res = client.put(f"/api/expenses/{exp.id}", json={})
    assert res.status_code == 400
    assert res.json["error"]["code"] == "VALIDATION_ERROR"


def test_delete_expense(client):
    exp = ExpenseFactory()
    res = client.delete(f"/api/expenses/{exp.id}")
    assert res.status_code == 204
    assert client.get(f"/api/expenses/{exp.id}").status_code == 404


def test_list_expenses_pagination(client):
    cat = CategoryFactory()
    for _ in range(5):
        ExpenseFactory(category=cat, description="x")
    res = client.get("/api/expenses?per_page=3&page=1")
    assert len(res.json["data"]) == 3
    assert res.json["meta"]["total"] >= 5
