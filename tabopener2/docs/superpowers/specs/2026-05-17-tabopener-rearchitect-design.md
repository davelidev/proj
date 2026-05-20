# tabopener2 — Rearchitect Design

**Date:** 2026-05-17  
**Status:** Approved  
**Scope:** Full rebuild of `../tabopener` into `tabopener2` — improved performance (SSE, background cache, single `ps` call) and improved frontend (no Bootstrap, search/filter, keyboard nav, drag-drop).

---

## Goals

- Eliminate polling lag: replace 500ms `setInterval` with Server-Sent Events
- Move expensive work (AppleScript, `lsof`, JSONL parsing) off the request path into a background cache thread
- Split the 780-line monolith into focused modules
- Redesign frontend: no CDN dependencies, search/filter, keyboard navigation, proper drag-and-drop
- Zero new runtime dependencies: Python stdlib only

---

## Backend Architecture

### File layout

```
tabopener2/
├── app.py          ← HTTP handler, SSE endpoint, static file serving, server startup
├── cache.py        ← background refresh thread, snapshot store, change detection
├── terminal.py     ← AppleScript Terminal.app queries, tty→cwd resolution
├── sources.py      ← Claude + Gemini session parsing (single shared ps call)
├── index.html
├── style.css
└── app.js
```

### cache.py — background refresh + SSE notification

- One background daemon thread, refresh interval ~400ms
- Each cycle:
  1. Call `sources.get_sessions()` (single `ps` call → Claude + Gemini) → `dict[tty, session_info]`
  2. Call `terminal.get_tabs()` (AppleScript list) → `list[dict]`
  3. Merge: for each tab, look up `session_info` by `tab["tty"]` and attach fields (`model`, `ctx_pct`, etc.)
  4. Call `terminal.enrich_gemini_tabs(tabs)` (parallel AppleScript statusline reads, mutates in place)
  5. Resolve missing cwds via `terminal.get_tty_cwds()`
  6. Apply sort order from `_global_order`
  7. JSON-serialize result, hash it (md5 of bytes)
  8. If hash changed: store new snapshot, notify `threading.Condition`
- Exposes:
  - `get_snapshot() -> (bytes, str)` — current JSON bytes + etag
  - `wait_for_change(current_etag, timeout=15) -> bool` — blocks until hash changes or timeout
- Also owns `_global_order`, `_manual_titles`, `_manual_lock`, `_manual_title_worker` thread

### terminal.py — AppleScript + process queries

- `get_tabs() -> list[dict]` — AppleScript query for all Terminal windows/tabs
- `get_tty_cwds(ttys) -> dict` — `lsof` fallback for missing cwds
- `enrich_gemini_tabs(tabs)` — parallel AppleScript statusline reads via `ThreadPoolExecutor`
- `focus_window(win_id)` — AppleScript bring-to-front
- `rename_tab(win_id, tab_id, title)` — AppleScript set custom title
- `spawn_tab(cwd, cmd)` — AppleScript open new tab + run command

### sources.py — session data

- `get_sessions() -> dict[tty, session_info]` — single `ps -eo pid,tty,args` call; routes each process to Claude or Gemini parser
- `parse_claude_session(pid, tty, args) -> dict` — reads `~/.claude/sessions/<pid>.json`, statusline-cache, JSONL
- `parse_gemini_session(pid, tty, args) -> dict` — reads cwd via `lsof`, finds matching JSONL by project hash
- `format_model_display(model_id) -> str` — unchanged from original
- `get_claude_info() -> dict` — statusline-cache summary + daily tokens (for `/api/claude`)

### app.py — HTTP handler

- Uses `ThreadingHTTPServer` (stdlib, one thread per connection)
- GET `/` — serve `index.html`
- GET `/style.css`, `/app.js` — serve static files from same directory
- GET `/api/tabs` — return `cache.get_snapshot()` bytes directly (instant, no work)
- GET `/api/stream` — SSE: loop calling `cache.wait_for_change(etag)`, emit `data:<json>\n\n` on change, `:\n\n` heartbeat on timeout
- GET `/api/claude` — call `sources.get_claude_info()` directly (cheap, cached data)
- POST `/api/focus` — call `terminal.focus_window(win_id)`
- POST `/api/rename` — call `terminal.rename_tab(...)`, update `cache._manual_titles`
- POST `/api/title-mode` — update `cache._manual_titles`
- POST `/api/spawn` — call `terminal.spawn_tab(cwd, cmd)` in daemon thread
- POST `/api/reorder` — update `cache._global_order`

---

## API Surface

