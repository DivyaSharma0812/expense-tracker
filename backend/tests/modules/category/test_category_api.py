from tests.conftest import CategoryFactory, ExpenseFactory


def test_list_categories_empty(client):
    res = client.get("/api/categories")
    assert res.status_code == 200
    assert res.json["data"] == []


def test_create_category(client):
    res = client.post("/api/categories", json={"name": "Food", "color": "#ff0000"})
    assert res.status_code == 201
    assert res.json["data"]["name"] == "Food"
    assert res.json["data"]["color"] == "#ff0000"


def test_create_category_missing_name(client):
    res = client.post("/api/categories", json={"color": "#ff0000"})
    assert res.status_code == 400
    assert res.json["error"]["code"] == "VALIDATION_ERROR"


def test_create_category_invalid_color(client):
    res = client.post("/api/categories", json={"name": "X", "color": "notahex"})
    assert res.status_code == 422
    assert res.json["error"]["code"] == "BUSINESS_RULE_VIOLATION"


def test_create_duplicate_category(client):
    client.post("/api/categories", json={"name": "Dup"})
    res = client.post("/api/categories", json={"name": "dup"})
    assert res.status_code == 409


def test_get_category(client):
    cat = CategoryFactory(name="MyCategory")
    res = client.get(f"/api/categories/{cat.id}")
    assert res.status_code == 200
    assert res.json["data"]["name"] == "MyCategory"


def test_get_category_not_found(client):
    res = client.get("/api/categories/99999")
    assert res.status_code == 404


def test_update_category(client):
    cat = CategoryFactory(name="Old")
    res = client.put(f"/api/categories/{cat.id}", json={"name": "New"})
    assert res.status_code == 200
    assert res.json["data"]["name"] == "New"


def test_update_category_no_fields(client):
    cat = CategoryFactory()
    res = client.put(f"/api/categories/{cat.id}", json={})
    assert res.status_code == 400
    assert res.json["error"]["code"] == "VALIDATION_ERROR"


def test_delete_category_without_expenses(client):
    cat = CategoryFactory()
    res = client.delete(f"/api/categories/{cat.id}")
    assert res.status_code == 204


def test_delete_category_with_expenses_fails(client):
    expense = ExpenseFactory()
    res = client.delete(f"/api/categories/{expense.category_id}")
    assert res.status_code == 409


def test_list_categories_returns_all(client):
    CategoryFactory(name="A")
    CategoryFactory(name="B")
    res = client.get("/api/categories")
    names = [c["name"] for c in res.json["data"]]
    assert "A" in names
    assert "B" in names
