import pytest
from fastapi.testclient import TestClient

def auth_headers(client: TestClient, email: str, password: str) -> dict[str, str]:
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    if response.status_code != 200:
        return {}
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def setup_movements(client: TestClient):
    headers = auth_headers(client, "admin@example.com", "admin-password")
    import uuid
    uid = str(uuid.uuid4())[:8]
    
    inv_res = client.post("/api/v1/investors", json={"name": f"Dashboard Investor {uid}", "document_id": f"DOC-DASH-{uid}"}, headers=headers)
    inv_id = inv_res.json()["id"]

    cat_res = client.post("/api/v1/movement-categories", json={"name": f"Dashboard Cat {uid}"}, headers=headers)
    cat_id = cat_res.json()["id"]

    # Create deposits
    client.post("/api/v1/financial-movements", json={
        "investor_id": inv_id,
        "category_id": cat_id,
        "type": "deposit",
        "amount": "1500.00",
        "currency": "USD",
        "status": "completed",
        "movement_date": "2026-06-01",
    }, headers=headers)

    client.post("/api/v1/financial-movements", json={
        "investor_id": inv_id,
        "category_id": cat_id,
        "type": "deposit",
        "amount": "2500.00",
        "currency": "EUR",
        "status": "completed",
        "movement_date": "2026-06-02",
    }, headers=headers)

    # Create withdrawal
    client.post("/api/v1/financial-movements", json={
        "investor_id": inv_id,
        "category_id": cat_id,
        "type": "withdrawal",
        "amount": "500.00",
        "currency": "USD",
        "status": "completed",
        "movement_date": "2026-06-03",
    }, headers=headers)

    return {"investor_id": inv_id, "category_id": cat_id, "uid": uid}


def test_get_dashboard_metrics(client: TestClient, setup_movements: dict):
    headers = auth_headers(client, "admin@example.com", "admin-password")
    inv_id = setup_movements["investor_id"]

    response = client.get(f"/api/v1/dashboard/metrics?investor_id={inv_id}", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["total_movements"] == 3
    
    balances = data["balances"]
    assert len(balances) == 2
    
    usd_balance = next(b for b in balances if b["currency"] == "USD")
    assert usd_balance["total_deposits"] == "1500.00"
    assert usd_balance["total_withdrawals"] == "500.00"
    assert usd_balance["balance"] == "1000.00"

    eur_balance = next(b for b in balances if b["currency"] == "EUR")
    assert eur_balance["total_deposits"] == "2500.00"
    assert eur_balance["total_withdrawals"] == "0"
    assert eur_balance["balance"] == "2500.00"
    
    categories = data["category_distribution"]
    assert len(categories) == 1
    assert categories[0]["total_amount"] == "4500.00"  # 1500 + 2500 + 500
