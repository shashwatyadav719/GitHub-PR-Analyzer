from fastapi.testclient import TestClient
from app.main import app
from app.routes.github import get_current_user  # important

client = TestClient(app)


def test_get_repositories(monkeypatch):

    # 🔹 Mock auth dependency
    async def mock_get_current_user():
        return {
            "github_token": "fake_token",
            "github_user_id": 123
        }

    # 🔹 Mock GitHub API response (must match response_model)
    async def mock_get_repo(token: str):
        return [
            {
                "id": 1,
                "name": "repo1",
                "full_name": "testuser/repo1",
                "private": False,
                "html_url": "https://github.com/testuser/repo1"
            },
            {
                "id": 2,
                "name": "repo2",
                "full_name": "testuser/repo2",
                "private": False,
                "html_url": "https://github.com/testuser/repo2"
            }
        ]

    # ✅ Override FastAPI dependency (IMPORTANT)
    app.dependency_overrides[get_current_user] = mock_get_current_user

    # ✅ Mock normal function
    monkeypatch.setattr(
        "app.routes.github.get_repo",
        mock_get_repo
    )

    # 🔹 Call endpoint
    response = client.get("/github/repos")

    # 🔹 Assertions
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2

    assert data[0]["name"] == "repo1"
    assert data[0]["full_name"] == "testuser/repo1"
    assert data[0]["private"] is False

    assert data[1]["name"] == "repo2"

    # ✅ Cleanup (VERY IMPORTANT)
    app.dependency_overrides.clear()