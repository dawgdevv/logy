"""Seed the database with every possible case for testing."""

from packages.database.repository import Repository
from packages.shared.config import settings
from packages.shared.constants import Difficulty

# Wipe existing DB
db_path = settings.db_path
if db_path.exists():
    db_path.unlink()
db_path.parent.mkdir(parents=True, exist_ok=True)

repo = Repository(db_path)

entries = [
    # Daily entries (no project / with project)
    dict(
        content="Refactored the CLI entry system for better maintainability",
        category="daily",
        difficulty=Difficulty.medium,
    ),
    dict(
        content="Fixed a bug in the database connection pooling",
        project_name="logy",
        category="daily",
        difficulty=Difficulty.medium,
    ),
    # Hard problem entries (no project / with project)
    dict(
        content="\n".join(
            [
                "Problem: SQLModel relationships not loading",
                "Solution: Added selectinload to all relationship queries",
                "Lessons: Always check eager loading options when using SQLModel",
            ]
        ),
        category="hard_problem",
        difficulty=Difficulty.hard,
    ),
    dict(
        content="\n".join(
            [
                "Problem: Production server crashing under load",
                "Solution: Profiled with py-spy and found a connection pool bottleneck",
                "Lessons: Profile before optimising — intuition is often wrong",
            ]
        ),
        project_name="website",
        category="hard_problem",
        difficulty=Difficulty.hard,
    ),
    # Feature
    dict(
        content="Added dark mode support across the entire dashboard UI",
        project_name="website",
        category="feature",
        difficulty=Difficulty.easy,
    ),
    dict(
        content="Built a real-time notification system with WebSocket support",
        project_name="logy",
        category="feature",
        difficulty=Difficulty.hard,
    ),
    dict(
        content="Implemented keyboard shortcuts for the most common actions",
        category="feature",
        difficulty=Difficulty.medium,
    ),
    # Bugfix
    dict(
        content="Fixed the off-by-one error in the pagination component",
        project_name="website",
        category="bugfix",
        difficulty=Difficulty.easy,
    ),
    dict(
        content="Patched a memory leak in the event listener system",
        project_name="logy",
        category="bugfix",
        difficulty=Difficulty.medium,
    ),
    dict(
        content="Resolved a race condition in the task scheduler",
        category="bugfix",
        difficulty=Difficulty.hard,
    ),
    # Refactor
    dict(
        content="Extracted the authentication middleware into a reusable package",
        category="refactor",
        difficulty=Difficulty.medium,
    ),
    dict(
        content="Rewrote the legacy ORM layer to use SQLModel throughout",
        project_name="logy",
        category="refactor",
        difficulty=Difficulty.hard,
    ),
    dict(
        content="Consolidated three separate API clients into one unified client",
        project_name="website",
        category="refactor",
        difficulty=Difficulty.easy,
    ),
    # Research
    dict(
        content="Evaluated vector database options for the semantic search feature",
        category="research",
        difficulty=Difficulty.easy,
    ),
    dict(
        content="Benchmarked WebSocket vs SSE for real-time data streaming",
        project_name="website",
        category="research",
        difficulty=Difficulty.medium,
    ),
    dict(
        content="Investigated WASM performance for client-side data processing",
        category="research",
        difficulty=Difficulty.hard,
    ),
    # Learning
    dict(
        content="Completed the Advanced Rust course and applied borrow checker patterns",
        category="learning",
        difficulty=Difficulty.hard,
    ),
    dict(
        content="Learned React re-render optimisation with useMemo and useCallback",
        project_name="website",
        category="learning",
        difficulty=Difficulty.easy,
    ),
    dict(
        content="Studied distributed systems consensus algorithms (Raft)",
        category="learning",
        difficulty=Difficulty.medium,
    ),
    # Infrastructure
    dict(
        content="Set up CI/CD pipeline with GitHub Actions",
        category="infrastructure",
        difficulty=Difficulty.medium,
    ),
    dict(
        content="Migrated database from SQLite to PostgreSQL with zero downtime",
        project_name="logy",
        category="infrastructure",
        difficulty=Difficulty.hard,
    ),
    dict(
        content="Configured Kubernetes cluster for staging environment",
        category="infrastructure",
        difficulty=Difficulty.hard,
    ),
    # Documentation
    dict(
        content="Wrote API reference docs with examples in every language",
        category="documentation",
        difficulty=Difficulty.easy,
    ),
    dict(
        content="Created the onboarding guide for new team members",
        project_name="claude-tools",
        category="documentation",
        difficulty=Difficulty.medium,
    ),
    dict(
        content="Wrote architecture decision records for the past quarter",
        category="documentation",
        difficulty=Difficulty.easy,
    ),
    # Other
    dict(
        content="Planned the quarterly roadmap and prioritised the backlog",
        category="other",
        difficulty=Difficulty.medium,
    ),
    dict(
        content="Organised a team workshop on effective code review practices",
        project_name="logy",
        category="other",
        difficulty=Difficulty.easy,
    ),
    dict(
        content="Wrote a retrospective on the last sprint and action items",
        category="other",
        difficulty=Difficulty.medium,
    ),
]

for e in entries:
    repo.create_entry(
        content=e["content"],
        project_name=e.get("project_name"),
        category=e["category"],
        difficulty=e["difficulty"],
    )

print(f"\nSeeded {len(entries)} entries across all cases.\n")
print(f"{'#':>3}  {'Date':<12}  {'Difficulty':<10}  {'Category':<16}  {'Project':<14}  Content")
print("─" * 100)
for e in repo.get_entries(limit=100):
    proj = e.project.name if e.project else "—"
    line = f"  {e.id:>2}  {e.created_at:%m-%d %H:%M}"
    line += f"  {e.difficulty.value:<10}  {e.category:<16}  {proj:<14}"
    line += f"  {e.content[:55]}"
    print(line)
