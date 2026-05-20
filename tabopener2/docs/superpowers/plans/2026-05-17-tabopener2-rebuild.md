# tabopener2 Rebuild Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild tabopener as a 6-file Python+JS project with SSE push updates, background cache, single `ps` call, and a redesigned no-Bootstrap frontend with search/filter, keyboard nav, and drag-and-drop.

**Architecture:** A background thread in `cache.py` refreshes tab data every 400ms and notifies a `threading.Condition`; `app.py` uses `ThreadingHTTPServer` with an SSE endpoint that blocks on that condition and pushes JSON only when data changes. The frontend (`app.js`) replaces `setInterval` polling with `EventSource`.

**Tech Stack:** Python 3 stdlib only (no pip installs); vanilla JS ES2020; custom CSS (no Bootstrap)

---

## File Map

| File | Role |
|------|------|
| `sources.py` | Single `ps` call → Claude + Gemini session dicts |
| `terminal.py` | AppleScript queries, tty→cwd, focus/rename/spawn |
| `cache.py` | Background refresh thread, `threading.Condition`, in-memory state |
| `app.py` | `ThreadingHTTPServer`, SSE endpoint, all API routes |
| `index.html` | Minimal HTML shell |
| `style.css` | All styles, CSS custom properties |
| `app.js` | SSE client, DOM diff, filter, keyboard nav, drag-drop |
| `tests/test_sources.py` | Unit tests for pure functions in `sources.py` |

---

## Task 1: Scaffold

**Files:**
- Create: `sources.py`, `terminal.py`, `cache.py`, `app.py`, `index.html`, `style.css`, `app.js`, `tests/__init__.py`, `tests/test_sources.py`

- [ ] **Create the directory structure and empty files**

```bash
cd /Users/daveli/Desktop/proj/tabopener2
mkdir -p tests
touch sources.py terminal.py cache.py app.py index.html style.css app.js
touch tests/__init__.py tests/test_sources.py
```

- [ ] **Verify layout**

```bash
ls -1
# sources.py  terminal.py  cache.py  app.py  index.html  style.css  app.js
ls tests/
# __init__.py  test_sources.py
```

- [ ] **Commit**

```bash
git add sources.py terminal.py cache.py app.py index.html style.css app.js tests/
git commit -m "chore: scaffold tabopener2 file structure"
```

---

## Task 2: sources.py — pure functions (TDD)

**Files:**
- Write: `sources.py` (partial — `format_model_display`, `parse_last_usage`, `_gemini_project_hash`)
- Write: `tests/test_sources.py`

- [ ] **Write the failing tests**

```python
# tests/test_sources.py
import json
import os
import tempfile

import pytest
import sources


def test_format_model_display_claude():
    assert sources.format_model_display("claude-haiku-4-5") == "Haiku 4.5"
    assert sources.format_model_display("claude-sonnet-4-6") == "Sonnet 4.6"
    assert sources.format_model_display("claude-opus-4-7") == "Opus 4.7"


def test_format_model_display_passthrough():
    assert sources.format_model_display("gemini-2.5-pro") == "gemini-2.5-pro"
    assert sources.format_model_display("") == ""
    assert sources.format_model_display(None) == ""


def test_parse_last_usage_returns_zeros_for_empty_file():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        f.write("")
        path = f.name
    try:
        total, pct, cache_r, model = sources.parse_last_usage(path)
        assert total == 0
        assert pct == 0
        assert cache_r == 0
        assert model is None
    finally:
        os.unlink(path)


def test_parse_last_usage_reads_tokens():
    line = json.dumps({
        "message": {
            "model": "claude-sonnet-4-6",
            "usage": {
                "input_tokens": 50000,
                "cache_read_input_tokens": 10000,
                "cache_creation_input_tokens": 0,
                "output_tokens": 2000,
            }
        }
    })
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        f.write(line + "\n")
        path = f.name
    try:
        total, pct, cache_r, model = sources.parse_last_usage(path)
        assert total == 62000
        assert pct == round(min(100, 62000 / 200000 * 100))
        assert cache_r == 10000
        assert model == "claude-sonnet-4-6"
    finally:
        os.unlink(path)


def test_parse_last_usage_skips_synthetic():
    line = json.dumps({
        "message": {"model": "<synthetic>", "usage": {"input_tokens": 1000}}
    })
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        f.write(line + "\n")
        path = f.name
    try:
        _, _, _, model = sources.parse_last_usage(path)
        assert model is None
    finally:
        os.unlink(path)


def test_gemini_project_hash_is_sha256():
    import hashlib
    cwd = "/Users/test/myproject"
    expected = hashlib.sha256(os.path.abspath(cwd).encode()).hexdigest()
    assert sources._gemini_project_hash(cwd) == expected
```

- [ ] **Run tests — verify they fail**

```bash
cd /Users/daveli/Desktop/proj/tabopener2
python -m pytest tests/test_sources.py -v 2>&1 | head -30
# Expected: ImportError or AttributeError — sources has no functions yet
```

- [ ] **Implement the pure functions in sources.py**

```python
# sources.py
import hashlib
import json
import os
import subprocess
from pathlib import Path


def format_model_display(model_id: str) -> str:
    if not model_id:
        return ""
    m = model_id
    if m.lower().startswith("claude-"):
        m = m[len("claude-"):]
    parts = m.split("-")
    if len(parts) >= 2 and all(p.isdigit() for p in parts[1:]):
        return parts[0].capitalize() + " " + ".".join(parts[1:])
    return model_id


def parse_last_usage(jsonl_path: str):
    """Return (total_tokens, ctx_pct, cache_read, last_model_id)."""
    try:
        with open(jsonl_path) as f:
            last_usage = None
            last_model = None
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if '"usage"' not in line and '"model"' not in line:
                    continue
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                msg = d.get("message", {})
                if not isinstance(msg, dict):
                    continue
                m = msg.get("model")
                if isinstance(m, str) and m and m != "<synthetic>":
                    last_model = m
                u = msg.get("usage", {})
                if isinstance(u, dict) and "input_tokens" in u:
                    last_usage = u
            if last_usage:
                inp = last_usage.get("input_tokens", 0)
                cache_r = last_usage.get("cache_read_input_tokens", 0)
                cache_c = last_usage.get("cache_creation_input_tokens", 0)
                out = last_usage.get("output_tokens", 0)
                total = inp + cache_r + cache_c + out
                pct = round(min(100, total / 200000 * 100))
                return total, pct, cache_r, last_model
    except Exception:
        pass
    return 0, 0, 0, None


def _gemini_project_hash(cwd: str) -> str:
    return hashlib.sha256(os.path.abspath(cwd).encode()).hexdigest()
```

- [ ] **Run tests — verify they pass**

```bash
python -m pytest tests/test_sources.py -v
# Expected: 6 passed
```

- [ ] **Commit**

```bash
git add sources.py tests/test_sources.py
git commit -m "feat: sources pure functions with tests (format_model_display, parse_last_usage)"
```

