#!/usr/bin/env python3
"""Tab opener — list Terminal.app windows, bring them to front, show Claude/Gemini stats."""

import http.server
import hashlib
import json
import urllib.parse
import subprocess
import os
import threading
import time
from pathlib import Path

HOST = "0.0.0.0"
PORT = int(os.environ.get("TABOPENER_PORT", 5072))
HERE = Path(__file__).parent

# Saved global tab order: [tty1, tty2, ...]
_global_order = []

# Manual (pinned) titles: tty -> {"title": str, "winId": str, "tabId": str}
_manual_titles = {}
_manual_lock = threading.Lock()


def get_default_model():
    """Read the default model from settings.json / claude.json."""
    for path in [
        Path(os.path.expanduser("~/.claude/settings.json")),
        Path(os.path.expanduser("~/.claude/claude.json")),
    ]:
        try:
            return json.loads(path.read_text()).get("model", "unknown")
        except Exception:
            pass
    return "unknown"


def get_session_jsonl_for_pid(pid):
    """Find session JSONL file via ~/.claude/sessions/<pid>.json."""
    try:
        session_path = Path(os.path.expanduser(f"~/.claude/sessions/{pid}.json"))
        if session_path.exists():
            data = json.loads(session_path.read_text())
            sid = data.get("sessionId")
            if sid:
                projects_dir = Path(os.path.expanduser("~/.claude/projects"))
                for proj in projects_dir.iterdir():
                    if proj.is_dir() or proj.suffix != ".jsonl":
                        jl = proj / f"{sid}.jsonl" if proj.is_dir() else None
                        if jl and jl.exists():
                            return str(jl)
                    # Also check flat .jsonl files in projects dir
                    if proj.suffix == ".jsonl" and proj.stem == sid:
                        return str(proj)
    except Exception:
        pass
    return None


def parse_last_usage(jsonl_path):
    """Return (total_tokens, ctx_pct, cache_read, last_model_id) from the JSONL."""
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
                except:
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


def format_model_display(model_id):
    """Convert a raw model id like 'claude-haiku-4-5' -> 'Haiku 4.5'."""
    if not model_id:
        return ""
    m = model_id
    if m.lower().startswith("claude-"):
        m = m[len("claude-"):]
    parts = m.split("-")
    if len(parts) >= 2 and all(p.isdigit() for p in parts[1:]):
        return parts[0].capitalize() + " " + ".".join(parts[1:])
    return model_id


