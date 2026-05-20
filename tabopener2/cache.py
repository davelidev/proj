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
