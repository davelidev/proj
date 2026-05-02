import subprocess
import sys
import os
import re

# ---------------------------------------------------------------------------
# Path Configurations (Absolute)
# ---------------------------------------------------------------------------
PROJECT_ROOT = "/Users/daveli/Desktop/proj/QuantConnect"
BUNDLE_SCRIPT = os.path.join(PROJECT_ROOT, "strategies/bundle.py")
RUN_SCRIPT = os.path.join(PROJECT_ROOT, "api/run_qc_backtest.py")
POLL_SCRIPT = os.path.join(PROJECT_ROOT, "api/poll_backtest.py")
STATS_SCRIPT = os.path.join(PROJECT_ROOT, "api/get_yearly_stats.py")
TARGET_FILE = os.path.join(PROJECT_ROOT, "strategies/embedded/ensemble.py")

def main():
    os.chdir(PROJECT_ROOT)

    # 1. Bundle
    print("Step 1: Bundling Ensemble...")
    subprocess.run(["python3", BUNDLE_SCRIPT], check=True)

    # 2. Run Backtest & Capture ID
    print("\nStep 2: Triggering Backtest...")
    # We capture stdout to get the ID, but keep informational messages on stderr visible
    res = subprocess.run(["python3", RUN_SCRIPT, TARGET_FILE, "UltimateAlgo Run"], 
                         capture_output=True, text=True)
    
    # Show informational output (stderr)
    print(res.stderr, file=sys.stderr)
    
    # Extract ID
    match = re.search(r"BACKTEST_ID=([\w\d]+)", res.stdout)
    if not match:
        print(f"Error: Could not find Backtest ID in output:\n{res.stdout}")
        sys.exit(1)
    
    bid = match.group(1)
    print(f"Captured Backtest ID: {bid}")

    # 3. Poll for Completion
    print("\nStep 3: Polling for Completion...")
    # Inherit stdout/stderr for real-time progress (\r)
    subprocess.run(["python3", POLL_SCRIPT, bid], check=True)

    # 4. Fetch Yearly Stats
    print("\nStep 4: Fetching Statistics...")
    subprocess.run(["python3", STATS_SCRIPT, bid], check=True)

if __name__ == "__main__":
    main()
