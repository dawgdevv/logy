from pathlib import Path

import pytest

from packages.database.repository import Repository
from packages.shared.constants import Difficulty


@pytest.fixture
def repo(tmp_path: Path) -> Repository:
    """Create a temporary repository for testing."""
    db_path = tmp_path / "test.db"
    return Repository(db_path)


class TestRepositoryEntries:
    def test_create_entry(self, repo: Repository) -> None:
        entry = repo.create_entry(
            content="Test entry",
            project_name="Test Project",
            category="coding",
            difficulty=Difficulty.easy,
            tags=["python", "fastapi"],
        )
        assert entry.id is not None
        assert entry.content == "Test entry"
        assert entry.category == "coding"
        assert entry.difficulty == Difficulty.easy

    def test_get_entry(self, repo: Repository) -> None:
        entry = repo.create_entry(content="Test entry")
        fetched = repo.get_entry(entry.id)
        assert fetched is not None
        assert fetched.id == entry.id
        assert fetched.content == "Test entry"

    def test_get_entry_not_found(self, repo: Repository) -> None:
        assert repo.get_entry(999) is None

    def test_get_entries(self, repo: Repository) -> None:
        repo.create_entry(content="Entry 1")
        repo.create_entry(content="Entry 2")
        repo.create_entry(content="Entry 3")
        entries = repo.get_entries()
        assert len(entries) == 3

    def test_get_entries_with_limit(self, repo: Repository) -> None:
        repo.create_entry(content="Entry 1")
        repo.create_entry(content="Entry 2")
        repo.create_entry(content="Entry 3")
        entries = repo.get_entries(limit=2)
        assert len(entries) == 2

    def test_update_entry(self, repo: Repository) -> None:
        entry = repo.create_entry(content="Original")
        updated = repo.update_entry(entry.id, content="Updated")
        assert updated is not None
        assert updated.content == "Updated"

    def test_update_entry_not_found(self, repo: Repository) -> None:
        assert repo.update_entry(999, content="Updated") is None

    def test_delete_entry(self, repo: Repository) -> None:
        entry = repo.create_entry(content="To delete")
        assert repo.delete_entry(entry.id) is True
        assert repo.get_entry(entry.id) is None

    def test_delete_entry_not_found(self, repo: Repository) -> None:
        assert repo.delete_entry(999) is False

    def test_search_entries(self, repo: Repository) -> None:
        repo.create_entry(content="Python is great")
        repo.create_entry(content="Java is okay")
        repo.create_entry(content="I love Python")
        results = repo.search_entries("Python")
        assert len(results) == 2


class TestRepositoryProjects:
    def test_create_project(self, repo: Repository) -> None:
        project = repo.create_project(name="Test Project", description="A test")
        assert project.id is not None
        assert project.name == "Test Project"

    def test_get_project(self, repo: Repository) -> None:
        project = repo.create_project(name="Test Project")
        fetched = repo.get_project(project.id)
        assert fetched is not None
        assert fetched.id == project.id

    def test_get_project_not_found(self, repo: Repository) -> None:
        assert repo.get_project(999) is None

    def test_get_project_by_name(self, repo: Repository) -> None:
        repo.create_project(name="My Project")
        project = repo.get_project_by_name("My Project")
        assert project is not None
        assert project.name == "My Project"

    def test_get_projects(self, repo: Repository) -> None:
        repo.create_project(name="Project 1")
        repo.create_project(name="Project 2")
        projects = repo.get_projects()
        assert len(projects) == 2

    def test_update_project(self, repo: Repository) -> None:
        project = repo.create_project(name="Original")
        updated = repo.update_project(project.id, name="Updated")
        assert updated is not None
        assert updated.name == "Updated"

    def test_update_project_not_found(self, repo: Repository) -> None:
        assert repo.update_project(999, name="Updated") is None

    def test_delete_project(self, repo: Repository) -> None:
        project = repo.create_project(name="To delete")
        assert repo.delete_project(project.id) is True
        assert repo.get_project(project.id) is None

    def test_delete_project_not_found(self, repo: Repository) -> None:
        assert repo.delete_project(999) is False


class TestRepositoryTags:
    def test_entry_with_tags(self, repo: Repository) -> None:
        entry = repo.create_entry(
            content="Tagged entry",
            tags=["python", "testing"],
        )
        fetched = repo.get_entry(entry.id)
        assert fetched is not None
        tag_names = [t.name for t in fetched.tags]
        assert "python" in tag_names
        assert "testing" in tag_names
