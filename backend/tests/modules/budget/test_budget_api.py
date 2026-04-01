from tests.conftest import CategoryFactory, BudgetFactory


def test_list_budgets_empty(client):
    res = client.get("/api/budgets")
    assert res.status_code == 200
    assert res.json["data"] == []


def test_create_budget(client):
    cat = CategoryFactory()
    res = client.post("/api/budgets", json={
        "category_id": cat.id,
        "year": 2025,
        "month": 3,
        "amount": "500",
    })
    assert res.status_code == 201
    assert res.json["data"]["amount"] == "500.00"


def test_create_budget_invalid_month(client):
    cat = CategoryFactory()
    res = client.post("/api/budgets", json={
        "category_id": cat.id,
        "year": 2025,
        "month": 13,
        "amount": "500",
    })
    assert res.status_code == 400


def test_create_budget_zero_amount(client):
    cat = CategoryFactory()
    res = client.post("/api/budgets", json={
        "category_id": cat.id,
        "year": 2025,
        "month": 3,
        "amount": "0",
    })
    assert res.status_code == 422


def test_create_duplicate_budget(client):
    cat = CategoryFactory()
    client.post("/api/budgets", json={"category_id": cat.id, "year": 2025, "month": 5, "amount": "200"})
    res = client.post("/api/budgets", json={"category_id": cat.id, "year": 2025, "month": 5, "amount": "300"})
    assert res.status_code == 409


def test_get_budget(client):
    budget = BudgetFactory()
    res = client.get(f"/api/budgets/{budget.id}")
    assert res.status_code == 200
    assert res.json["data"]["id"] == budget.id


def test_get_budget_not_found(client):
    res = client.get("/api/budgets/99999")
    assert res.status_code == 404


def test_update_budget(client):
    budget = BudgetFactory()
    res = client.put(f"/api/budgets/{budget.id}", json={"amount": "750"})
    assert res.status_code == 200
    assert res.json["data"]["amount"] == "750.00"


def test_delete_budget(client):
    budget = BudgetFactory()
    res = client.delete(f"/api/budgets/{budget.id}")
    assert res.status_code == 204


def test_list_budgets_filter_by_year_month(client):
    cat = CategoryFactory()
    BudgetFactory(category=cat, year=2025, month=1)
    BudgetFactory(category=cat, year=2025, month=2)
    res = client.get("/api/budgets?year=2025&month=1")
    assert len(res.json["data"]) == 1
    assert res.json["data"][0]["month"] == 1
