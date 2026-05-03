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

def main():
    # 1. Bundle
    if len(sys.argv) > 1:
        # Resolve path immediately before chdir
        standalone_path = os.path.abspath(sys.argv[1])
        os.chdir(PROJECT_ROOT)
        
        print(f"Step 1: Bundling Standalone ({standalone_path})...")
        subprocess.run(["python3", BUNDLE_SCRIPT, standalone_path], check=True)
        
        target_file = os.path.join(PROJECT_ROOT, "strategies/embedded/standalone.py")
        base_name = os.path.basename(standalone_path)
        test_name = f"Standalone Run: {base_name}"
    else:
        os.chdir(PROJECT_ROOT)
        print("Step 1: Bundling Ensemble...")
        subprocess.run(["python3", BUNDLE_SCRIPT], check=True)
        
        target_file = os.path.join(PROJECT_ROOT, "strategies/embedded/ensemble.py")
        test_name = "UltimateAlgo Run"

    # 2. Run Backtest & Capture ID
    print(f"\nStep 2: Triggering Backtest ({test_name})...")
    # We capture stdout to get the ID, but let stderr flow through for real-time progress
    res = subprocess.run(["python3", RUN_SCRIPT, target_file, test_name], 
                         stdout=subprocess.PIPE, stderr=sys.stderr, text=True)

    # Extract ID from captured stdout
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
