import subprocess
import sys
import os
import re
import time
import hashlib
import base64
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
_USER_ID   = os.environ.get("QC_USER_ID")
_API_TOKEN = os.environ.get("QC_API_TOKEN")
_PROJECT   = os.environ.get("QC_PROJECT_ID")
_BASE_URL  = os.environ.get("QC_BASE_URL", "https://www.quantconnect.com/api/v2")

def _auth():
    ts = str(int(time.time()))
    h  = hashlib.sha256(f"{_API_TOKEN}:{ts}".encode()).hexdigest()
    return {"Authorization": f"Basic {base64.b64encode(f'{_USER_ID}:{h}'.encode()).decode()}",
            "Timestamp": ts}

def _fetch_cagr_maxdd(bid):
    r = requests.get(f"{_BASE_URL}/backtests/read", headers=_auth(),
                     params={"projectId": _PROJECT, "backtestId": bid})
    stats = r.json().get("backtest", {}).get("statistics", {})
    cagr  = stats.get("Compounding Annual Return", "")
    maxdd = stats.get("Drawdown", "")
    if cagr:
        cagr = f"{round(float(cagr.strip('%')))  }%"
    if maxdd:
        maxdd = f"-{round(float(maxdd.strip('%')))}%"
    return cagr or None, maxdd or None

# ---------------------------------------------------------------------------
# Path Configurations (Absolute)
# ---------------------------------------------------------------------------
PROJECT_ROOT = "/Users/daveli/Desktop/proj/QuantConnect"
ENSEMBLE_DIR = os.path.join(PROJECT_ROOT, "cc/cc_algos/ensemble")
BUNDLE_SCRIPT = os.path.join(ENSEMBLE_DIR, "utils/bundle.py")
RUN_SCRIPT = os.path.join(PROJECT_ROOT, "api/run_qc_backtest.py")
POLL_SCRIPT = os.path.join(PROJECT_ROOT, "api/poll_backtest.py")
STATS_SCRIPT = os.path.join(PROJECT_ROOT, "api/get_yearly_stats.py")
MERGED_DIR = os.path.join(ENSEMBLE_DIR, "merged")


def standalone_target(sub_path):
    """Return absolute path; run_qc_backtest.py inlines base.py if needed."""
    return os.path.abspath(sub_path)


def bundle_ensemble():
    """Bundle the full ensemble -> merged/ensemble.py."""
    subprocess.run(["python3", BUNDLE_SCRIPT], check=True)
    return os.path.join(MERGED_DIR, "ensemble.py")


def run_one(target_file, test_name):
    """Upload target_file as main.py, run, poll to completion, print yearly stats.
    Returns (bid, cagr_str, maxdd_str) or (None, None, None) on failure."""
    print(f"\nTriggering Backtest ({test_name})...")
    res = subprocess.run(["python3", RUN_SCRIPT, target_file, test_name],
                         stdout=subprocess.PIPE, stderr=sys.stderr, text=True)
    match = re.search(r"BACKTEST_ID=([\w\d]+)", res.stdout)
    if not match:
        print(f"Error: Could not find Backtest ID in output:\n{res.stdout}")
        return None, None, None
    bid = match.group(1)
    print(f"Captured Backtest ID: {bid}")

    # Let poll write directly to terminal so \r status updates work
    subprocess.run(["python3", POLL_SCRIPT, bid], check=False)
    subprocess.run(["python3", STATS_SCRIPT, bid], check=False)

    cagr, maxdd = _fetch_cagr_maxdd(bid)
    return bid, cagr, maxdd


def discover_subs():
    """All NNN.py sub-algo files in the ensemble directory, sorted."""
    return [os.path.join(ENSEMBLE_DIR, f)
            for f in sorted(os.listdir(ENSEMBLE_DIR))
            if re.fullmatch(r"\d{3}\.py", f)]


def main():
    os.chdir(PROJECT_ROOT)
    args = sys.argv[1:]

    # No file args -> full ensemble.
    if not args:
        print("Bundling Ensemble...")
        target = bundle_ensemble()
        run_one(target, "UltimateAlgo Run")
        return

    # `ult all` -> every NNN.py sub as its own standalone backtest.
    if len(args) == 1 and args[0] == "all":
        subs = discover_subs()
    else:
        subs = [os.path.abspath(a) for a in args]

    results = {}
    for i, sub in enumerate(subs, 1):
        name = os.path.basename(sub)
        print(f"\n{'#' * 60}\n# [{i}/{len(subs)}] Standalone: {name}\n{'#' * 60}")
        if i > 1:
            time.sleep(5)  # space out backtest creation to avoid QC throttling
        results[name] = run_one(standalone_target(sub), f"Standalone Run: {name}")

    if len(subs) > 1:
        print(f"\n{'=' * 40}\n## Batch Summary\n{'=' * 40}")
        for name, (bid, cagr, maxdd) in results.items():
            if bid is None:
                print(f"  {name:<12} FAILED")
            else:
                stats = f"{cagr or '?':>6}  {maxdd or '?':>6}"
                print(f"  {name:<12} {stats}  {bid}")


if __name__ == "__main__":
    main()
