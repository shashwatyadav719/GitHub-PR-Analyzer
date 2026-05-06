from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_github_login_redirect():
    response = client.get("/auth/login", follow_redirects=False)

    assert response.status_code in [302, 307]
    assert "github.com/login/oauth/authorize" in response.headers["location"]




def test_github_callback_success(monkeypatch):

    # 🔹 Mock get_token
    async def mock_get_token(code: str):
        return {"access_token": "fake_token"}

    # 🔹 Mock get_user
    async def mock_get_user(token: str):
        return {
            "id": 123,
            "login": "testuser"
        }

    # Apply mocks
    monkeypatch.setattr(
        "app.routes.auth.get_token",
        mock_get_token
    )

    monkeypatch.setattr(
        "app.routes.auth.get_user",
        mock_get_user
    )

    response = client.get("/auth/callback?code=abc123")

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["user"] == "testuser"