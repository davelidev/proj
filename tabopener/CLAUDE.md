# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running

```bash
python3 app.py                        # starts on port 5072
TABOPENER_PORT=8080 python3 app.py    # custom port
```

Open `http://localhost:5072` in a browser. No install step — pure Python stdlib, no dependencies.

## Architecture

Two files:

- **`app.py`** — Python HTTP server (`http.server.BaseHTTPRequestHandler`). Queries Terminal.app via AppleScript (`osascript`) and `ps`/`lsof`. Serves `index.html` and a small REST API.
- **`index.html`** — Single-page Bootstrap 5 + vanilla JS frontend. Polls `/api/tabs` every 500ms and renders tab rows in-place (DOM diff by `data-tty`).

**macOS-only.** All terminal introspection uses AppleScript and macOS process tools.

## API surface

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/tabs` | All Terminal.app tabs with model/ctx/rate data |
| GET | `/api/claude` | Claude usage from statusline-cache |
| POST | `/api/focus` | Bring a Terminal window to front |
| POST | `/api/rename` | Set a tab's custom title (auto-pins it) |
| POST | `/api/title-mode` | Pin (`manual`) or unpin (`auto`) a tab title |
| POST | `/api/spawn` | Open a new Terminal tab and run a command |
| POST | `/api/reorder` | Persist global tty ordering |

## In-memory state

- `_global_order` — list of ttys defining sort order, updated by `/api/reorder`
- `_manual_titles` — pinned tab titles (tty → title/winId/tabId), protected by `_manual_lock`
- `_manual_title_worker` background thread re-applies pinned titles every 2s to fight Claude Code's OSC title overwrites

## Data sources

- **Claude sessions**: `~/.claude/sessions/<pid>.json` (cwd + sessionId) → `~/.claude/projects/<dir>/<sid>.jsonl` (token usage), `~/.claude/statusline-cache/*.json` (model, ctx%, rate limits)
- **Gemini sessions**: process list filtered for `gemini` args; cwd via `lsof`; session JSONL matched by SHA-256 project hash in `~/.gemini/tmp/`
- **Daily stats**: `~/.claude/stats-cache.json`
