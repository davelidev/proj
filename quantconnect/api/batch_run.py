import os
import time
import json
import sys
from run_qc_backtest import trigger_backtest, PROJECT_ID
from poll_backtest import get_backtest_status

ARCHIVE_DIR = "archive"
RESULTS_FILE = "batch_results.json"

def main():
    # Get all .py files in archive
    strategies = [f for f in os.listdir(ARCHIVE_DIR) if f.endswith(".py")]
    strategies.sort()
    
    results = {}
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'r') as f:
            results = json.load(f)

    for strategy in strategies:
        if strategy in results and results[strategy].get("status") == "Completed":
            print(f"Skipping {strategy}, already completed.")
            continue
            
        print(f"\n--- Processing {strategy} ---")
        strategy_path = os.path.join(ARCHIVE_DIR, strategy)
        
        try:
            backtest_id = trigger_backtest(PROJECT_ID, strategy_path, name=f"Batch: {strategy}")
            if not backtest_id:
                print(f"Failed to trigger {strategy}")
                continue
            
            print(f"Backtest {backtest_id} started. Polling...")
            
            while True:
                res = get_backtest_status(PROJECT_ID, backtest_id)
                if not res or not res.get("success"):
                    print(f"Failed to get status for {backtest_id}")
                    break
                
                bt = res.get("backtest", {})
                status = bt.get("status")
                progress = bt.get("progress", 0)
                print(f"Status: {status}, Progress: {float(progress)*100:.2f}%", end="\r")
                
                if status == "Completed":
                    stats = bt.get("statistics", {})
                    results[strategy] = {
                        "backtestId": backtest_id,
                        "status": status,
                        "CAGR": stats.get("Compounding Annual Return"),
                        "MaxDD": stats.get("Drawdown"),
                        "Sharpe": stats.get("Sharpe Ratio")
                    }
                    print(f"\n{strategy} Completed: CAGR {results[strategy]['CAGR']}, DD {results[strategy]['MaxDD']}")
                    break
                elif status in ["Failure", "RuntimeError", "Cancelled"]:
                    results[strategy] = {
                        "backtestId": backtest_id,
                        "status": status,
                        "error": bt.get("error", "Unknown error")
                    }
                    print(f"\n{strategy} failed with status: {status}")
                    break
                
                time.sleep(20) # Poll every 20 seconds
                
            # Save results after each completion
            with open(RESULTS_FILE, 'w') as f:
                json.dump(results, f, indent=4)
                
        except Exception as e:
            print(f"Error processing {strategy}: {e}")

if __name__ == "__main__":
    main()