---

## Task 3: sources.py — session detection

**Files:**
- Modify: `sources.py` (add all remaining functions)

- [ ] **Append the session-detection functions to sources.py**

```python
# Append to sources.py

def _get_default_model() -> str:
    for path in [
        Path(os.path.expanduser("~/.claude/settings.json")),
        Path(os.path.expanduser("~/.claude/claude.json")),
    ]:
        try:
            return json.loads(path.read_text()).get("model", "unknown")
        except Exception:
            pass
    return "unknown"


def _get_session_jsonl_for_pid(pid: str):
    try:
        session_path = Path(os.path.expanduser(f"~/.claude/sessions/{pid}.json"))
        if not session_path.exists():
            return None
        data = json.loads(session_path.read_text())
        sid = data.get("sessionId")
        if not sid:
            return None
        projects_dir = Path(os.path.expanduser("~/.claude/projects"))
        for proj in projects_dir.iterdir():
            if proj.is_dir():
                jl = proj / f"{sid}.jsonl"
                if jl.exists():
                    return str(jl)
            elif proj.suffix == ".jsonl" and proj.stem == sid:
                return str(proj)
    except Exception:
        pass
    return None


def _get_statusline_cache() -> dict:
    cache_by_sid = {}
    cache_dir = Path(os.path.expanduser("~/.claude/statusline-cache"))
    if not cache_dir.exists():
        return cache_by_sid
    for f in cache_dir.glob("*.json"):
        try:
            data = json.loads(f.read_text())
            sid = data.get("session_id") or data.get("sessionId")
            if not sid:
                continue
            rate = data.get("rate_limits", {})
            five = rate.get("five_hour", {})
            seven = rate.get("seven_day", {})
            model_obj = data.get("model", {}) or {}
            ctx_obj = data.get("context_window", {}) or {}
            cache_by_sid[sid] = {
                "model_display": model_obj.get("display_name") or model_obj.get("id") or "",
                "ctx_pct": round(float(ctx_obj["used_percentage"])) if ctx_obj.get("used_percentage") is not None else None,
                "rate_5h_pct": round(float(five.get("used_percentage", 0))),
                "rate_5h_resets": five.get("resets_at"),
                "rate_7d_pct": round(float(seven.get("used_percentage", 0))),
                "rate_7d_resets": seven.get("resets_at"),
            }
        except Exception:
            pass
    return cache_by_sid


def _parse_claude_session(pid: str, args: str, statusline_cache: dict) -> dict:
    model = _get_default_model()
    arg_parts = args.split()
    for i, a in enumerate(arg_parts):
        if a == "--model" and i + 1 < len(arg_parts):
            model = arg_parts[i + 1]
            break

    cwd = ""
    sid = ""
    try:
        sess_file = Path(os.path.expanduser(f"~/.claude/sessions/{pid}.json"))
        if sess_file.exists():
            sess_data = json.loads(sess_file.read_text())
            cwd = sess_data.get("cwd", "")
            sid = sess_data.get("sessionId", "")
    except Exception:
        pass

    home = os.path.expanduser("~")
    total_tokens, ctx_pct, cache_read, last_model_id = parse_last_usage(
        _get_session_jsonl_for_pid(pid) or ""
    )
    rate = statusline_cache.get(sid, {})
    return {
        "model": rate.get("model_display") or format_model_display(last_model_id) or model,
        "ctx_pct": rate.get("ctx_pct") if rate.get("ctx_pct") is not None else ctx_pct,
        "total_tokens": total_tokens,
        "cache_read": cache_read,
        "cwd": cwd.replace(home, "~") if cwd else "",
        "rate_5h_pct": rate.get("rate_5h_pct"),
        "rate_5h_resets": rate.get("rate_5h_resets"),
        "rate_7d_pct": rate.get("rate_7d_pct"),
        "rate_7d_resets": rate.get("rate_7d_resets"),
    }


def _gemini_cwd_for_pid(pid: str) -> str:
    try:
        r = subprocess.run(
            ["lsof", "-a", "-d", "cwd", "-Fn", "-p", pid],
            capture_output=True, text=True, timeout=2,
        )
        for ln in r.stdout.split("\n"):
            if ln.startswith("n") and len(ln) > 1:
                return ln[1:]
    except Exception:
        pass
    return ""


def _parse_gemini_jsonl(jsonl_path: str):
    """Return (total_tokens, model_id)."""
    try:
        total = 0
        last_model = None
        with open(jsonl_path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                m = d.get("model")
                if isinstance(m, str) and m:
                    last_model = m
                t = d.get("tokens", {})
                if isinstance(t, dict):
                    total += t.get("total", 0)
        return total, last_model
    except Exception:
        return 0, None


def _parse_gemini_session(pid: str, args: str) -> dict:
    model = ""
    arg_parts = args.split()
    for i, a in enumerate(arg_parts):
        if a in ("--model", "-m") and i + 1 < len(arg_parts):
            model = arg_parts[i + 1]
            break

    home = os.path.expanduser("~")
    cwd = _gemini_cwd_for_pid(pid)
    total_tokens = 0

    if cwd:
        proj_hash = _gemini_project_hash(cwd)
        tmp_dir = Path(os.path.expanduser("~/.gemini/tmp"))
        if tmp_dir.exists():
            best_mtime, best_path = 0, None
            for proj_dir in tmp_dir.iterdir():
                if not proj_dir.is_dir():
                    continue
                chats_dir = proj_dir / "chats"
                if not chats_dir.exists():
                    continue
                for sess_file in chats_dir.iterdir():
                    if sess_file.suffix != ".jsonl":
                        continue
                    try:
                        with open(sess_file) as f:
                            first = json.loads(f.readline().strip())
                        if first.get("projectHash") == proj_hash:
                            mtime = sess_file.stat().st_mtime
                            if mtime > best_mtime:
                                best_mtime, best_path = mtime, sess_file
                    except Exception:
                        pass
            if best_path:
                total_tokens, session_model = _parse_gemini_jsonl(str(best_path))
                if session_model and not model:
                    model = session_model

    return {
        "model": model or "gemini",
        "ctx_pct": 0,
        "total_tokens": total_tokens,
        "cache_read": 0,
        "cwd": cwd.replace(home, "~") if cwd else "",
        "rate_5h_pct": None,
        "rate_5h_resets": None,
        "rate_7d_pct": None,
        "rate_7d_resets": None,
    }


def get_sessions() -> dict:
    """Single ps call → {full_tty: session_info} for Claude + Gemini processes."""
    sessions = {}
    statusline_cache = _get_statusline_cache()
    try:
        proc = subprocess.run(
            ["ps", "-eo", "pid,tty,args"],
            capture_output=True, text=True, timeout=5,
        )
        for line in proc.stdout.strip().split("\n"):
            line = line.strip()
            if not line:
                continue
            parts = line.split(maxsplit=2)
            if len(parts) != 3:
                continue
            pid, tty, args = parts
            if tty in ("??", "console"):
                continue
            full_tty = "/dev/" + tty
            if "claude" in args and "--dangerously-skip-permissions" in args:
                sessions[full_tty] = _parse_claude_session(pid, args, statusline_cache)
            elif ("gemini" in args
                  and "geminicodeassist" not in args.lower()
                  and "Code Helper" not in args):
                sessions[full_tty] = _parse_gemini_session(pid, args)
    except Exception:
        pass
    return sessions


def get_claude_info() -> dict:
    """Return Claude sessions + today's token count for /api/claude."""
    info: dict = {"sessions": [], "today_tokens": 0}
    cache_dir = Path(os.path.expanduser("~/.claude/statusline-cache"))
    seen: dict = {}
    if cache_dir.exists():
        for f in cache_dir.glob("*.json"):
            try:
                data = json.loads(f.read_text())
                model = (data.get("model", {}).get("display_name")
                         or data.get("model", {}).get("id", "unknown"))
                ctx_pct = round(float(data.get("context_window", {}).get("used_percentage", 0)))
                cwd = data.get("workspace", {}).get("current_dir") or data.get("cwd", "")
                rate = data.get("rate_limits", {})
                five = rate.get("five_hour", {})
                seven = rate.get("seven_day", {})
                seen[model] = {
                    "model": model,
                    "ctx_pct": ctx_pct,
                    "cwd": cwd,
                    "rate_5h_pct": round(float(five.get("used_percentage", 0))),
                    "rate_5h_resets": five.get("resets_at"),
                    "rate_7d_pct": round(float(seven.get("used_percentage", 0))),
                    "rate_7d_resets": seven.get("resets_at"),
                }
            except Exception:
                pass
    info["sessions"] = list(seen.values())
    try:
        stats = json.loads(
            Path(os.path.expanduser("~/.claude/stats-cache.json")).read_text()
        )
        daily = stats.get("dailyModelTokens", [])
        if daily:
            info["today_tokens"] = sum(daily[-1].get("tokensByModel", {}).values())
    except Exception:
        pass
    return info
```

