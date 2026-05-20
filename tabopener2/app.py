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
        try:
            length = int(self.headers.get("Content-Length", 0))
        except (ValueError, TypeError):
            length = 0
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