def get_claude_sessions_by_tty():
    """Return dict mapping /dev/ttysXXX -> {model, ctx_pct, total_tokens} for running Claude sessions."""
    default_model = get_default_model()
    sessions = {}

    # Read statusline cache for model + rate data, keyed by session_id
    cache_by_sid = {}
    cache_dir = Path(os.path.expanduser("~/.claude/statusline-cache"))
    if cache_dir.exists():
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
                    "ctx_pct": round(float(ctx_obj.get("used_percentage", 0))) if ctx_obj.get("used_percentage") is not None else None,
                    "rate_5h_pct": round(float(five.get("used_percentage", 0))),
                    "rate_5h_resets": five.get("resets_at"),
                    "rate_7d_pct": round(float(seven.get("used_percentage", 0))),
                    "rate_7d_resets": seven.get("resets_at"),
                }
            except Exception:
                pass

    try:
        proc = subprocess.run(
            ["ps", "-eo", "pid,tty,args"],
            capture_output=True, text=True, timeout=5
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
            if "claude" in args and "--dangerously-skip-permissions" in args:
                model = default_model
                arg_parts = args.split()
                for i, a in enumerate(arg_parts):
                    if a == "--model" and i + 1 < len(arg_parts):
                        model = arg_parts[i + 1]
                        break

                full_tty = "/dev/" + tty
                total_tokens, ctx_pct, cache_read, last_model_id = parse_last_usage(get_session_jsonl_for_pid(pid) or "")
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
                short_cwd = cwd.replace(home, "~") if cwd else ""
                rate = cache_by_sid.get(sid, {})
                sessions[full_tty] = {
                    "model": rate.get("model_display") or format_model_display(last_model_id) or model,
                    "ctx_pct": rate.get("ctx_pct") if rate.get("ctx_pct") is not None else ctx_pct,
                    "total_tokens": total_tokens,
                    "cache_read": cache_read,
                    "cwd": short_cwd or cwd,
                    "rate_5h_pct": rate.get("rate_5h_pct"),
                    "rate_5h_resets": rate.get("rate_5h_resets"),
                    "rate_7d_pct": rate.get("rate_7d_pct"),
                    "rate_7d_resets": rate.get("rate_7d_resets"),
                }
    except Exception:
        pass
    return sessions


# ── Gemini session parsing ───────────────────────────────────────────

def get_gemini_project_hash(cwd):
    """SHA-256 of the absolute directory path (matches Gemini CLI's project hash)."""
    return hashlib.sha256(os.path.abspath(cwd).encode()).hexdigest()


def parse_gemini_session_usage(jsonl_path):
    """Return (total_tokens, model_id) from a Gemini session JSONL file."""
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


def get_gemini_sessions_by_tty():
    """Return dict mapping /dev/ttysXXX -> {model, ctx_pct, total_tokens, cwd} for running Gemini sessions."""
    sessions = {}
    try:
        proc = subprocess.run(
            ["ps", "-eo", "pid,tty,args"],
            capture_output=True, text=True, timeout=5
        )
        home = os.path.expanduser("~")
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
            # Match gemini CLI but NOT the VS Code extension
            if "gemini" not in args or "geminicodeassist" in args.lower() or "Code Helper" in args:
                continue

            model = ""
            arg_parts = args.split()
            for i, a in enumerate(arg_parts):
                if a in ("--model", "-m") and i + 1 < len(arg_parts):
                    model = arg_parts[i + 1]
                    break

            full_tty = "/dev/" + tty

            # Get cwd via lsof
            cwd = ""
            try:
                lsof = subprocess.run(
                    ["lsof", "-a", "-d", "cwd", "-Fn", "-p", pid],
                    capture_output=True, text=True, timeout=2,
                )
                for ln in lsof.stdout.split("\n"):
                    if ln.startswith("n") and len(ln) > 1:
                        cwd = ln[1:]
                        break
            except Exception:
                pass

            short_cwd = cwd.replace(home, "~") if cwd else ""

            # Find session JSONL
            total_tokens = 0
            if cwd:
                proj_hash = get_gemini_project_hash(cwd)
                # Search all project tmp dirs for matching chats
                tmp_dir = Path(os.path.expanduser("~/.gemini/tmp"))
                if tmp_dir.exists():
                    best_mtime = 0
                    best_path = None
                    for proj_dir in tmp_dir.iterdir():
                        if not proj_dir.is_dir():
                            continue
                        chats_dir = proj_dir / "chats"
                        if not chats_dir.exists():
                            continue
                        for sess_file in chats_dir.iterdir():
                            if not sess_file.suffix == ".jsonl":
                                continue
                            try:
                                with open(sess_file) as f:
                                    first = json.loads(f.readline().strip())
                                if first.get("projectHash") == proj_hash:
                                    mtime = sess_file.stat().st_mtime
                                    if mtime > best_mtime:
                                        best_mtime = mtime
                                        best_path = sess_file
                            except Exception:
                                pass
                    if best_path:
                        total_tokens, session_model = parse_gemini_session_usage(str(best_path))
                        if session_model and not model:
                            model = session_model

            sessions[full_tty] = {
                "model": model or "gemini",
                "ctx_pct": 0,  # filled later by terminal read
                "total_tokens": total_tokens,
                "cache_read": 0,
                "cwd": short_cwd or cwd,
                "rate_5h_pct": None,
                "rate_5h_resets": None,
                "rate_7d_pct": None,
                "rate_7d_resets": None,
            }
    except Exception:
        pass
    return sessions


# ── End Gemini ───────────────────────────────────────────────────────


def parse_gemini_statusline(win_id, tab_index):
    """Read a Gemini tab's terminal history and extract model + quota from the statusline.
    Returns (model_name, quota_pct) or (None, None) if unreadable.

    The Gemini statusline footer looks like:
        workspace (/directory)      branch     sandbox         /model                   quota
        ~/Desktop/...               main       no sandbox      Auto (Gemini 2.5)        5% used
    """
    try:
        script = (
            'tell application "Terminal"\n'
            f'    history of tab {tab_index} of window id {win_id}\n'
            'end tell'
        )
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=3
        )
        history = result.stdout
        if not history:
            return None, None
        import re
        lines = history.split("\n")
        # Find the last line with "X% used" — that's the data row of the statusline
        for i in range(len(lines) - 1, -1, -1):
            line = lines[i]
            m = re.search(r'(\d+)%\s*used', line)
            if not m:
                continue
            quota = int(m.group(1))
            # The model is the field just before the quota percentage.
            # Split on 2+ spaces and pick the second-to-last field.
            fields = re.split(r'\s{2,}', line.strip())
            if len(fields) >= 2:
                # Last field is "5% used", second-to-last is the model
                model = fields[-2].strip()
                return model, quota
            return None, quota
        return None, None
    except Exception:
        return None, None