| Method | Path | Notes |
|--------|------|-------|
| GET | `/` | index.html |
| GET | `/style.css` | static |
| GET | `/app.js` | static |
| GET | `/api/tabs` | cached snapshot, instant response |
| GET | `/api/stream` | **new** SSE stream |
| GET | `/api/claude` | unchanged |
| POST | `/api/focus` | unchanged |
| POST | `/api/rename` | unchanged |
| POST | `/api/title-mode` | unchanged |
| POST | `/api/spawn` | unchanged |
| POST | `/api/reorder` | unchanged |

SSE event format: `data:<json-array>\n\n` (same shape as `/api/tabs` response).  
Heartbeat: `:\n\n` every 15s (keeps proxies from closing the connection).

---

## Frontend

### Files

- `index.html` — minimal shell: `<link>` + `<script>` tags, one `<div id="app">`
- `style.css` — all styles, CSS custom properties for theming, no external deps
- `app.js` — all logic, vanilla JS ES2020, no build step

### Layout

```
┌─────────────────────────────────────────────────────┐
│  Terminal Tabs  [12]     [🔍 filter…]               │
│  [~/Desktop/proj] [Opus 4.7 ▾] [+ Spawn]           │
├─────────────────────────────────────────────────────┤
│ ⠿ ● │ my-project          [Sonnet 4.6]  ~/proj/foo  │
│      │ ctx ▓▓▓░░ 42%  5h ▓░░░ 12%  7d ░░░ 3%       │
├─────────────────────────────────────────────────────┤
│ ⠿ ● │ gemini-research     [Gemini 2.5]  ~/notes     │
│      │ quota ▓░░░░ 18%                              │
└─────────────────────────────────────────────────────┘
```

### SSE client (`app.js`)

```
EventSource('/api/stream')
  onmessage → parse JSON → diff + render
  onerror   → reconnect with exponential backoff (1s → 2s → 4s → … → 30s cap)
```

DOM diff strategy: keyed by `tty` (same as original `data-tty` approach), but HTML is only rewritten when the serialized row data changes.

### Search / filter

- `<input id="filter">` in the toolbar
- Filters visible tabs by: title, cwd, model (case-insensitive substring)
- Non-matching rows get `display:none` (not removed from DOM — preserves drag state)
- Filter is client-side only, no server round-trip

### Keyboard navigation

| Key | Action |
|-----|--------|
| `/` | Focus filter input |
| `Escape` | Clear filter, deselect |
| `↑` / `k` | Move cursor up through visible tabs |
| `↓` / `j` | Move cursor down through visible tabs |
| `Enter` | Focus selected Terminal window |

Cursor is a CSS `--selected` highlight; arrow keys skip hidden (filtered-out) rows.

### Drag-and-drop

- HTML5 drag API: `draggable="true"` on each row, drag handle `⠿` as visual affordance
- Events: `dragstart`, `dragover`, `drop`, `dragend`
- On drop: reorder the in-memory array, re-render, save to `localStorage`, POST `/api/reorder`
- Dragging tab gets `opacity:0.4`; drop target gets a blue top-border indicator

### Color swatch / palette

- Unchanged behavior: click swatch opens inline palette popup
- Palette colors hardcoded (20 colors), saved to `localStorage['tabColors']`
- Popup positioned via `getBoundingClientRect`, closed on outside click

### Provider color badges

| Provider | Color |
|----------|-------|
| Claude (opus/sonnet/haiku) | `#fd7e14` (orange) |
| Gemini / auto | `#8b5cf6` (purple) |
| DeepSeek | `#0d6efd` (blue) |
| Unknown | `#6c757d` (grey) |

### Progress bars

Pure CSS — no Bootstrap. A `<div class="bar-track"><div class="bar-fill" style="width:42%"></div></div>` pattern.  
Color thresholds: `< 50%` green, `50–70%` yellow, `> 70%` red (same logic as original).

### Rename / pin

- Double-click title or click pencil `✎` → `contentEditable=true`, select-all
- Enter or blur → POST `/api/rename`
- Pin button `⦿` (pinned) / `↻` (auto, spins if title changed in last 3s) → POST `/api/title-mode`

---

## Performance Summary

| Problem in original | Fix in tabopener2 |
|---------------------|-------------------|
| AppleScript on every request | Background thread; requests hit cache |
| `ps` called twice (Claude + Gemini) | Single call in `sources.get_sessions()` |
| 500ms blind polling | SSE push; browser only wakes on change |
| Synchronous single-threaded server | `ThreadingHTTPServer` |
| Gemini statusline reads serial | Already parallelized; kept |

---

## Non-goals

- No authentication (local tool, loopback only)
- No persistence beyond `localStorage` and in-memory state (same as original)
- No support for terminal emulators other than Terminal.app
- No Windows/Linux support
