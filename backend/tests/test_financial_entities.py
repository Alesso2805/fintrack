from fastapi.testclient import TestClient


def auth_headers(client: TestClient, email: str, password: str) -> dict[str, str]:
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def create_investor(client: TestClient, headers: dict[str, str], name: str = "Acme Capital") -> dict:
    response = client.post(
        "/api/v1/investors",
        json={"name": name, "document_id": "INV-001", "email": "ops@example.com"},
        headers=headers,
    )
    assert response.status_code == 201
    return response.json()


def create_category(client: TestClient, headers: dict[str, str], name: str = "Capital call") -> dict:
    response = client.post(
        "/api/v1/movement-categories",
        json={"name": name, "description": "Investor capital movement"},
        headers=headers,
    )
    assert response.status_code == 201
    return response.json()


def test_admin_can_manage_financial_entities(client: TestClient) -> None:
    headers = auth_headers(client, "admin@example.com", "admin-password")
    investor = create_investor(client, headers)
    category = create_category(client, headers)

    movement_response = client.post(
        "/api/v1/financial-movements",
        json={
            "investor_id": investor["id"],
            "category_id": category["id"],
            "type": "deposit",
            "amount": "12500.75",
            "currency": "usd",
            "status": "completed",
            "movement_date": "2026-06-06",
            "description": "Initial contribution",
        },
        headers=headers,
    )

    assert movement_response.status_code == 201
    movement = movement_response.json()
    assert movement["currency"] == "USD"
    assert movement["created_by"]

    list_response = client.get(
        "/api/v1/financial-movements?type=deposit&status=completed&date_from=2026-06-01&date_to=2026-06-30",
        headers=headers,
    )

    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    update_response = client.patch(
        f"/api/v1/financial-movements/{movement['id']}",
        json={"status": "pending", "amount": "13000.00"},
        headers=headers,
    )

    assert update_response.status_code == 200
    assert update_response.json()["status"] == "pending"
    assert update_response.json()["amount"] == "13000.00"


def test_viewer_can_read_but_cannot_create_investor(client: TestClient) -> None:
    admin_headers = auth_headers(client, "admin@example.com", "admin-password")
    viewer_headers = auth_headers(client, "viewer@example.com", "viewer-password")
    create_investor(client, admin_headers)

    list_response = client.get("/api/v1/investors", headers=viewer_headers)
    create_response = client.post(
        "/api/v1/investors",
        json={"name": "Read Only Investor"},
        headers=viewer_headers,
    )

    assert list_response.status_code == 200
    assert create_response.status_code == 403


def test_duplicate_investor_name_returns_conflict(client: TestClient) -> None:
    headers = auth_headers(client, "admin@example.com", "admin-password")
    create_investor(client, headers)

    response = client.post(
        "/api/v1/investors",
        json={"name": "Acme Capital"},
        headers=headers,
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Investor name already exists"


def test_movement_requires_existing_references(client: TestClient) -> None:
    headers = auth_headers(client, "admin@example.com", "admin-password")

    response = client.post(
        "/api/v1/financial-movements",
        json={
            "investor_id": "missing-investor",
            "category_id": "missing-category",
            "type": "deposit",
            "amount": "100.00",
            "currency": "USD",
            "status": "completed",
            "movement_date": "2026-06-06",
        },
        headers=headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Investor not found"
