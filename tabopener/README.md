# Tab Opener

A local web dashboard for managing macOS Terminal.app tabs, with live Claude and Gemini session stats.

![macOS only](https://img.shields.io/badge/macOS-only-lightgrey)

## Features

- **Tab switcher** — see all open Terminal windows/tabs at a glance; click to bring any window to front
- **AI session stats** — per-tab model name, context window %, 5-hour and 7-day rate limit usage
- **Spawn tabs** — open a new Terminal tab running Claude, Gemini, or DeepSeek in a chosen directory
- **Rename tabs** — double-click or click the pencil icon to set a custom title; pin it to prevent Claude Code from overwriting it
- **Color labels** — assign a color swatch to any tab for visual grouping
- **Drag-to-reorder** — rearrange tabs; order persists across refreshes

Supports Claude Code, Gemini CLI, and DeepSeek sessions simultaneously.

## Requirements

- macOS (uses AppleScript + Terminal.app)
- Python 3 (stdlib only, no packages to install)
- Terminal.app must be allowed Accessibility / Automation access

## Usage

```bash
python3 app.py
```

Then open **http://localhost:5072** in a browser.

To use a different port:

```bash
TABOPENER_PORT=8080 python3 app.py
```

## How it works

`app.py` is a single-file HTTP server that:

1. Queries Terminal.app via AppleScript to list all windows and tabs
2. Correlates each tab's tty with running `claude` / `gemini` / `deepseek` processes
3. Reads session metadata from `~/.claude/statusline-cache/` and `~/.gemini/tmp/` to show model and usage stats
4. Serves `index.html`, which polls `/api/tabs` every 500ms and updates the UI in place

Tab title pinning works by re-applying the custom title via AppleScript every 2 seconds in a background thread, overriding the OSC escape sequences that Claude Code uses to update titles.
