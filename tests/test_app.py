from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_root_redirect():
    # Arrange
    # (TestClient created at module level)

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307


def test_get_activities():
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_duplicate_and_remove_cycle():
    # Arrange
    activity = "Basketball Team"
    email = "testuser_signup@example.com"

    # Ensure clean state: remove if already present
    participants = client.get("/activities").json()[activity]["participants"]
    if email in participants:
        client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Act: sign up
    response_signup = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert: signup succeeded
    assert response_signup.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]

    # Act: attempt duplicate signup
    response_duplicate = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert: duplicate fails with 400
    assert response_duplicate.status_code == 400

    # Act: remove participant
    response_remove = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert: remove succeeded and participant gone
    assert response_remove.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]
