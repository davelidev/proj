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
    if cmd:
        safe_cmd = cmd.replace("\\", "\\\\").replace('"', '\\"')
        full_escaped = f'cd "{safe_cwd}" && {safe_cmd}'.replace("\\", "\\\\").replace('"', '\\"')
    else:
        full_escaped = f'cd "{safe_cwd}"'.replace("\\", "\\\\").replace('"', '\\"')
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