# ──────────────────────────────────────────────────────────────────────


def get_tty_cwds(ttys):
    """Return dict mapping /dev/ttysXXX -> cwd by looking at processes on each tty."""
    cwds = {}
    try:
        proc = subprocess.run(["ps", "-eo", "pid=,tty=,lstart="], capture_output=True, text=True, timeout=5)
        tty_to_pids = {}
        for line in proc.stdout.strip().split("\n"):
            parts = line.strip().split(None, 2)
            if len(parts) < 2:
                continue
            pid, tty = parts[0], parts[1]
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


def get_terminals():
    """Return list of Terminal.app windows/tabs via AppleScript, sorted by tty, with model/usage per tab."""
    script = """set out to ""
tell application "Terminal"
    set winCount to count of windows
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
            set out to out & wid & "|" & frontWin & "|" & isActive & "|" & tabIndex & "|" & tname & "|" & ttty & "\\n"
        end repeat
    end repeat
end tell
return out"""
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=5
        )
        lines = result.stdout.strip().split("\n")
        tabs = []
        for line in lines:
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

        sessions = get_claude_sessions_by_tty()
        gemini_sessions = get_gemini_sessions_by_tty()
        sessions.update(gemini_sessions)
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

        # OPTIMIZATION: Enrich Gemini tabs in parallel
        import concurrent.futures
        def enrich_tab(tab):
            model_lower = (tab.get("model") or "").lower()
            if model_lower.startswith("gemini") or "gemini" in model_lower or model_lower == "auto":
                term_model, quota = parse_gemini_statusline(tab["winId"], tab["tabIndex"])
                if quota is not None: tab["ctx_pct"] = quota
                if term_model: tab["model"] = term_model
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(enrich_tab, tabs)

        missing = {t["tty"] for t in tabs if not t["cwd"]}
        if missing:
            tty_cwds = get_tty_cwds(missing)
            home = os.path.expanduser("~")
            for tab in tabs:
                if not tab["cwd"]:
                    raw = tty_cwds.get(tab["tty"], "")
                    tab["cwd"] = raw.replace(home, "~") if raw else ""

        global _global_order
        def sorter(t):
            if t["tty"] in _global_order:
                return (0, _global_order.index(t["tty"]))
            return (1, int(t["winId"]), t["tabIndex"])
        tabs.sort(key=sorter)
        return tabs
    except Exception as e:
        return {"error": str(e)}

