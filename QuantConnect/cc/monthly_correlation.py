"""
Monthly-return correlation of each ensemble sub-algo vs the full ensemble.

For each of the 17 sub-algos, runs a standalone backtest, fetches M1 monthly
equity data (144 data points, 2014-2025), computes Pearson r against the full
ensemble's monthly return series, and writes a ranked table to
cc/md/ensemble_monthly_correlation.md.

Usage:
    python3 cc/monthly_correlation.py              # run all standalones + compute
    python3 cc/monthly_correlation.py --table-only # regenerate MD from stored results
"""

import os, sys, re, json, time, subprocess
import hashlib, base64, requests, math
from dotenv import load_dotenv

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(ROOT, "api/.env"))
USER_ID    = os.environ.get("QC_USER_ID")
API_TOKEN  = os.environ.get("QC_API_TOKEN")
PROJECT_ID = os.environ.get("QC_PROJECT_ID")
BASE_URL   = os.environ.get("QC_BASE_URL", "https://www.quantconnect.com/api/v2")

BUNDLE_PY    = os.path.join(ROOT, "cc/cc_algos/ensemble/utils/bundle.py")
STANDALONE   = os.path.join(ROOT, "cc/cc_algos/ensemble/merged/standalone.py")
RUN_SCRIPT   = os.path.join(ROOT, "api/run_qc_backtest.py")
POLL_SCRIPT  = os.path.join(ROOT, "api/poll_backtest.py")
RESULTS_PATH = os.path.join(ROOT, "cc/monthly_corr_results.json")
MD_OUT       = os.path.join(ROOT, "cc/md/ensemble_monthly_correlation.md")

# Full ensemble backtest ID (from backtest_cc000.jsonl)
ENSEMBLE_BT_ID = "16800d6b5e7cd83718b947f63b6d5e97"

# 17 active sub-algos: (file, short_id, display_name)
SUB_ALGOS = [
    ("001.py", "S01", "TQQQ 60% Annual Rebalance"),
    ("002.py", "S02", "QQQ RSI(2) Dip"),
    ("003.py", "S03", "TQQQ Dynamic Sizing"),
    ("004.py", "S04", "TQQQ Expanding Range Breakout"),
    ("005.py", "S05", "QQQ SMA(150) Trend → TQQQ"),
    ("006.py", "S06", "TQQQ IBS Extreme + ATR Stop"),
    ("008.py", "S08", "ROC(20) Zero Cross"),
    ("009.py", "S09", "Up-Day Count(20)"),
    ("010.py", "S10", "TII(20) Trend Intensity"),
    ("011.py", "S11", "Price 126D Percentile"),
    ("012.py", "S12", "Trend Stretch Exit"),
    ("013.py", "S13", "TQQQ Anti-Martingale Pyramid"),
    ("014.py", "S14", "Donchian-200 Midline"),
    ("015.py", "S15", "ROC+D200 + 7% Trail Exit"),
    ("016.py", "S16", "TQQQ Pyramid (10%/day)"),
    ("017.py", "S17", "Range Expanded 110%"),
    ("018.py", "S18", "MFI14_Hyst"),
]

# ---------------------------------------------------------------------------
# QC API helpers
# ---------------------------------------------------------------------------

def auth():
    ts = str(int(time.time()))
    h  = hashlib.sha256(f"{API_TOKEN}:{ts}".encode()).hexdigest()
    b  = base64.b64encode(f"{USER_ID}:{h}".encode()).decode()
    return {"Authorization": f"Basic {b}", "Timestamp": ts}


def cancel_stale():
    try:
        r = requests.get(f"{BASE_URL}/backtests/list", headers=auth(),
                         params={"projectId": PROJECT_ID}, timeout=30)
        for bt in r.json().get("backtests", []):
            st = bt.get("status", "")
            if "Progress" in st or "Queue" in st:
                requests.post(f"{BASE_URL}/backtests/update", headers=auth(),
                              json={"projectId": PROJECT_ID, "backtestId": bt["backtestId"],
                                    "name": bt["name"], "status": "Cancel"}, timeout=30)
    except Exception:
        pass