- [ ] **Run existing tests — verify still pass**

```bash
python -m pytest tests/test_sources.py -v
# Expected: 6 passed
```

- [ ] **Commit**

```bash
git add sources.py
git commit -m "feat: sources.py session detection (Claude + Gemini, single ps call)"
```

---

## Task 4: terminal.py

**Files:**
- Write: `terminal.py`

- [ ] **Write terminal.py**

```python
# terminal.py
import concurrent.futures
import os
import re
import subprocess
import threading


def get_tabs() -> list:
    """Query Terminal.app via AppleScript; return list of tab dicts."""
    script = r"""set out to ""
tell application "Terminal"
    repeat with w in windows
        set wid to id of w as text
        set frontWin to frontmost of w
        set tabList to tabs of w
        set tabIndex to 0
        set selTty to tty of selected tab of w
        repeat with t in tabList
            set tabIndex to tabIndex + 1
            set tname to custom title of t
            set ttty to tty of t
            set isActive to "0"
            if ttty is selTty then set isActive to "1"
            set out to out & wid & "|" & frontWin & "|" & isActive & "|" & tabIndex & "|" & tname & "|" & ttty & "\n"
        end repeat
    end repeat
end tell
return out"""
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=5,
        )
        tabs = []
        for line in result.stdout.strip().split("\n"):
            if not line.strip():
                continue
            parts = line.split("|", 5)
            if len(parts) == 6:
                tabs.append({
                    "winId": parts[0],
                    "frontWin": parts[1] == "true",
                    "isActive": parts[2] == "1",
                    "tabIndex": int(parts[3]),
                    "title": parts[4],
                    "tty": parts[5],
                    "tabId": parts[3],
                })
        return tabs
    except Exception:
        return []


def get_tty_cwds(ttys: set) -> dict:
    """Return {tty: cwd} for the given set of ttys, via ps + lsof."""
    cwds: dict = {}
    try:
        proc = subprocess.run(
            ["ps", "-eo", "pid=,tty="],
            capture_output=True, text=True, timeout=5,
        )
        tty_to_pids: dict = {}
        for line in proc.stdout.strip().split("\n"):
            parts = line.strip().split(None, 1)
            if len(parts) < 2:
                continue
            pid, tty = parts
            if tty in ("?", "??", "console"):
                continue
            full_tty = "/dev/" + tty
            if full_tty not in ttys:
                continue
            tty_to_pids.setdefault(full_tty, []).append(pid)
        for tty, pids in tty_to_pids.items():
            for pid in reversed(pids):
                try:
                    lsof = subprocess.run(
                        ["lsof", "-a", "-d", "cwd", "-Fn", "-p", pid],
                        capture_output=True, text=True, timeout=2,
                    )
                    for ln in lsof.stdout.split("\n"):
                        if ln.startswith("n") and len(ln) > 1:
                            cwds[tty] = ln[1:]
                            break
                    if tty in cwds:
                        break
                except Exception:
                    pass
    except Exception:
        pass
    return cwds


def _parse_gemini_statusline(win_id: str, tab_index: int):
    """Read terminal history, extract Gemini model + quota % from statusline footer."""
    try:
        script = (
            'tell application "Terminal"\n'
            f'    history of tab {tab_index} of window id {win_id}\n'
            'end tell'
        )
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=3,
        )
        if not result.stdout:
            return None, None
        for line in reversed(result.stdout.split("\n")):
            m = re.search(r'(\d+)%\s*used', line)
            if not m:
                continue
            quota = int(m.group(1))
            fields = re.split(r'\s{2,}', line.strip())
            model = fields[-2].strip() if len(fields) >= 2 else None
            return model, quota
        return None, None
    except Exception:
        return None, None


def enrich_gemini_tabs(tabs: list) -> None:
    """Mutate tabs in place: fill model + ctx_pct for Gemini tabs via AppleScript."""
    def _enrich(tab):
        model_lower = (tab.get("model") or "").lower()
        if "gemini" in model_lower or model_lower == "auto":
            term_model, quota = _parse_gemini_statusline(tab["winId"], tab["tabIndex"])
            if quota is not None:
                tab["ctx_pct"] = quota
            if term_model:
                tab["model"] = term_model

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
        list(ex.map(_enrich, tabs))


def focus_window(win_id: str) -> None:
    script = (
        'tell application "Terminal"\n'
        f'    set frontmost of window id {win_id} to true\n'
        '    activate\n'
        'end tell'
    )
    subprocess.Popen(["osascript", "-e", script])


def rename_tab(win_id: str, tab_id: str, title: str) -> None:
    safe = title.replace("\\", "\\\\").replace('"', '\\"')
    target = f"tab {tab_id} of " if tab_id else "tab 1 of "
    script = (
        'tell application "Terminal"\n'
        f'    set custom title of {target}window id {win_id} to "{safe}"\n'
        'end tell'
    )
    threading.Thread(
        target=lambda: subprocess.run(["osascript", "-e", script], timeout=5),
        daemon=True,
    ).start()


def spawn_tab(cwd: str, cmd: str) -> None:
    cwd_expanded = os.path.expanduser(cwd) if cwd else os.path.expanduser("~")
    safe_cwd = cwd_expanded.replace("\\", "\\\\").replace('"', '\\"')
    safe_cmd = cmd.replace("\\", "\\\\").replace('"', '\\"')
    full_escaped = f'cd "{safe_cwd}" && {safe_cmd}'.replace("\\", "\\\\").replace('"', '\\"')
    script = (
        'tell application "Terminal"\n'
        '    activate\n'
        '    set hasWin to (count of windows) > 0\n'
        'end tell\n'
        'if hasWin then\n'
        '    tell application "System Events" to keystroke "t" using command down\n'
        '    delay 0.25\n'
        '    tell application "Terminal"\n'
        f'        do script "{full_escaped}" in selected tab of front window\n'
        '    end tell\n'
        'else\n'
        '    tell application "Terminal"\n'
        f'        do script "{full_escaped}"\n'
        '    end tell\n'
        'end if'
    )
    threading.Thread(
        target=lambda: subprocess.run(["osascript", "-e", script], timeout=5),
        daemon=True,
    ).start()
```

