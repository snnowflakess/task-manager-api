#1.login
def register_and_login(client, email="test@example.com"):
    # Register a test user
    client.post(
        "/users",
        json={
            "name": "Test User",
            "email": email,
            "password": "TestPass123!"
        }
    )

    # Login and obtain JWT
    response = client.post(
        "/login",
        json={
            "email": email,
            "password": "TestPass123!"
        }
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


def test_login(client):
    headers = register_and_login(client)

    assert "Authorization" in headers


def test_access_without_token(client):
    response = client.get("/tasks")

    assert response.status_code == 401


def test_create_task(client):
    headers = register_and_login(client)

    response = client.post(
        "/tasks",
        headers=headers,
        json={
            "title": "Test Task",
            "description": "Testing task creation",
            "status": "PENDING",
            "priority": "HIGH",
            "due_date": "2026-12-01"
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"


def test_user_cannot_access_another_users_task(client):
    # 2.First user creates a task
    first_headers = register_and_login(
        client, "first@example.com"
    )

    task_response = client.post(
        "/tasks",
        headers=first_headers,
        json={
            "title": "Private Task",
            "description": "Belongs to first user",
            "status": "PENDING",
            "priority": "HIGH"
        }
    )

    task_id = task_response.json()["id"]

    # 3.Second user tries to access it
    second_headers = register_and_login(
        client, "second@example.com"
    )

    response = client.get(
        f"/tasks/{task_id}",
        headers=second_headers
    )

    assert response.status_code == 404


def test_task_pagination(client):
    headers = register_and_login(client)

    # 5. pagination Create three tasks
    for number in range(1, 4):
        response = client.post(
            "/tasks",
            headers=headers,
            json={
                "title": f"Pagination Task {number}",
                "description": "Testing pagination",
                "status": "PENDING",
                "priority": "MEDIUM"
            }
        )
        assert response.status_code == 200

    # Fetch first page
    first_page = client.get(
        "/tasks?skip=0&limit=2",
        headers=headers
    )

    # Fetch second page
    second_page = client.get(
        "/tasks?skip=2&limit=2",
        headers=headers
    )

    assert first_page.status_code == 200
    assert second_page.status_code == 200

    assert len(first_page.json()) == 2
    assert len(second_page.json()) == 1

    first_ids = {task["id"] for task in first_page.json()}
    second_ids = {task["id"] for task in second_page.json()}

    assert first_ids.isdisjoint(second_ids)
