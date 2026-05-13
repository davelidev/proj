import os
import time
import json
import requests
import hashlib
import base64
from dotenv import load_dotenv

load_dotenv()

USER_ID = os.environ.get("QC_USER_ID")
API_TOKEN = os.environ.get("QC_API_TOKEN")
PROJECT_ID = os.environ.get("QC_PROJECT_ID")
BASE_URL = os.environ.get("QC_BASE_URL")

RESEARCH_DIR = os.path.join(os.path.dirname(__file__), "..", "research")
STRATEGIES_DIR = os.path.join(os.path.dirname(__file__), "..", "strategies")
RESULTS_FILE = os.path.join(os.path.dirname(__file__), "research_stats.json")

# Archive entries 21-32 mapped to (file, label, dir, param_overrides)
TARGETS = [
    ("strategy_38.py",              "A21 - S38",       RESEARCH_DIR,   None),
    ("strategy_template.py",        "A22 - Iter69",    RESEARCH_DIR,   {"rsi_trigger": 25.52, "rsi_exit": 70.64, "vix_limit": 32.95, "vix_ratio_limit": 1.073, "use_soxl": "false", "atr_stop_mult": 2.63}),
    ("strategy_template.py",        "A23 - Iter60",    RESEARCH_DIR,   {"rsi_trigger": 24.55, "rsi_exit": 87.57, "vix_limit": 25.51, "vix_ratio_limit": 1.018, "use_soxl": "false", "atr_stop_mult": 2.58}),
    ("strategy_36.py",              "A24 - S36",       RESEARCH_DIR,   None),
    ("strategy_35.py",              "A25 - S35",       RESEARCH_DIR,   None),
    ("strategy_template.py",        "A26 - Iter192",   RESEARCH_DIR,   {"rsi_trigger": 21.09, "rsi_exit": 89.35, "vix_limit": 33.68, "vix_ratio_limit": 0.988, "use_soxl": "false", "atr_stop_mult": 2.69}),
    ("strategy_34.py",              "A27 - S34",       RESEARCH_DIR,   None),
    ("strategy_22.py",              "A28 - S22",       RESEARCH_DIR,   None),
    ("strategy_31.py",              "A29 - S31",       RESEARCH_DIR,   None),
    ("strategy_16.py",              "A30 - S16",       RESEARCH_DIR,   None),
    ("cheat_code_rotator_tqqq.py",  "A32 - S11",       RESEARCH_DIR,   None),
]

def get_auth_headers():
    timestamp = str(int(time.time()))
    token_hash = hashlib.sha256(f"{API_TOKEN}:{timestamp}".encode()).hexdigest()
    auth_64 = base64.b64encode(f"{USER_ID}:{token_hash}".encode()).decode()
    return {"Authorization": f"Basic {auth_64}", "Timestamp": timestamp}

def inject_params(content, params):
    """Replace GetParameter defaults with fixed values for a specific iteration."""
    import re
    for key, val in params.items():
        if key == "use_soxl":
            pattern = rf'(GetParameter\("{key}",\s*")[^"]*(")'
            content = re.sub(pattern, rf'\g<1>{val}\g<2>', content)
        else:
            pattern = rf'(GetParameter\("{key}",\s*)[^\)]+(\))'
            content = re.sub(pattern, rf'\g<1>{val}\g<2>', content)
    return content

def run_backtest(label, content):
    resp = requests.post(f"{BASE_URL}/files/update", headers=get_auth_headers(),
                         json={"projectId": PROJECT_ID, "name": "main.py", "content": content})
    if not resp.json().get("success"):
        print(f"  Failed to upload {label}")
        return None

    time.sleep(2)
    resp = requests.post(f"{BASE_URL}/compile/create", headers=get_auth_headers(),
                         json={"projectId": PROJECT_ID})
    cr = resp.json()
    if not cr.get("success"):
        print(f"  Compile failed: {cr.get('errors')}")
        return None

    time.sleep(2)
    resp = requests.post(f"{BASE_URL}/backtests/create", headers=get_auth_headers(),
                         json={"projectId": PROJECT_ID, "compileId": cr["compileId"], "backtestName": label})
    br = resp.json()
    if not br.get("success"):
        print(f"  Backtest trigger failed: {br.get('errors')}")
        return None
    return br["backtest"]["backtestId"]

def poll(bid):
    while True:
        resp = requests.get(f"{BASE_URL}/backtests/read", headers=get_auth_headers(),
                            params={"projectId": PROJECT_ID, "backtestId": bid})
        bt = resp.json().get("backtest", {})
        status = bt.get("status", "")
        progress = float(bt.get("progress", 0)) * 100
        print(f"  {status} {progress:.0f}%", end="\r")
        if status in ["Completed", "Completed."]:
            return bt.get("statistics", {})
        if status in ["Failure", "RuntimeError", "Runtime Error", "Cancelled"]:
            print(f"\n  Failed: {bt.get('error','')}")
            return None
        time.sleep(10)

def parse_stats(stats):
    def pct(v):
        if v is None: return None
        return float(str(v).replace("%", "").strip())
    win_rate = pct(stats.get("Win Rate"))
    loss_rate = pct(stats.get("Loss Rate"))
    total = stats.get("Total Orders")
    pl_ratio = stats.get("Profit-Loss Ratio")
    if total is None or win_rate is None:
        return None
    total = int(str(total).replace(",", ""))
    win_n = round(total * win_rate / 100)
    loss_n = total - win_n
    wl = round(win_n / loss_n, 2) if loss_n else None
    return {
        "Win #": win_n,
        "Loss #": loss_n,
        "W/L Ratio": wl,
        "Profit Ratio": float(str(pl_ratio).replace("%", "")) if pl_ratio else None,
        "Win Rate": win_rate,
        "Total Orders": total,
    }

def main():
    results = {}
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE) as f:
            results = json.load(f)

    for filename, label, directory, params in TARGETS:
        if label in results:
            print(f"Skipping {label} (cached)")
            continue

        print(f"\n--- {label} ({filename}) ---")
        filepath = os.path.join(directory, filename)
        with open(filepath) as f:
            content = f.read()

        if params:
            content = inject_params(content, params)

        bid = run_backtest(label, content)
        if not bid:
            continue

        print(f"  Backtest ID: {bid}")
        stats = poll(bid)
        if not stats:
            continue

        parsed = parse_stats(stats)
        if parsed:
            results[label] = parsed
            print(f"\n  Win #: {parsed['Win #']}  Loss #: {parsed['Loss #']}  W/L: {parsed['W/L Ratio']}  Profit Ratio: {parsed['Profit Ratio']}")
        else:
            print(f"\n  Could not parse stats: {stats}")

        with open(RESULTS_FILE, "w") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

    print("\n\nFinal Results:")
    print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