- [ ] **Run tests — verify still pass**

```bash
python -m pytest tests/ -v
# Expected: 6 passed
```

- [ ] **Commit**

```bash
git add terminal.py
git commit -m "feat: terminal.py AppleScript queries, enrichment, focus/rename/spawn"
```

---

## Task 5: cache.py

**Files:**
- Write: `cache.py`

- [ ] **Write cache.py**

```python
# cache.py
import hashlib
import json
import os
import subprocess
import threading
import time

import sources
import terminal

_snapshot: bytes = b"[]"
_etag: str = ""
_cond = threading.Condition()

_global_order: list = []
_manual_titles: dict = {}   # tty -> {"title", "winId", "tabId"}
_manual_lock = threading.Lock()


def get_snapshot():
    """Return (snapshot_bytes, etag). Non-blocking."""
    with _cond:
        return _snapshot, _etag


def wait_for_change(current_etag: str, timeout: float = 15.0) -> bool:
    """Block until etag changes or timeout. Return True if data changed."""
    with _cond:
        if _etag != current_etag:
            return True
        return _cond.wait_for(lambda: _etag != current_etag, timeout=timeout)


def _build_snapshot() -> bytes:
    sessions = sources.get_sessions()
    tabs = terminal.get_tabs()

    home = os.path.expanduser("~")
    with _manual_lock:
        manual_ttys = set(_manual_titles.keys())

    for tab in tabs:
        s = sessions.get(tab["tty"], {})
        tab["model"] = s.get("model")
        tab["ctx_pct"] = s.get("ctx_pct", 0)
        tab["total_tokens"] = s.get("total_tokens", 0)
        tab["cwd"] = s.get("cwd", "")
        tab["rate_5h_pct"] = s.get("rate_5h_pct")
        tab["rate_5h_resets"] = s.get("rate_5h_resets")
        tab["rate_7d_pct"] = s.get("rate_7d_pct")
        tab["rate_7d_resets"] = s.get("rate_7d_resets")
        tab["manual"] = tab["tty"] in manual_ttys

    terminal.enrich_gemini_tabs(tabs)

    missing = {t["tty"] for t in tabs if not t["cwd"]}
    if missing:
        tty_cwds = terminal.get_tty_cwds(missing)
        for tab in tabs:
            if not tab["cwd"]:
                raw = tty_cwds.get(tab["tty"], "")
                tab["cwd"] = raw.replace(home, "~") if raw else ""

    def _sort_key(t):
        if t["tty"] in _global_order:
            return (0, _global_order.index(t["tty"]))
        return (1, int(t["winId"]), t["tabIndex"])

    tabs.sort(key=_sort_key)
    return json.dumps(tabs, ensure_ascii=False).encode()


def _refresh_loop() -> None:
    global _snapshot, _etag
    while True:
        try:
            data = _build_snapshot()
            new_etag = hashlib.md5(data).hexdigest()
            with _cond:
                if new_etag != _etag:
                    _snapshot = data
                    _etag = new_etag
                    _cond.notify_all()
        except Exception:
            pass
        time.sleep(0.4)


def _manual_title_worker() -> None:
    while True:
        time.sleep(2)
        with _manual_lock:
            items = list(_manual_titles.items())
        for tty, info in items:
            title = info.get("title", "")
            if not title:
                continue
            safe = title.replace("\\", "\\\\").replace('"', '\\"')
            win_id = info.get("winId", "")
            tab_id = info.get("tabId", "")
            try:
                if win_id:
                    target = f"tab {tab_id} of " if tab_id else "tab 1 of "
                    script = (
                        'tell application "Terminal"\n'
                        f'    set custom title of {target}window id {win_id} to "{safe}"\n'
                        'end tell'
                    )
                    subprocess.run(["osascript", "-e", script], capture_output=True, timeout=3)
                else:
                    with _manual_lock:
                        _manual_titles.pop(tty, None)
            except Exception:
                with _manual_lock:
                    _manual_titles.pop(tty, None)


def start() -> None:
    """Start background threads. Call once at server startup."""
    threading.Thread(target=_refresh_loop, daemon=True).start()
    threading.Thread(target=_manual_title_worker, daemon=True).start()
```

- [ ] **Run tests — verify still pass**

```bash
python -m pytest tests/ -v
# Expected: 6 passed
```

- [ ] **Commit**

```bash
git add cache.py
git commit -m "feat: cache.py background refresh thread, SSE condition, manual title worker"
```

---

## Task 6: app.py

**Files:**
- Write: `app.py`

- [ ] **Write app.py**

