from src import app as app_module


def test_root_redirects_to_static_index(client):
    # Arrange
    endpoint = "/"

    # Act
    response = client.get(endpoint, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_expected_structure(client):
    # Arrange
    endpoint = "/activities"

    # Act
    response = client.get(endpoint)
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(payload, dict)
    assert "Chess Club" in payload
    assert "participants" in payload["Chess Club"]


def test_signup_successfully_registers_participant(client):
    # Arrange
    activity = "Debate Club"
    email = "new.student@mergington.edu"
    endpoint = f"/activities/{activity}/signup"

    # Act
    response = client.post(endpoint, params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Signed up {email} for {activity}"
    assert email in app_module.activities[activity]["participants"]


def test_signup_rejects_duplicate_participant(client):
    # Arrange
    activity = "Chess Club"
    existing_email = "michael@mergington.edu"
    endpoint = f"/activities/{activity}/signup"

    # Act
    response = client.post(endpoint, params={"email": existing_email})
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Student already signed up"


def test_signup_unknown_activity_returns_not_found(client):
    # Arrange
    activity = "Unknown Club"
    email = "student@mergington.edu"
    endpoint = f"/activities/{activity}/signup"

    # Act
    response = client.post(endpoint, params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_unregister_successfully_removes_participant(client):
    # Arrange
    activity = "Basketball Team"
    email = "alex@mergington.edu"
    endpoint = f"/activities/{activity}/participants"

    # Act
    response = client.delete(endpoint, params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Unregistered {email} from {activity}"
    assert email not in app_module.activities[activity]["participants"]


def test_unregister_non_registered_participant_returns_not_found(client):
    # Arrange
    activity = "Soccer Club"
    email = "not-registered@mergington.edu"
    endpoint = f"/activities/{activity}/participants"

    # Act
    response = client.delete(endpoint, params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Student is not signed up for this activity"


def test_unregister_unknown_activity_returns_not_found(client):
    # Arrange
    activity = "Unknown Club"
    email = "student@mergington.edu"
    endpoint = f"/activities/{activity}/participants"

    # Act
    response = client.delete(endpoint, params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"
