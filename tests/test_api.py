import pytest
from fastapi.testclient import TestClient

import app.main as main


# Create a test client connected directly to the FastAPI application.
#
# TestClient allows us to send HTTP-like requests to the application
# without starting Uvicorn or opening a real network port.
client = TestClient(main.app)


@pytest.fixture(autouse=True)
def reset_application_state():
    """
    Reset the in-memory application state before every test.

    Each test must start from a predictable and independent state.
    Since tasks are currently stored in global memory, we clear the
    task list and reset the ID counter before executing each test.
    """

    main.tasks.clear()
    main.next_id = 1


def test_health():
    """
    The liveness endpoint should report that the application is alive.
    """

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ready():
    """
    The readiness endpoint should report that the application
    is ready to receive traffic.
    """

    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_tasks():
    """
    An application with no created tasks should return an empty list.
    """

    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_create_task():
    """
    A valid POST request should create and return a new task.
    """

    response = client.post(
        "/tasks",
        json={
            "title": "Task 1",
            "completed": False,
        },
    )

    assert response.status_code == 201

    assert response.json() == {
        "id": 1,
        "title": "Task 1",
        "completed": False,
    }


def test_get_existing_task():
    """
    A task created through the API should be retrievable by its ID.
    """

    create_response = client.post(
        "/tasks",
        json={
            "title": "Task 2",
            "completed": False,
        },
    )

    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200

    assert response.json() == {
        "id": task_id,
        "title": "Task 2",
        "completed": False,
    }


def test_get_nonexistent_task():
    """
    Requesting a task that does not exist should return HTTP 404.
    """

    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_delete_existing_task():
    """
    An existing task should be deleted successfully.
    """

    create_response = client.post(
        "/tasks",
        json={
            "title": "Task to delete",
            "completed": False,
        },
    )

    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")

    assert delete_response.status_code == 204

    # Verify that the task really disappeared.
    get_response = client.get(f"/tasks/{task_id}")

    assert get_response.status_code == 404


def test_create_invalid_task():
    """
    A task without the required title field should be rejected
    by FastAPI/Pydantic validation.
    """

    response = client.post(
        "/tasks",
        json={
            "completed": False,
        },
    )

    assert response.status_code == 422