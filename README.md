# logy

> Terminal-first professional memory for builders.

Capture what you build every day. Browse your history. Never lose your engineering journey.

```bash
uv run logy
```

## Quick Start

```bash
uv venv
source .venv/bin/activate
uv sync
uv run logy
```

Choose from 4 tracks:

- **Daily Log** — What did you build or learn today?
- **Project** — Log work for a specific project (select or create)
- **Hard Problem** — Solved something tough? Record context, solution, and lessons
- **Recent Entries** — Browse your full history with arrow keys

## Power-User Commands

```bash
uv run logy log create "message" --project X --category Y --difficulty Z --tags "a,b"
uv run logy log list
uv run logy search search "query"
uv run logy projects list
uv run logy projects timeline "project-name"
uv run logy review weekly
uv run logy serve start
```

## Tech Stack

| Layer | Choice |
|-------|--------|
| Runtime | Python 3.12+ |
| CLI | Typer + Rich |
| TUI | Textual |
| API | FastAPI |
| Database | SQLite via SQLModel |
| AI | LiteLLM |
| Knowledge Graph | Cognee + NetworkX |
| Web | React + Vite + Tailwind CSS |
| Package Manager | uv |
| Linter | ruff |

## Project Structure

```
apps/
├── cli/          # Typer CLI + interactive TUI
├── tui/          # Textual TUI
├── server/       # FastAPI backend
└── web/          # React dashboard
packages/
├── ai/           # LiteLLM enrichment
├── cognee/       # Cognee integration
├── database/     # SQLModel models
└── shared/       # Config, constants, utils
```

## Principles

- **Terminal-first** — logging happens where work happens
- **Human-first** — you write every entry; AI enriches, never writes
- **Local-first** — everything works offline
- **Fast** — entry in under 2 minutes
- **Permanent memory** — every entry feeds the lifelong graph

## Development

```bash
uv run ruff check .
uv run ruff format .
uv run pytest
```
