from io import BytesIO

import pytest
from fastapi.testclient import TestClient

from app.models.imports import ImportBatchStatus


@pytest.fixture
def csv_content(client: TestClient):
    admin_headers = auth_headers(client, "admin@example.com", "admin-password")
    
    import uuid
    uid = str(uuid.uuid4())[:8]
    inv_res = client.post("/api/v1/investors", json={"name": f"Test Investor CSV {uid}", "document_id": f"DOC-{uid}"}, headers=admin_headers)
    inv_id = inv_res.json()["id"]

    cat_res = client.post("/api/v1/movement-categories", json={"name": f"Test Category CSV {uid}"}, headers=admin_headers)
    cat_id = cat_res.json()["id"]

    content = f"""investor_id,category_id,type,amount,currency,status,movement_date,description
{inv_id},{cat_id},deposit,1000.50,USD,completed,2026-06-01,Test deposit
{inv_id},{cat_id},withdrawal,500.00,USD,pending,2026-06-02,Test withdrawal
"""
    return content


@pytest.fixture
def invalid_csv_content(client: TestClient):
    admin_headers = auth_headers(client, "admin@example.com", "admin-password")
    
    import uuid
    uid = str(uuid.uuid4())[:8]
    inv_res = client.post("/api/v1/investors", json={"name": f"Test Investor CSV Invalid {uid}", "document_id": f"DOC-INV-{uid}"}, headers=admin_headers)
    inv_id = inv_res.json()["id"]

    cat_res = client.post("/api/v1/movement-categories", json={"name": f"Test Category CSV Invalid {uid}"}, headers=admin_headers)
    cat_id = cat_res.json()["id"]

    content = f"""investor_id,category_id,type,amount,currency,status,movement_date,description
{inv_id},{cat_id},deposit,1000.50,USD,completed,2026-06-01,Test deposit
{inv_id},{cat_id},invalid_type,-500.00,USD,pending,2026-06-02,Test withdrawal
"""
    return content


def auth_headers(client: TestClient, email: str, password: str) -> dict[str, str]:
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    if response.status_code != 200:
        return {}
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_upload_valid_csv(client: TestClient, csv_content: str):
    headers = auth_headers(client, "admin@example.com", "admin-password")
    files = {"file": ("data.csv", BytesIO(csv_content.encode("utf-8")), "text/csv")}
    response = client.post("/api/v1/imports/csv", headers=headers, files=files)
    
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == ImportBatchStatus.COMPLETED
    assert data["total_rows"] == 2
    assert data["successful_rows"] == 2
    assert data["failed_rows"] == 0


def test_upload_invalid_csv_partial_success(client: TestClient, invalid_csv_content: str):
    headers = auth_headers(client, "admin@example.com", "admin-password")
    files = {"file": ("data.csv", BytesIO(invalid_csv_content.encode("utf-8")), "text/csv")}
    response = client.post("/api/v1/imports/csv", headers=headers, files=files)
    
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == ImportBatchStatus.PARTIAL_SUCCESS
    assert data["total_rows"] == 2
    assert data["successful_rows"] == 1
    assert data["failed_rows"] == 1


def test_list_and_get_import_batches(client: TestClient, csv_content: str):
    headers = auth_headers(client, "admin@example.com", "admin-password")
    
    files = {"file": ("data.csv", BytesIO(csv_content.encode("utf-8")), "text/csv")}
    upload_res = client.post("/api/v1/imports/csv", headers=headers, files=files)
    assert upload_res.status_code == 201
    batch_id = upload_res.json()["id"]

    list_res = client.get("/api/v1/imports", headers=headers)
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1

    get_res = client.get(f"/api/v1/imports/{batch_id}", headers=headers)
    assert get_res.status_code == 200
    assert get_res.json()["id"] == batch_id
    assert get_res.json()["error_details"] == []