def read_statusline_cache():
    """Read statusline cache files, return dict keyed by lowercased model name."""
    cache_dir = Path(os.path.expanduser("~/.claude/statusline-cache"))
    result = {}
    if not cache_dir.exists():
        return result
    for f in cache_dir.glob("*.json"):
        try:
            data = json.loads(f.read_text())
            model_display = data.get("model", {}).get("display_name") or ""
            model_id = data.get("model", {}).get("id", "")
            model = model_display or model_id
            if not model:
                continue
            ctx_pct = round(float(data.get("context_window", {}).get("used_percentage", 0)))
            rate = data.get("rate_limits", {})
            five = rate.get("five_hour", {})
            seven = rate.get("seven_day", {})
            cwd = data.get("workspace", {}).get("current_dir") or data.get("cwd", "")
            result[model.lower()] = {
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
    return result


def _manual_title_worker():
    """Background thread: re-apply pinned manual titles every 2s to fight Claude's OSC overwrites."""
    while True:
        time.sleep(2)
        with _manual_lock:
            items = list(_manual_titles.items())
        for tty, info in items:
            title = info.get("title", "")
            if not title:
                continue
            safe_title = title.replace("\\", "\\\\").replace('"', '\\"')
            win_id = info.get("winId", "")
            tab_id = info.get("tabId", "")
            try:
                if tab_id and win_id:
                    script = (
                        'tell application "Terminal"\n'
                        f'    set custom title of tab {tab_id} of window id {win_id} to "{safe_title}"\n'
                        'end tell'
                    )
                elif win_id:
                    script = (
                        'tell application "Terminal"\n'
                        f'    set custom title of tab 1 of window id {win_id} to "{safe_title}"\n'
                        'end tell'
                    )
                else:
                    with _manual_lock:
                        _manual_titles.pop(tty, None)
                    continue
                subprocess.run(["osascript", "-e", script], capture_output=True, timeout=3)
            except Exception:
                with _manual_lock:
                    _manual_titles.pop(tty, None)


def get_claude_info():
    """Return Claude info from statusline cache (accurate per-session data)."""
    info = {"sessions": [], "today_tokens": 0}

    # Read statusline cache files written by ~/.claude/statusline.sh
    cache_dir = Path(os.path.expanduser("~/.claude/statusline-cache"))
    seen = {}
    if cache_dir.exists():
        for f in cache_dir.glob("*.json"):
            try:
                data = json.loads(f.read_text())
                model = data.get("model", {}).get("display_name") or data.get("model", {}).get("id", "unknown")
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

    # Today's usage from stats-cache
    try:
        stats = json.loads(Path(os.path.expanduser("~/.claude/stats-cache.json")).read_text())
        daily = stats.get("dailyModelTokens", [])
        if daily:
            latest = daily[-1]
            info["today_tokens"] = sum(latest.get("tokensByModel", {}).values())
    except Exception:
        pass

    return info


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            html = (HERE / "index.html").read_text(encoding="utf-8")
            self.wfile.write(html.encode())

        elif path == "/api/tabs":
            data = get_terminals()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())

        elif path == "/api/claude":
            data = get_claude_info()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404")

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode() if length else "{}"
        data = json.loads(body) if body else {}

        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == "/api/focus":
            win_id = data.get("winId")
            if win_id:
                script = (
                    'tell application "Terminal"\n'
                    f'    set frontmost of window id {win_id} to true\n'
                    '    activate\n'
                    'end tell'
                )
                subprocess.Popen(["osascript", "-e", script])
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True}).encode())
        elif parsed.path == "/api/rename":
            win_id = data.get("winId")
            tab_id = data.get("tabId")
            title = data.get("title", "")
            tty = data.get("tty", "")
            if win_id and title:
                safe_title = title.replace("\\", "\\\\").replace('"', '\\"')
                if tab_id:
                    script = (
                        f'tell application "Terminal"\n'
                        f'    set custom title of tab {tab_id} of window id {win_id} to "{safe_title}"\n'
                        f'end tell'
                    )
                else:
                    script = (
                        f'tell application "Terminal"\n'
                        f'    set custom title of tab 1 of window id {win_id} to "{safe_title}"\n'
                        f'end tell'
                    )
                threading.Thread(target=lambda: subprocess.run(["osascript", "-e", script], timeout=5), daemon=True).start()
                # Auto-pin when user renames
                if tty:
                    with _manual_lock:
                        _manual_titles[tty] = {
                            "title": title,
                            "winId": win_id,
                            "tabId": tab_id or "",
                        }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True}).encode())
        elif parsed.path == "/api/title-mode":
            tty = data.get("tty")
            mode = data.get("mode")
            if tty and mode:
                with _manual_lock:
                    if mode == "manual":
                        _manual_titles[tty] = {
                            "title": data.get("title", ""),
                            "winId": data.get("winId", ""),
                            "tabId": data.get("tabId", ""),
                        }
                    else:
                        _manual_titles.pop(tty, None)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True}).encode())
        elif parsed.path == "/api/spawn":
            cwd = data.get("cwd", "").strip() or os.path.expanduser("~")
            cmd = data.get("cmd", "").strip()
            if cmd:
                cwd_expanded = os.path.expanduser(cwd)
                safe_cwd = cwd_expanded.replace("\\", "\\\\").replace('"', '\\"')
                safe_cmd = cmd.replace("\\", "\\\\").replace('"', '\\"')
                full = f'cd "{safe_cwd}" && {safe_cmd}'
                full_escaped = full.replace("\\", "\\\\").replace('"', '\\"')
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
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True}).encode())
            return
        elif parsed.path == "/api/reorder":
            tty_order = data.get("ttyOrder")
            if tty_order:
                global _global_order
                _global_order = list(tty_order)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True}).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404")

    def log_message(self, fmt, *args):
        print(f"[tabopener] {args[0]}")


if __name__ == "__main__":
    threading.Thread(target=_manual_title_worker, daemon=True).start()
    server = http.server.HTTPServer((HOST, PORT), Handler)
    print(f"Tab Opener: http://{HOST}:{PORT}")
    server.serve_forever()
