from fastapi.testclient import TestClient


def test_login_current_user_and_refresh_happy_path(client: TestClient) -> None:
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@example.com", "password": "admin-password"},
    )

    assert login_response.status_code == 200
    tokens = login_response.json()
    assert tokens["token_type"] == "bearer"
    assert tokens["access_token"]
    assert tokens["refresh_token"]

    me_response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )

    assert me_response.status_code == 200
    assert me_response.json()["user"]["email"] == "admin@example.com"
    assert me_response.json()["user"]["role"] == "admin"

    refresh_response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": tokens["refresh_token"]},
    )

    assert refresh_response.status_code == 200
    assert refresh_response.json()["access_token"]
    assert refresh_response.json()["refresh_token"]


def test_login_rejects_invalid_password(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@example.com", "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_viewer_cannot_access_admin_check(client: TestClient) -> None:
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "viewer@example.com", "password": "viewer-password"},
    )
    token = login_response.json()["access_token"]

    response = client.get(
        "/api/v1/users/admin-check",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Insufficient permissions"
