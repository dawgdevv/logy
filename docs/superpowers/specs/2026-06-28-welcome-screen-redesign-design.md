# Logy Welcome Screen Redesign — Design

## Goal

Replace the current minimal-text welcome screen with a more visually distinctive header that establishes brand presence on first launch. Keep the menu flow and keymap unchanged.

## Scope

In scope:
- `apps/cli/interactive.py` — rewrite `render_welcome` and `header_block` to use a new ASCII-art logo block, inline version badge, and tagline
- Add a `LOGO` constant + a `compact_header` helper so non-welcome screens (project picker, category picker, etc.) stay visually consistent without the big banner

Out of scope:
- Changing menu flow, key bindings, or input behavior
- Touching TUI, web, or server code
- Adding pyfiglet or other dependencies

## Design

### Logo

Block-letter rendering of "logy" using solid `█` characters. 7 rows tall, monospace-friendly. The `y` carries its descender below the baseline:

```
█      ████    █████   ██  ██
█     █    █  █     █   █ █
█     █    █  █  ███    ██
█     █    █  █     █   █
█      ████    █████   ██
█
██████
```

(Note: the exact glyphs above are illustrative — final strings will be verified by rendering in a monospace terminal and adjusted for column alignment.)

### Version

Pulled from `APP_VERSION` in `packages/shared/constants.py` (currently `"0.1.0"`), rendered as `v0.1.0` in dim white, positioned to the right of the logo, vertically aligned to the logo's middle row.

### Tagline

`Terminal-first professional memory` — italic, dim, centered below the logo block.

### Box

Keep the existing `Panel` wrapper: `box.ROUNDED`, `border_style="cyan"`, centered content via `Align.center(..., vertical="middle")`.

### Layout (inside box)

1. Big logo (bold cyan) — top
2. Version badge — right of logo, mid-row aligned
3. Tagline — italic dim, below logo
4. Menu — `▸` for selected, two columns (label left, description right), cyan-on-dim
5. Keymap — bottom: `↑↓ move    enter select    ctrl+c quit`

### Other screens (project picker, category picker, difficulty picker, entry list, entry detail, confirm)

Use `compact_header` instead of the full banner: same title style as before (`logy` bold cyan + tagline italic dim), no logo art, no version. Keeps visual rhythm without repeating the full banner on every screen.

## Implementation Plan

1. Add `LOGO_ART` (list[str] or single multiline string) and `LOGO_HEIGHT` constants near top of `interactive.py`.
2. Replace `header_block` with two functions:
   - `big_header(version_text) -> Group` — renders the full logo + version badge + tagline
   - `compact_header() -> Group` — renders just the title + tagline, no art (used by non-welcome screens)
3. Rewrite `render_welcome` to use `big_header` + menu + keymap inside the existing `make_panel` wrapper.
4. Update all non-welcome renderers (`render_picker`, `render_entry_list`, `render_entry_detail`, `render_confirm`, `render_input`) to use `compact_header` so the visual language stays consistent.
5. Verify alignment by running `uv run logy` and adjusting glyph column counts in `LOGO_ART` until logo reads cleanly.

## Verification

- `uv run ruff check apps/cli/interactive.py` — no lint errors
- `uv run logy` — welcome screen renders cleanly with logo, version, tagline, menu, keymap
- Arrow keys + Enter still navigate the menu
- All other screens still render with consistent compact header
- Other CLI commands (`log create`, `search`, etc.) unaffected

## Risks

- Monospace rendering depends on terminal font. Logo will use only `█` and space, which renders identically across all common monospace fonts (no Unicode dependency).
- Width: logo is ~30 columns wide, fits in any terminal ≥ 60 cols.
