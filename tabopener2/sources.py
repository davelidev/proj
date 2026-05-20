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
                "rate_5h_pct": round(float(five["used_percentage"])) if "used_percentage" in five else None,
                "rate_5h_resets": five.get("resets_at"),
                "rate_7d_pct": round(float(seven["used_percentage"])) if "used_percentage" in seven else None,
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
