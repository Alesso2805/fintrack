import pytest
from fastapi.testclient import TestClient

def auth_headers(client: TestClient, email: str, password: str) -> dict[str, str]:
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    if response.status_code != 200:
        return {}
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def setup_export_movements(client: TestClient):
    headers = auth_headers(client, "admin@example.com", "admin-password")
    import uuid
    uid = str(uuid.uuid4())[:8]
    
    inv_res = client.post("/api/v1/investors", json={"name": f"Export Investor {uid}", "document_id": f"DOC-EXP-{uid}"}, headers=headers)
    inv_id = inv_res.json()["id"]

    cat_res = client.post("/api/v1/movement-categories", json={"name": f"Export Cat {uid}"}, headers=headers)
    cat_id = cat_res.json()["id"]

    client.post("/api/v1/financial-movements", json={
        "investor_id": inv_id,
        "category_id": cat_id,
        "type": "deposit",
        "amount": "999.99",
        "currency": "USD",
        "status": "completed",
        "movement_date": "2026-06-01",
        "description": "Test Export Description"
    }, headers=headers)

    return {"investor_id": inv_id, "category_id": cat_id, "uid": uid}

def test_export_movements_csv(client: TestClient, setup_export_movements: dict):
    headers = auth_headers(client, "admin@example.com", "admin-password")
    inv_id = setup_export_movements["investor_id"]

    response = client.get(f"/api/v1/exports/movements/csv?investor_id={inv_id}", headers=headers)
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv; charset=utf-8"
    assert "attachment; filename=movements_export.csv" in response.headers["content-disposition"]
    
    csv_content = response.text
    lines = csv_content.strip().split("\r\n")
    if len(lines) == 1: # Fallback in case of \n
        lines = csv_content.strip().split("\n")

    assert len(lines) == 2 # Header + 1 row
    assert "investor_id" in lines[0]
    assert "999.99" in lines[1]
    assert "Test Export Description" in lines[1]
    assert "USD" in lines[1]
