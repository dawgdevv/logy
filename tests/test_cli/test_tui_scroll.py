from datetime import datetime
from types import SimpleNamespace

from apps.cli.tui.state import State
from apps.cli.tui.views.entry_detail import clamp_detail_scroll, move_detail_scroll
from apps.cli.tui.views.entry_list import _clamp_scroll, jump_selection, move_selection


def _entries(count: int) -> list[SimpleNamespace]:
    return [
        SimpleNamespace(
            id=index + 1,
            content=f"Entry {index + 1}",
            category="daily",
            difficulty="medium",
            project=None,
            created_at=datetime(2026, 1, 1),
        )
        for index in range(count)
    ]


def test_entry_list_scroll_follows_selection_past_first_window() -> None:
    state = State()
    state.entries = _entries(30)

    for _ in range(18):
        move_selection(state, 1, max_visible=10)

    assert state.entry_idx == 18
    assert state.entry_scroll == 9


def test_entry_list_jump_end_shows_final_entries() -> None:
    state = State()
    state.entries = _entries(30)

    jump_selection(state, 29, max_visible=10)

    assert state.entry_idx == 29
    assert state.entry_scroll == 20


def test_entry_list_clamps_after_terminal_resize() -> None:
    state = State()
    state.entries = _entries(12)
    state.entry_idx = 99
    state.entry_scroll = 99

    _clamp_scroll(state, max_visible=5)

    assert state.entry_idx == 11
    assert state.entry_scroll == 7


def test_detail_scroll_clamps_to_available_lines() -> None:
    state = State()
    state.detail_scroll = 20

    clamp_detail_scroll(state, max_visible=6, line_count=9)

    assert state.detail_scroll == 3


def test_detail_page_scroll_stays_in_bounds() -> None:
    state = State()

    move_detail_scroll(state, 6, max_visible=6, line_count=9)
    move_detail_scroll(state, 6, max_visible=6, line_count=9)

    assert state.detail_scroll == 3