def run_backtest(algo_file, name):
    """Bundle algo_file as standalone, upload, compile, create backtest. Returns backtest_id."""
    algo_path = os.path.join(ROOT, "cc/cc_algos/ensemble", algo_file)

    # Bundle
    subprocess.run(["python3", BUNDLE_PY, algo_path], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    with open(STANDALONE) as f:
        content = f.read()

    # Upload
    r = requests.post(f"{BASE_URL}/files/update", headers=auth(),
                      json={"projectId": PROJECT_ID, "name": "main.py", "content": content})
    if not r.json().get("success"):
        raise RuntimeError(f"Upload failed: {r.json()}")

    # Compile
    r = requests.post(f"{BASE_URL}/compile/create", headers=auth(),
                      json={"projectId": PROJECT_ID})
    compile_id = r.json()["compileId"]
    for _ in range(120):
        r = requests.get(f"{BASE_URL}/compile/read", headers=auth(),
                         params={"projectId": PROJECT_ID, "compileId": compile_id})
        status = r.json().get("state") or r.json().get("status", "")
        if status == "BuildSuccess":
            break
        if status == "BuildError":
            raise RuntimeError(f"Compile error for {algo_file}")
        time.sleep(2)

    # Create backtest
    r = requests.post(f"{BASE_URL}/backtests/create", headers=auth(),
                      json={"projectId": PROJECT_ID, "compileId": compile_id, "backtestName": name})
    if not r.json().get("success"):
        raise RuntimeError(f"Backtest create failed: {r.json()}")
    return r.json()["backtest"]["backtestId"]


def poll_backtest(bid, label=""):
    """Poll until backtest completes. Returns final stats dict."""
    for i in range(600):
        r = requests.get(f"{BASE_URL}/backtests/read", headers=auth(),
                         params={"projectId": PROJECT_ID, "backtestId": bid})
        bt = r.json().get("backtest", {})
        progress = bt.get("progress", 0) * 100
        status   = bt.get("status", "")
        cash     = bt.get("statistics", {}).get("Total Net Profit", "")
        print(f"  {label}: {progress:.1f}%", end="\r", flush=True)
        if progress >= 100 and status not in ("", "Running"):
            print()
            return r.json()
        if "Error" in status or "Cancelled" in status:
            raise RuntimeError(f"Backtest {bid} failed: {status}")
        time.sleep(3)
    raise RuntimeError(f"Backtest {bid} timed out")


def fetch_monthly_returns(bid):
    """Returns list of (yyyymm_str, pct_return) sorted by date, using M1_ rolling window."""
    r = requests.get(f"{BASE_URL}/backtests/read", headers=auth(),
                     params={"projectId": PROJECT_ID, "backtestId": bid})
    rw = r.json().get("backtest", {}).get("rollingWindow", {})

    # Collect M1_ keys → monthly equity snapshots
    entries = []
    for key, val in rw.items():
        if not key.startswith("M1_"):
            continue
        # Key format: M1_YYYYMMDD
        date_str = key[3:]  # YYYYMMDD
        end_eq   = float(val.get("portfolioStatistics", {}).get("endEquity", 0))
        start_eq = float(val.get("portfolioStatistics", {}).get("startEquity", 0))
        entries.append((date_str, start_eq, end_eq))

    entries.sort(key=lambda x: x[0])
    if not entries:
        return []

    # month-over-month return using endEquity chain
    monthly = []
    prev_end = entries[0][1]  # first startEquity as the baseline
    for date_str, start_eq, end_eq in entries:
        if prev_end > 0:
            ret = (end_eq / prev_end) - 1.0
        else:
            ret = 0.0
        monthly.append((date_str[:6], ret))  # YYYYMM
        prev_end = end_eq

    return monthly


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------

def pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return float("nan")
    mx = sum(xs) / n
    my = sum(ys) / n
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sx  = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy  = math.sqrt(sum((y - my) ** 2 for y in ys))
    if sx == 0 or sy == 0:
        return float("nan")
    return cov / (sx * sy)


def align_series(a_series, b_series):
    """Return two aligned lists of floats using only months present in both."""
    a_map = dict(a_series)
    b_map = dict(b_series)
    common = sorted(set(a_map) & set(b_map))
    return [a_map[m] for m in common], [b_map[m] for m in common], len(common)


# ---------------------------------------------------------------------------
# Markdown generation
# ---------------------------------------------------------------------------

def generate_md(results, ensemble_monthly):
    lines = [
        "# Ensemble Monthly Correlation",
        "",
        "*Pearson r on monthly returns (M1 rolling window, 2014–2025, up to 144 data points).*",
        "",
        "## Correlation with Full Ensemble",
        "",
        "| r | n | ID | Name |",
        "| ---: | ---: | :-- | :-- |",
    ]
    rows = sorted(
        [(v["r"], v["n"], sid, v["name"]) for sid, v in results.items() if "r" in v],
        reverse=True
    )
    for r_val, n, sid, name in rows:
        lines.append(f"| {r_val:.3f} | {n} | {sid} | {name} |")

    lines += [
        "",
        "## Notes",
        "",
        "- Monthly returns computed as month-over-month equity change from QC M1 rolling window.",
        "- `n` = number of overlapping months used for the correlation.",
        "- Ensemble backtest: full 17-algo portfolio.",
        "- Each sub-algo run standalone (equal allocation, same date range).",
    ]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def load_results():
    if os.path.exists(RESULTS_PATH):
        return json.load(open(RESULTS_PATH))
    return {}


def save_results(results):
    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


def main():
    table_only = "--table-only" in sys.argv
    results = load_results()

    # ------------------------------------------------------------------
    # Phase 1: ensure every sub-algo has a backtest ID
    # ------------------------------------------------------------------
    if not table_only:
        for algo_file, sid, name in SUB_ALGOS:
            entry = results.get(sid, {})
            if entry.get("backtestId") and entry.get("status") == "completed":
                print(f"[skip] {sid} {name}: already have backtest {entry['backtestId'][:12]}...")
                continue

            cancel_stale()
            time.sleep(3)

            bt_name = f"MonthCorr: {algo_file}"
            print(f"\n{'='*60}")
            print(f"Running: {sid} {name}")
            print(f"{'='*60}")
            try:
                bid = run_backtest(algo_file, bt_name)
                print(f"  Backtest ID: {bid}")
                data = poll_backtest(bid, label=sid)
                stats = data.get("backtest", {}).get("statistics", {})
                results[sid] = {
                    "name":       name,
                    "file":       algo_file,
                    "backtestId": bid,
                    "status":     "completed",
                }
                save_results(results)
                print(f"  Saved {sid}")
            except Exception as e:
                print(f"  ERROR: {e}")
                results[sid] = results.get(sid, {"name": name, "file": algo_file})
                results[sid]["status"] = "error"
                results[sid]["error"]  = str(e)
                save_results(results)
                continue

            time.sleep(5)

    # ------------------------------------------------------------------
    # Phase 2: fetch monthly returns for ensemble + all sub-algos
    # ------------------------------------------------------------------
    print("\nFetching ensemble monthly returns...")
    ensemble_monthly = fetch_monthly_returns(ENSEMBLE_BT_ID)
    print(f"  Ensemble: {len(ensemble_monthly)} months")

    for algo_file, sid, name in SUB_ALGOS:
        entry = results.get(sid, {})
        bid   = entry.get("backtestId", "")
        if not bid:
            print(f"[skip] {sid}: no backtest ID")
            continue
        if "r" in entry and not table_only:
            pass  # will recompute anyway

        print(f"  Fetching {sid} ({bid[:12]}...)...")
        try:
            algo_monthly = fetch_monthly_returns(bid)
            xs, ys, n = align_series(ensemble_monthly, algo_monthly)
            r = pearson(xs, ys)
            results[sid]["r"] = round(r, 4)
            results[sid]["n"] = n
        except Exception as e:
            print(f"    ERROR fetching {sid}: {e}")
            results[sid]["r"] = None

    save_results(results)

    # ------------------------------------------------------------------
    # Phase 3: write markdown
    # ------------------------------------------------------------------
    md = generate_md(results, ensemble_monthly)
    os.makedirs(os.path.dirname(MD_OUT), exist_ok=True)
    with open(MD_OUT, "w") as f:
        f.write(md)

    print(f"\nTable written to {MD_OUT}")
    print()
    print(f"{'r':>7} | {'n':>4} | {'ID':<4} | Name")
    print("-" * 55)
    rows = sorted(
        [(v["r"], v.get("n", 0), sid, v["name"]) for sid, v in results.items()
         if v.get("r") is not None],
        reverse=True
    )
    for r_val, n, sid, name in rows:
        print(f"{r_val:>7.3f} | {n:>4} | {sid:<4} | {name}")


if __name__ == "__main__":
    main()
