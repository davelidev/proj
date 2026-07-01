import subprocess
import sys
import os
import re
import time

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
    """No bundling needed: base.py is a separate project file and the sub file
    already imports from it. Upload the sub directly as main.py."""
    return os.path.abspath(sub_path)


def bundle_ensemble():
    """Bundle the full ensemble -> merged/ensemble.py."""
    subprocess.run(["python3", BUNDLE_SCRIPT], check=True)
    return os.path.join(MERGED_DIR, "ensemble.py")


def run_one(target_file, test_name):
    """Upload target_file as main.py, run, poll to completion, print yearly stats."""
    print(f"\nTriggering Backtest ({test_name})...")
    res = subprocess.run(["python3", RUN_SCRIPT, target_file, test_name],
                         stdout=subprocess.PIPE, stderr=sys.stderr, text=True)
    match = re.search(r"BACKTEST_ID=([\w\d]+)", res.stdout)
    if not match:
        print(f"Error: Could not find Backtest ID in output:\n{res.stdout}")
        return None
    bid = match.group(1)
    print(f"Captured Backtest ID: {bid}")

    subprocess.run(["python3", POLL_SCRIPT, bid], check=True)
    subprocess.run(["python3", STATS_SCRIPT, bid], check=True)
    return bid


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
        for name, bid in results.items():
            print(f"  {name:<12} {bid or 'FAILED'}")


if __name__ == "__main__":
    main()
