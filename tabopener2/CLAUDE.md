# CLAUDE.md

## Running

```bash
python3 app.py                        # starts on port 5072
TABOPENER_PORT=8080 python3 app.py    # custom port
```

Open `http://localhost:5072`. No install — Python stdlib only.

## Architecture

| File | Role |
|------|------|
| `app.py` | `ThreadingHTTPServer`, SSE endpoint, API routes |
| `cache.py` | Background refresh thread, `threading.Condition`, in-memory state |
| `terminal.py` | AppleScript queries (tabs, focus, rename, spawn), tty→cwd |
| `sources.py` | Claude + Gemini session parsing from a single `ps` call |
| `index.html` | Minimal HTML shell |
| `style.css` | All styles, CSS custom properties |
| `app.js` | SSE client, DOM diff, filter, keyboard nav, drag-drop |

## API

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/tabs` | Cached snapshot (instant) |
| GET | `/api/stream` | SSE — pushes `data:<json>` on change, `:\n\n` heartbeat every 15s |
| GET | `/api/claude` | Claude usage from statusline-cache |
| POST | `/api/focus` | Bring Terminal window to front |
| POST | `/api/rename` | Set tab custom title (auto-pins) |
| POST | `/api/title-mode` | Pin/unpin tab title |
| POST | `/api/spawn` | Open new tab and run command |
| POST | `/api/reorder` | Persist global tty order |

## Tests

```bash
python -m pytest tests/ -v
```

## In-memory state (cache.py)

- `_global_order` — tty sort order from `/api/reorder`
- `_manual_titles` — pinned tab titles (tty → title/winId/tabId), guarded by `_manual_lock`
- `_manual_title_worker` re-applies pinned titles every 2s to fight Claude Code's OSC overwrites

## Keyboard shortcuts (browser)

| Key | Action |
|-----|--------|
| `/` | Focus filter |
| `Escape` | Clear filter, deselect |
| `j` / `↓` | Select next tab |
| `k` / `↑` | Select previous tab |
| `Enter` | Focus selected Terminal window |
