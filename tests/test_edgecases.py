def test_signup_nonexistent_activity(client):
    # Arrange
    activity = "Fake Club"
    email = "nobody@example.com"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404


def test_remove_nonexistent_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "unknown_participant@example.com"

    # Ensure email not present
    participants = client.get("/activities").json()[activity]["participants"]
    if email in participants:
        client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Act
    response = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert response.status_code == 404
