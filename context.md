# Logy — Build Spec

> Terminal-first professional memory for builders.

---

## Core Pitch

Engineers build, debug, and decide daily—but most of that experience disappears. Logy captures it in under 2 minutes, enriches it with AI, and preserves it in a searchable knowledge graph.

---

## Locked Tech Stack

| Layer | Choice | Why |
|-------|--------|-----|
| Runtime | **Python 3.12+** | Ecosystem, type hints, speed |
| CLI | **Typer** + **Rich** | Industry standard, great DX |
| TUI | **Rich** | Terminal UI built with Rich Live |
| API | **FastAPI** | Async, auto-docs, Pydantic-native |
| DB | **SQLite** ([sqlite-utils](https://sqlite-utils.datasette.io/)) | Zero-infra, local-first, battle-tested |
| ORM | **SQLModel** | Pydantic + SQLAlchemy, no friction |
| Migrations | **Alembic** | Needed once schema evolves |
| AI | **LiteLLM** | Provider-agnostic, swap models freely |
| Knowledge | **Cognee** | Graph builder + semantic search |
| Graph | **NetworkX** | Graph model for knowledge representation |
| Web | **React 18** + **Vite** + **Tailwind CSS** | Standard modern stack |
| Graph Viz | **React Flow** | Interactive knowledge graph |
| Package mgmt | **uv** | Fast Python package manager |
| Linting | **ruff** | Fast, unified linter + formatter |
| Testing | **pytest** | Standard |
| Pre-commit | **pre-commit** | Automated quality gates |

**AI Constraint**: AI *enriches* entries (grammar, entities, tech extraction). AI never *writes* them.

---

## Architecture

```text
typer CLI  ──►  Rich TUI  ──►  FastAPI  ──►  SQLite (source of truth)
                                        │
                                   LiteLLM enrichment
                                        │
                                    cognee engine
                                        │
                              knowledge graph (NetworkX)
                                        │
                              react flow web dashboard
```

---

## Folder Structure

```text
logy/
├── apps/
│   ├── cli/             # Typer CLI entrypoint + commands
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── commands/
│   │   │   ├── log.py
│   │   │   ├── search.py
│   │   │   ├── projects.py
│   │   │   ├── review.py
│   │   │   └── serve.py
│   │   └── tui/         # Rich TUI
│   │       ├── __init__.py
│   │       ├── app.py
│   │       ├── flow.py
│   │       ├── keys.py
│   │       ├── state.py
│   │       └── views/
│   ├── server/          # FastAPI backend
│   │   ├── api/
│   │   ├── services/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── database/
│   │   └── workers/
│   └── web/             # React + Vite dashboard
│       ├── src/
│       ├── pages/
│       ├── graph/
│       └── components/
├── packages/
│   ├── ai/              # LiteLLM enrichment pipeline
│   │   ├── __init__.py
│   │   ├── extraction.py
│   │   ├── grammar.py
│   │   └── prompts/
│   ├── cognee/          # Cognee integration
│   │   ├── __init__.py
│   │   ├── ingest.py
│   │   ├── graph.py
│   │   ├── search.py
│   │   ├── relationships.py
│   │   └── memory.py
│   ├── shared/          # Shared config, constants, utils
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── constants.py
│   │   └── utils.py
│   └── database/        # SQLModel models + migrations
│       ├── __init__.py
│       ├── models.py
│       ├── migrations/
│       └── repository.py
├── data/                # Runtime data (gitignored)
│   ├── sqlite.db
│   └── graph/
├── tests/
│   ├── test_cli/
│   ├── test_api/
│   ├── test_ai/
│   └── test_cognee/
├── pyproject.toml
├── README.md
├── CONTEXT.md           # ← this file
└── AGENTS.md
```

---

## Build Phases

### Phase 1 — Core CLI (Days 1-2)
- `pyproject.toml` with uv, ruff config
- Typer CLI with `log`, `search`, `projects`, `serve` commands
- SQLModel schema + SQLite setup
- `log` command writes entries to DB

### Phase 2 — AI Enrichment (Days 3-4)
- LiteLLM integration (provider-agnostic)
- Grammar correction pipeline
- Entity + technology extraction
- Difficulty estimation
- Background enrichment worker

### Phase 3 — Knowledge Graph (Days 5-6)
- Cognee ingestion pipeline
- NetworkX graph construction
- Semantic search via Cognee
- Relationship extraction

### Phase 4 — Web Dashboard (Days 7-9)
- React + Vite + Tailwind scaffolding
- FastAPI serves API
- Timeline view
- Interactive knowledge graph (React Flow)
- Weekly review generation

### Phase 5 — TUI (Days 10-12)
- Rich TUI with screens for log, search, projects, review
- Rich formatting for terminal display
- Streak tracking

---

## MVP Scope

- Daily logging with `log` command
- Project management (create, list, timeline)
- Semantic search via Cognee
- AI enrichment (grammar, entities, tech, difficulty)
- Interactive knowledge graph (web)
- Timeline view (CLI + web)
- Weekly review auto-generation
- Streak tracking

---

## Out of Scope (for MVP)

Auth, cloud sync, teams, mobile, AI chat, markdown editor, attachments, GitHub integration, VS Code extension, resume generator, interview mode.

---

## Design Principles

- **Terminal-first**: logging happens where work happens
- **Human-first**: user writes every entry; reflection IS the product
- **AI-assisted**: AI enriches, never writes
- **Local-first**: everything works offline; net only for AI
- **Fast**: entry in under 2 minutes
- **Permanent memory**: every entry feeds the lifelong graph