```python
#!/usr/bin/env python3
"""tabopener2 — macOS Terminal tab manager with SSE push."""

import http.server
import json
import os
import urllib.parse
from pathlib import Path

import cache
import sources
import terminal

HOST = "0.0.0.0"
PORT = int(os.environ.get("TABOPENER_PORT", 5072))
HERE = Path(__file__).parent

_STATIC = {
    "/style.css": "text/css",
    "/app.js": "application/javascript",
}


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path

        if path == "/":
            self._serve_file("index.html", "text/html; charset=utf-8")
        elif path in _STATIC:
            self._serve_file(path.lstrip("/"), _STATIC[path])
        elif path == "/api/tabs":
            data, _ = cache.get_snapshot()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(data)
        elif path == "/api/stream":
            self._sse()
        elif path == "/api/claude":
            self._json(sources.get_claude_info())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404")

    def _serve_file(self, fname: str, ct: str) -> None:
        try:
            content = (HERE / fname).read_bytes()
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("Content-Type", ct)
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(content)

    def _sse(self) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.send_header("X-Accel-Buffering", "no")
        self.end_headers()
        data, etag = cache.get_snapshot()
        try:
            self.wfile.write(b"data:" + data + b"\n\n")
            self.wfile.flush()
        except Exception:
            return
        while True:
            changed = cache.wait_for_change(etag, timeout=15.0)
            data, etag = cache.get_snapshot()
            try:
                msg = b"data:" + data + b"\n\n" if changed else b":\n\n"
                self.wfile.write(msg)
                self.wfile.flush()
            except Exception:
                return

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode() if length else "{}"
        try:
            body = json.loads(raw) if raw else {}
        except Exception:
            body = {}

        path = urllib.parse.urlparse(self.path).path

        if path == "/api/focus":
            win_id = body.get("winId")
            if win_id:
                terminal.focus_window(win_id)
            self._json({"ok": True})

        elif path == "/api/rename":
            win_id = body.get("winId", "")
            tab_id = body.get("tabId", "")
            title = body.get("title", "")
            tty = body.get("tty", "")
            if win_id and title:
                terminal.rename_tab(win_id, tab_id, title)
                if tty:
                    with cache._manual_lock:
                        cache._manual_titles[tty] = {
                            "title": title, "winId": win_id, "tabId": tab_id,
                        }
            self._json({"ok": True})

        elif path == "/api/title-mode":
            tty = body.get("tty")
            mode = body.get("mode")
            if tty and mode:
                with cache._manual_lock:
                    if mode == "manual":
                        cache._manual_titles[tty] = {
                            "title": body.get("title", ""),
                            "winId": body.get("winId", ""),
                            "tabId": body.get("tabId", ""),
                        }
                    else:
                        cache._manual_titles.pop(tty, None)
            self._json({"ok": True})

        elif path == "/api/spawn":
            cwd = body.get("cwd", "").strip()
            cmd = body.get("cmd", "").strip()
            if cmd:
                terminal.spawn_tab(cwd, cmd)
            self._json({"ok": True})

        elif path == "/api/reorder":
            order = body.get("ttyOrder")
            if order:
                cache._global_order[:] = list(order)
            self._json({"ok": True})

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404")

    def _json(self, obj) -> None:
        body = json.dumps(obj).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f"[tabopener2] {args[0]}")


if __name__ == "__main__":
    cache.start()
    server = http.server.ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Tab Opener 2: http://localhost:{PORT}")
    server.serve_forever()
```

- [ ] **Smoke-test the server starts**

```bash
python app.py &
SERVER_PID=$!
sleep 1
curl -s http://localhost:5072/api/tabs | python -m json.tool | head -20
kill $SERVER_PID
# Expected: JSON array (possibly empty if no Terminal windows open)
```

- [ ] **Commit**

```bash
git add app.py
git commit -m "feat: app.py ThreadingHTTPServer with SSE endpoint and all API routes"
```

---

## Task 7: index.html

**Files:**
- Write: `index.html`

- [ ] **Write index.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tab Opener</title>
<link rel="stylesheet" href="/style.css">
</head>
<body>
<div class="toolbar">
  <div class="toolbar-title">
    Terminal Tabs
    <span class="tab-count" id="tabCount">0</span>
  </div>
  <input id="filter" class="filter-input" type="text" placeholder="🔍 filter…" autocomplete="off">
  <div class="spawn-row">
    <input id="spawnCwd" class="spawn-cwd" type="text" placeholder="~/dir" value="">
    <select id="modelSelect" class="model-select">
      <optgroup label="Claude">
        <option value="claude-opus-4-7">Opus 4.7</option>
        <option value="claude-sonnet-4-6">Sonnet 4.6</option>
        <option value="claude-sonnet-4-5">Sonnet 4.5</option>
      </optgroup>
      <optgroup label="Gemini">
        <option value="auto">Auto (Gemini)</option>
        <option value="gemini-2.5-pro">Gemini 2.5 Pro</option>
        <option value="gemini-2.5-flash">Gemini 2.5 Flash</option>
        <option value="gemini-3-pro-preview">Gemini 3 Pro (preview)</option>
        <option value="gemini-3-flash-preview">Gemini 3 Flash (preview)</option>
      </optgroup>
      <optgroup label="DeepSeek">
        <option value="deepseek-v4-flash">DeepSeek Flash</option>
        <option value="deepseek-v4-pro">DeepSeek Pro</option>
      </optgroup>
    </select>
    <button class="btn-spawn" onclick="spawnModel()">+ Spawn</button>
  </div>
</div>
<div class="tab-list" id="tabList"></div>
<script src="/app.js"></script>
</body>
</html>
```

- [ ] **Commit**

```bash
git add index.html
git commit -m "feat: index.html minimal shell"
```

---

## Task 8: style.css

**Files:**
- Write: `style.css`

- [ ] **Write style.css**

```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg: #f5f6fa;
  --surface: #ffffff;
  --border: #e2e4ea;
  --border-hover: #0d6efd;
  --text: #1a1d23;
  --text-muted: #6b7280;
  --accent: #0d6efd;
  --accent-light: rgba(13,110,253,.1);
  --radius: 8px;
  --shadow-hover: 0 0 0 3px rgba(13,110,253,.15);
  --font-mono: "SF Mono", Menlo, monospace;
}

body {
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: 13px;
  line-height: 1.4;
  user-select: none;
  -webkit-user-select: none;
}

[contenteditable="true"] { user-select: text; -webkit-user-select: text; }

.toolbar {
  position: sticky; top: 0; z-index: 10;
  background: var(--bg);
  padding: 10px 16px 8px;
  display: flex; flex-wrap: wrap; gap: 8px; align-items: center;
  border-bottom: 1px solid var(--border);
}

.toolbar-title {
  font-size: 14px; font-weight: 600;
  display: flex; align-items: center; gap: 6px;
}

.tab-count {
  background: var(--border); border-radius: 10px;
  padding: 1px 7px; font-size: 11px; font-weight: 500; color: var(--text-muted);
}

.filter-input, .spawn-cwd {
  border: 1px solid var(--border); border-radius: 6px;
  padding: 4px 8px; font-size: 12px; outline: none;
  background: var(--surface); color: var(--text);
}

.filter-input { flex: 1; min-width: 130px; max-width: 210px; }
.spawn-cwd { width: 190px; font-family: var(--font-mono); }

.filter-input:focus, .spawn-cwd:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 2px var(--accent-light);
}

.spawn-row { display: flex; gap: 6px; align-items: center; flex-wrap: wrap; }

.model-select {
  border: 1px solid var(--border); border-radius: 6px;
  padding: 4px 8px; font-size: 12px; outline: none;
  background: var(--surface); color: var(--text); cursor: pointer;
}

