# AGENTS.md — Logy Development Guide

## Project Overview

Logy is a terminal-first professional memory system for software engineers. It captures daily work via CLI, enriches entries with AI (LiteLLM), builds a knowledge graph (Cognee + NetworkX), and surfaces everything through a web dashboard (React + Vite) and TUI (Textual).

## Tech Stack (LOCKED)

| Area | Stack |
|------|-------|
| Runtime | Python 3.12+ |
| CLI | Typer + Rich |
| TUI | Textual |
| API | FastAPI |
| Database | SQLite via SQLModel |
| Migrations | Alembic |
| AI | LiteLLM (provider-agnostic) |
| Knowledge Graph | Cognee + NetworkX |
| Web | React 18 + Vite + Tailwind CSS + React Flow |
| Package Manager | uv |
| Linter/Formatter | ruff |
| Testing | pytest |
| Pre-commit | pre-commit |

## Project Structure

```
logy/
├── apps/
│   ├── cli/          # Typer CLI
│   ├── tui/          # Textual TUI
│   ├── server/       # FastAPI backend
│   └── web/          # React dashboard
├── packages/
│   ├── ai/           # LiteLLM enrichment pipeline
│   ├── cognee/       # Cognee integration
│   ├── database/     # SQLModel models + Alembic
│   └── shared/       # Config, constants, utils
├── data/             # Runtime data (gitignored)
├── tests/
└── pyproject.toml
```

## Coding Standards

### General
- **Type hints required** on all function signatures
- **Docstrings**: only when logic is non-obvious
- **No wildcard imports** (`from x import *`)
- Follow **single responsibility** — one function, one job
- Prefer **pure functions** over side effects

### Python
- Use `ruff` for linting & formatting (line length = 100)
- Use `pathlib` for all filesystem operations
- Use Pydantic for all data validation (models, schemas)
- Use `typing` module (not 3.10+ pipe syntax for now for broad compat)
- Exception: use `str | None` is fine, just be consistent

### Imports order (sorted by ruff)
1. Standard library
2. Third-party
3. Local packages

### Database
- All models inherit from `SQLModel`
- All relationships use `back_populates`
- Migrations via Alembic (auto-generate when schema changes)

### AI
- All AI calls go through **LiteLLM** abstraction layer
- Never call OpenAI/Anthropic APIs directly
- AI enrichment runs **async** in background worker
- AI always enriches, never writes user content

### Git
- Commits: conventional commits (`feat:`, `fix:`, `chore:`)
- Branch from `main`, PR into `main`
- No force-push to main

## Common Patterns

### Adding a new CLI command
```python
# apps/cli/commands/<name>.py
import typer

app = typer.Typer()

@app.command()
def my_command(param: str = typer.Option(...)):
    """Description."""
    # logic here
```

### Adding a new API endpoint
```python
# apps/server/api/<name>.py
from fastapi import APIRouter

router = APIRouter(prefix="/resource", tags=["resource"])

@router.get("/")
def list_resources():
    ...
```

### Adding a new DB model
```python
# packages/database/models.py
from sqlmodel import SQLModel, Field, Relationship

class MyModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
```

## Verification

- `ruff check .` — no lint errors
- `pytest` — all tests pass
- `uv run ...` — entry point works

## Pre-commit hooks

Install with `pre-commit install` after cloning. Runs ruff on every commit.

## Getting Started

```bash
uv venv
source .venv/bin/activate
uv sync
pre-commit install
uv run logy --help
```
