# Tab Opener 2

A fast macOS Terminal tab dashboard — rebuilt with SSE push updates and no Bootstrap.

## Features

- **SSE push** — server pushes updates only when data changes; no 500ms blind polling
- **Tab switcher** — all Terminal windows/tabs at a glance; click to bring to front
- **AI session stats** — model name, context %, 5h/7d rate limits per tab (Claude + Gemini + DeepSeek)
- **Search/filter** — live-filter by title, cwd, or model
- **Keyboard navigation** — `/` to filter, `j`/`k` to navigate, `Enter` to focus
- **Drag-to-reorder** — HTML5 drag with handle; persisted across refreshes
- **Spawn** — open new tab running Claude/Gemini/DeepSeek in a chosen directory
- **Rename + pin** — custom titles; pin to prevent Claude Code's OSC overwrites
- **Color labels** — per-tab color swatches

## Requirements

- macOS (AppleScript + Terminal.app)
- Python 3.9+ (stdlib only — no pip installs)
- Terminal.app with Accessibility/Automation permission

## Usage

```bash
python3 app.py
```

Open **http://localhost:5072**. Custom port: `TABOPENER_PORT=8080 python3 app.py`