.btn-spawn {
  background: var(--accent); color: #fff; border: none;
  border-radius: 6px; padding: 4px 12px; font-size: 12px;
  font-weight: 500; cursor: pointer; white-space: nowrap;
}
.btn-spawn:hover { background: #0b5ed7; }

.tab-list { padding: 8px 16px; display: flex; flex-direction: column; gap: 4px; }

.tab-row {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 8px 10px; cursor: pointer;
  transition: border-color .12s, box-shadow .12s;
}
.tab-row:hover { border-color: var(--border-hover); box-shadow: var(--shadow-hover); }
.tab-row:active { transform: scale(.998); }
.tab-row.selected { border-color: var(--accent); box-shadow: var(--shadow-hover); }
.tab-row.front { border-left: 3px solid var(--accent); }
.tab-row.dragging { opacity: .4; }
.tab-row.drag-over { border-top: 2px solid var(--accent); }

.row-main { display: flex; align-items: center; gap: 8px; min-width: 0; }

.drag-handle {
  cursor: grab; opacity: .25; font-size: 14px;
  flex-shrink: 0; line-height: 1; color: var(--text-muted);
}
.drag-handle:hover { opacity: .65; }

.color-swatch {
  width: 20px; height: 20px; border-radius: 50%; flex-shrink: 0; cursor: pointer;
  border: 2px solid transparent; transition: border-color .12s, transform .12s;
}
.color-swatch:hover { border-color: var(--accent); transform: scale(1.15); }

.tab-info { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 3px; }

.tab-title-row { display: flex; align-items: center; gap: 4px; min-width: 0; }

.tab-title-text {
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  min-width: 0; font-weight: 500;
}

.icon-btn {
  cursor: pointer; opacity: .4; font-size: 12px; flex-shrink: 0;
  transition: opacity .12s, color .12s; color: var(--text-muted); line-height: 1;
}
.icon-btn:hover { opacity: 1; color: var(--accent); }
.icon-btn.pinned { opacity: 1; color: var(--accent); }
.icon-btn.spin { animation: spin 1s linear infinite; display: inline-block; }
@keyframes spin { to { transform: rotate(360deg); } }

.tab-meta-row { display: flex; align-items: center; gap: 6px; min-width: 0; }

.model-badge {
  font-size: 11px; font-family: var(--font-mono);
  padding: 1px 6px; border-radius: 4px; flex-shrink: 0; white-space: nowrap;
}

.cwd-text {
  font-size: 11px; font-family: var(--font-mono); color: var(--text-muted);
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap; min-width: 0;
}

.stats-row {
  display: flex; align-items: center; gap: 10px;
  padding-left: 28px; margin-top: 2px; flex-wrap: wrap;
}

.stat { display: flex; align-items: center; gap: 4px; }

.stat-label {
  font-size: 10px; font-family: var(--font-mono);
  color: var(--text-muted); white-space: nowrap;
}

.bar-track {
  width: 44px; height: 5px; background: var(--border);
  border-radius: 3px; overflow: hidden;
}

.bar-fill { height: 100%; border-radius: 3px; transition: width .3s; }
.bar-fill.green { background: #22c55e; }
.bar-fill.yellow { background: #f59e0b; }
.bar-fill.red { background: #ef4444; }

.stat-pct { font-size: 10px; font-family: var(--font-mono); color: var(--text-muted); }

.palette-popup {
  position: fixed; z-index: 9999; background: var(--surface);
  border-radius: 10px; box-shadow: 0 8px 30px rgba(0,0,0,.15);
  padding: 8px; display: grid; grid-template-columns: repeat(5, 1fr); gap: 4px;
}

.palette-swatch {
  width: 26px; height: 26px; border-radius: 5px; cursor: pointer;
  border: 2px solid transparent; transition: transform .1s, border-color .1s;
}
.palette-swatch:hover { transform: scale(1.2); border-color: var(--accent); }
.palette-swatch.active { border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent-light); }
```

- [ ] **Commit**

```bash
git add style.css
git commit -m "feat: style.css custom CSS design (no Bootstrap)"
```

---

## Task 9: app.js

**Files:**
- Write: `app.js`

- [ ] **Write app.js**

```javascript
// app.js — tabopener2 frontend
(function () {
'use strict';

var PALETTE = ['#ef4444','#f97316','#f59e0b','#eab308','#84cc16',
               '#22c55e','#10b981','#14b8a6','#06b6d4','#0ea5e9',
               '#3b82f6','#6366f1','#8b5cf6','#a855f7','#d946ef',
               '#ec4899','#f43f5e','#64748b','#6b7280','#78716c'];
var FALLBACK = ['#0d6efd','#dc3545','#198754','#fd7e14','#6f42c1','#d63384'];
var PROVIDER = {claude:'#fd7e14',opus:'#fd7e14',sonnet:'#fd7e14',haiku:'#fd7e14',
                gemini:'#8b5cf6',auto:'#8b5cf6',deepseek:'#0d6efd'};

var _tabs = [], _selectedIdx = -1, _filterText = '';
var _lastActiveFrontTty = null, _lastTitleChange = {};
var _isDragging = false, _dragSrcTty = null;

// ── Storage ──────────────────────────────────────────────────────────────
function getColors() { try { return JSON.parse(localStorage.getItem('tabColors')||'{}'); } catch(e) { return {}; } }
function saveColors(c) { localStorage.setItem('tabColors', JSON.stringify(c)); }
function getOrder() { try { return JSON.parse(localStorage.getItem('tabOrder')||'[]'); } catch(e) { return []; } }
function saveOrder(o) { localStorage.setItem('tabOrder', JSON.stringify(o)); }

// ── Helpers ──────────────────────────────────────────────────────────────
function esc(s) { var d = document.createElement('div'); d.textContent = s||''; return d.innerHTML; }

function providerColor(model) {
  if (!model) return null;
  var m = model.toLowerCase();
  for (var k in PROVIDER) if (m.includes(k)) return PROVIDER[k];
  return null;
}

function barClass(pct) { return pct > 70 ? 'red' : pct > 50 ? 'yellow' : 'green'; }

function barHtml(label, pct) {
  if (pct == null) return '';
  return '<div class="stat"><span class="stat-label">'+esc(label)+'</span>'+
    '<div class="bar-track"><div class="bar-fill '+barClass(pct)+'" style="width:'+pct+'%"></div></div>'+
    '<span class="stat-pct">'+pct+'%</span></div>';
}

function visibleTabs() {
  if (!_filterText) return _tabs.slice();
  var q = _filterText;
  return _tabs.filter(function(t) {
    return (t.title||'').toLowerCase().includes(q) ||
           (t.cwd||'').toLowerCase().includes(q) ||
           (t.model||'').toLowerCase().includes(q);
  });
}

// ── API ──────────────────────────────────────────────────────────────────
function post(path, body) {
  fetch(path, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)}).catch(function(){});
}

// ── Palette popup ─────────────────────────────────────────────────────────
function showPalette(swatchEl, tty) {
  var old = document.querySelector('.palette-popup');
  if (old) old.remove();
  var cur = swatchEl.style.background;
  var popup = document.createElement('div');
  popup.className = 'palette-popup';
  PALETTE.forEach(function(hex) {
    var s = document.createElement('div');
    s.className = 'palette-swatch'+(hex===cur?' active':'');
    s.style.background = hex;
    s.onclick = function() {
      var c = getColors(); c[tty] = hex; saveColors(c);
      swatchEl.style.background = hex; popup.remove();
    };
    popup.appendChild(s);
  });
  document.body.appendChild(popup);
  var r = swatchEl.getBoundingClientRect();
  popup.style.left = Math.min(r.left, window.innerWidth - popup.offsetWidth - 10) + 'px';
  popup.style.top = (r.bottom + 6) + 'px';
  setTimeout(function() {
    document.addEventListener('click', function close(e) {
      if (!e.target.closest('.palette-popup') && !e.target.closest('.color-swatch')) {
        popup.parentNode && popup.remove();
        document.removeEventListener('click', close);
      }
    });
  }, 10);
}

// ── Inline rename ─────────────────────────────────────────────────────────
function makeEditable(span, winId, tabId, tty) {
  span.contentEditable = true; span.focus();
  var r = document.createRange(); r.selectNodeContents(span);
  var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
  span.onblur = function() {
    span.contentEditable = false;
    var t = span.textContent.trim();
    if (t) post('/api/rename', {winId:winId, tabId:tabId, title:t, tty:tty});
  };
  span.onkeydown = function(e) {
    if (e.key === 'Enter') { e.preventDefault(); span.blur(); }
    if (e.key === 'Escape') { span.contentEditable = false; }
  };
}

// ── Spawn ─────────────────────────────────────────────────────────────────
window.spawnModel = function() {
  var sel = document.getElementById('modelSelect');
  var model = sel.value;
  var group = sel.options[sel.selectedIndex].parentNode.label || '';
  var cmd;
  if (model.startsWith('deepseek')) cmd = 'deepseek --model ' + model;
  else if (model.startsWith('gemini') || model === 'auto' || group === 'Gemini')
    cmd = 'gemini' + (model !== 'auto' ? ' --model ' + model : '');
  else cmd = 'claude --dangerously-skip-permissions --model ' + model;
  var cwd = (document.getElementById('spawnCwd').value || '').trim();
  _lastActiveFrontTty && (_dragSrcTty = _lastActiveFrontTty);
  post('/api/spawn', {cwd:cwd, cmd:cmd});
};

// ── Render ────────────────────────────────────────────────────────────────
function rowHtml(t, colorHex, isThinking, isFront, isSelected, idx) {
  var mc = providerColor(t.model) || '#6b7280';
  var isGemini = (t.model||'').toLowerCase().includes('gemini') || t.model === 'auto';
  var isDeepseek = (t.model||'').toLowerCase().includes('deepseek');
  var stats = '<div class="stats-row">' + barHtml(isGemini ? 'quota' : 'ctx', t.ctx_pct);
  if (!isDeepseek && !isGemini) stats += barHtml('5h', t.rate_5h_pct) + barHtml('7d', t.rate_7d_pct);
  stats += '</div>';
  var hasBars = t.ctx_pct || t.rate_5h_pct || t.rate_7d_pct;
  var pinBtn = t.manual
    ? '<span class="icon-btn pinned" data-action="unpin">⦿</span>'
    : '<span class="icon-btn'+(isThinking?' spin':'')+'" data-action="pin">↻</span>';
  var badge = t.model
    ? '<span class="model-badge" style="background:'+mc+'22;color:'+mc+';border:1px solid '+mc+'66">'+esc(t.model)+'</span>'
    : '<span class="model-badge" style="background:#f1f5f9;color:#94a3b8;border:1px solid #e2e8f0">—</span>';
  return '<div class="row-main">'+
    '<span class="drag-handle">⠿</span>'+
    '<div class="color-swatch" style="background:'+colorHex+'" data-action="color"></div>'+
    '<div class="tab-info">'+
      '<div class="tab-title-row">'+
        '<span class="tab-title-text" data-action="edit">'+esc(t.title||'')+'</span>'+
        '<span class="icon-btn" data-action="edit" style="font-size:11px">✎</span>'+
        pinBtn+
      '</div>'+
      '<div class="tab-meta-row">'+badge+(t.cwd?'<span class="cwd-text">'+esc(t.cwd)+'</span>':'')+'</div>'+
    '</div></div>'+(hasBars?stats:'');
}

function attachEvents(row, t) {
  row.onclick = function(e) {
    if (e.target.closest('[data-action]')) return;
    post('/api/focus', {winId:t.winId});
  };
  row.addEventListener('click', function(e) {
    var el = e.target.closest('[data-action]');
    if (!el) return;
    e.stopPropagation();
    var a = el.dataset.action;
    if (a === 'color') showPalette(el, t.tty);
    else if (a === 'edit') makeEditable(row.querySelector('.tab-title-text'), t.winId, t.tabId, t.tty);
    else if (a === 'pin') post('/api/title-mode', {tty:t.tty, mode:'manual', winId:t.winId, tabId:t.tabId, title:t.title});
    else if (a === 'unpin') post('/api/title-mode', {tty:t.tty, mode:'auto', winId:t.winId, tabId:t.tabId});
  });
  row.setAttribute('draggable', 'true');
  row.addEventListener('dragstart', onDragStart);
  row.addEventListener('dragover', onDragOver);
  row.addEventListener('drop', onDrop);
  row.addEventListener('dragend', onDragEnd);
}

function renderTabs(data) {
  if (_isDragging) return;
  _tabs = data;
  var now = Date.now();
  var colors = getColors();
  var list = document.getElementById('tabList');
  var vis = new Set(visibleTabs().map(function(t) { return t.tty; }));
  var allTtys = new Set(data.map(function(t) { return t.tty; }));

  var frontTty = null;
  for (var i = 0; i < data.length; i++) { if (data[i].frontWin && data[i].isActive) { frontTty = data[i].tty; break; } }
  if (!frontTty) frontTty = _lastActiveFrontTty;

  document.getElementById('tabCount').textContent = data.length;

  var prev = null;
  data.forEach(function(t, idx) {
    if (t.title !== _lastTitleChange['t_'+t.tty]) { _lastTitleChange['t_'+t.tty] = t.title; _lastTitleChange['ts_'+t.tty] = now; }
    var isThinking = (now - (_lastTitleChange['ts_'+t.tty]||0)) < 3000;
    var colorHex = colors[t.tty] || providerColor(t.model) || FALLBACK[idx % FALLBACK.length];
    var isFront = t.tty === frontTty;
    var isSelected = idx === _selectedIdx;
    var inner = rowHtml(t, colorHex, isThinking, isFront, isSelected, idx);

    var row = list.querySelector('[data-tty="'+CSS.escape(t.tty)+'"]');
    if (!row) {
      row = document.createElement('div');
      row.className = 'tab-row'+(isFront?' front':'');
      row.dataset.tty = t.tty; row.dataset.winId = t.winId; row.dataset.tabId = t.tabId;
      list.appendChild(row);
    }
    row.classList.toggle('front', isFront);
    row.classList.toggle('selected', isSelected);
    row.style.display = _filterText && !vis.has(t.tty) ? 'none' : '';
    if (row.dataset.lastInner !== inner) { row.innerHTML = inner; row.dataset.lastInner = inner; attachEvents(row, t); }

    var expected = prev ? prev.nextSibling : list.firstChild;
    if (expected !== row) list.insertBefore(row, expected);
    prev = row;
  });

  Array.prototype.slice.call(list.children).forEach(function(r) {
    if (r.dataset.tty && !allTtys.has(r.dataset.tty)) r.remove();
  });
  _lastActiveFrontTty = frontTty;
}

// ── Drag-and-drop ─────────────────────────────────────────────────────────
function onDragStart(e) {
  _isDragging = true; _dragSrcTty = this.dataset.tty;
  this.classList.add('dragging'); e.dataTransfer.effectAllowed = 'move';
}
function onDragOver(e) {
  e.preventDefault(); e.dataTransfer.dropEffect = 'move';
  document.querySelectorAll('.drag-over').forEach(function(r) { r.classList.remove('drag-over'); });
  if (this.dataset.tty !== _dragSrcTty) this.classList.add('drag-over');
}
function onDrop(e) {
  e.preventDefault(); this.classList.remove('drag-over');
  var dst = this.dataset.tty;
  if (!dst || dst === _dragSrcTty) return;
  var si = _tabs.findIndex(function(t) { return t.tty === _dragSrcTty; });
  var di = _tabs.findIndex(function(t) { return t.tty === dst; });
  if (si < 0 || di < 0) return;
  _tabs.splice(di, 0, _tabs.splice(si, 1)[0]);
  var ttys = _tabs.map(function(t) { return t.tty; });
  saveOrder(ttys); post('/api/reorder', {ttyOrder:ttys}); renderTabs(_tabs);
}
function onDragEnd() {
  this.classList.remove('dragging');
  document.querySelectorAll('.drag-over').forEach(function(r) { r.classList.remove('drag-over'); });
  _isDragging = false; _dragSrcTty = null;
}

// ── Keyboard ──────────────────────────────────────────────────────────────
document.addEventListener('keydown', function(e) {
  var ae = document.activeElement;
  var editing = ae && (ae.tagName === 'INPUT' || ae.tagName === 'TEXTAREA' || ae.contentEditable === 'true');
  if (e.key === '/' && !editing) { e.preventDefault(); document.getElementById('filter').focus(); return; }
  if (e.key === 'Escape') {
    document.getElementById('filter').value = ''; _filterText = ''; _selectedIdx = -1;
    renderTabs(_tabs); document.getElementById('filter').blur(); return;
  }
  if (editing) return;
  var vis = visibleTabs();
  if (!vis.length) return;
  if (e.key === 'ArrowDown' || e.key === 'j') { e.preventDefault(); _selectedIdx = Math.min(_selectedIdx+1, vis.length-1); syncSelection(); }
  else if (e.key === 'ArrowUp' || e.key === 'k') { e.preventDefault(); _selectedIdx = Math.max(_selectedIdx-1, 0); syncSelection(); }
  else if (e.key === 'Enter' && _selectedIdx >= 0 && vis[_selectedIdx]) { e.preventDefault(); post('/api/focus', {winId:vis[_selectedIdx].winId}); }
});

function syncSelection() {
  document.querySelectorAll('.tab-row').forEach(function(r) { r.classList.remove('selected'); });
  var vis = visibleTabs();
  if (_selectedIdx >= 0 && vis[_selectedIdx]) {
    var row = document.querySelector('[data-tty="'+CSS.escape(vis[_selectedIdx].tty)+'"]');
    if (row) { row.classList.add('selected'); row.scrollIntoView({block:'nearest'}); }
  }
}

// ── Filter ────────────────────────────────────────────────────────────────
document.getElementById('filter').addEventListener('input', function() {
  _filterText = this.value.trim().toLowerCase(); _selectedIdx = -1; renderTabs(_tabs);
});

// ── SSE ───────────────────────────────────────────────────────────────────
var _backoff = 1000;
function connectSSE() {
  var es = new EventSource('/api/stream');
  es.onmessage = function(e) {
    _backoff = 1000;
    try {
      var data = JSON.parse(e.data);
      if (!Array.isArray(data)) return;
      var order = getOrder();
      if (order.length) data.sort(function(a,b) {
        var ai = order.indexOf(a.tty), bi = order.indexOf(b.tty);
        return (ai>=0&&bi>=0)?ai-bi:(ai>=0)?-1:(bi>=0)?1:0;
      });
      renderTabs(data);
    } catch(err) { console.warn('SSE parse error', err); }
  };
  es.onerror = function() {
    es.close(); setTimeout(connectSSE, _backoff); _backoff = Math.min(_backoff*2, 30000);
  };
}
connectSSE();

})();
```

- [ ] **Commit**

```bash
git add app.js
git commit -m "feat: app.js SSE client, DOM diff, filter, keyboard nav, drag-drop, spawn"
```

---

## Task 10: CLAUDE.md + README.md + smoke test

**Files:**
- Write: `CLAUDE.md`, `README.md`

- [ ] **Write CLAUDE.md**

```markdown
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
```

- [ ] **Write README.md**

```markdown
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
```

- [ ] **Run all tests**

```bash
python -m pytest tests/ -v
# Expected: 6 passed
```

- [ ] **Full smoke test — start server and open browser**

```bash
python3 app.py &
SERVER_PID=$!
sleep 1
# Verify static files
curl -s -o /dev/null -w "%{http_code}" http://localhost:5072/          # 200
curl -s -o /dev/null -w "%{http_code}" http://localhost:5072/style.css # 200
curl -s -o /dev/null -w "%{http_code}" http://localhost:5072/app.js    # 200
# Verify API
curl -s http://localhost:5072/api/tabs | python3 -m json.tool | head -5
# Verify SSE (wait for first event then Ctrl-C)
curl -s --max-time 3 http://localhost:5072/api/stream
kill $SERVER_PID
```

Open `http://localhost:5072` in a browser and verify:
- [ ] Tab list loads within 1 second
- [ ] Filter input works (type a word, matching tabs stay visible)
- [ ] `/` focuses filter, `Escape` clears it
- [ ] `j`/`k` and arrow keys move the selection highlight
- [ ] `Enter` brings a Terminal window to front
- [ ] Drag handle moves tabs; order persists on reload
- [ ] Spawn button opens a new Terminal tab
- [ ] Color swatch opens palette; color persists on reload
- [ ] Double-click or pencil icon enables inline rename

- [ ] **Commit**

```bash
git add CLAUDE.md README.md
git commit -m "docs: CLAUDE.md and README.md for tabopener2"
```
