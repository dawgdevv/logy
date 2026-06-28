import uuid

from fastapi.testclient import TestClient

from apps.server.main import app

client = TestClient(app)


class TestHealthEndpoint:
    def test_health(self) -> None:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestEntriesAPI:
    def test_list_entries(self) -> None:
        response = client.get("/api/entries/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_create_entry(self) -> None:
        response = client.post(
            "/api/entries/",
            json={
                "content": "API test entry",
                "category": "testing",
                "difficulty": "easy",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["content"] == "API test entry"
        assert data["category"] == "testing"

    def test_get_entry(self) -> None:
        create_response = client.post(
            "/api/entries/",
            json={"content": "To fetch"},
        )
        entry_id = create_response.json()["id"]

        response = client.get(f"/api/entries/{entry_id}")
        assert response.status_code == 200
        assert response.json()["id"] == entry_id

    def test_get_entry_not_found(self) -> None:
        response = client.get("/api/entries/999")
        assert response.status_code == 404

    def test_update_entry(self) -> None:
        create_response = client.post(
            "/api/entries/",
            json={"content": "Original"},
        )
        entry_id = create_response.json()["id"]

        response = client.put(
            f"/api/entries/{entry_id}",
            json={"content": "Updated"},
        )
        assert response.status_code == 200
        assert response.json()["content"] == "Updated"

    def test_delete_entry(self) -> None:
        create_response = client.post(
            "/api/entries/",
            json={"content": "To delete"},
        )
        entry_id = create_response.json()["id"]

        response = client.delete(f"/api/entries/{entry_id}")
        assert response.status_code == 204

    def test_delete_entry_not_found(self) -> None:
        response = client.delete("/api/entries/999")
        assert response.status_code == 404


class TestProjectsAPI:
    def test_list_projects(self) -> None:
        response = client.get("/api/projects/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_create_project(self) -> None:
        name = f"API Test {uuid.uuid4().hex[:8]}"
        response = client.post(
            "/api/projects/",
            json={"name": name, "description": "Test"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == name

    def test_get_project(self) -> None:
        name = f"Fetch Me {uuid.uuid4().hex[:8]}"
        create_response = client.post(
            "/api/projects/",
            json={"name": name},
        )
        project_id = create_response.json()["id"]

        response = client.get(f"/api/projects/{project_id}")
        assert response.status_code == 200
        assert response.json()["id"] == project_id

    def test_get_project_not_found(self) -> None:
        response = client.get("/api/projects/999")
        assert response.status_code == 404
