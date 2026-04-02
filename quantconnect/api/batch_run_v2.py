import os
import time
import json
import sys
from run_qc_backtest import trigger_backtest, PROJECT_ID
from poll_backtest import get_backtest_status

ARCHIVE_DIR = "../archive"
RESULTS_FILE = "batch_results.json"

def main():
    strategies = [
        "rotation_v1.py", "large_cap_ema.py", "large_cap_breakout.py", 
        "z_gold_oil_breakout.py", "z_sector_rotation_hedge.py",
        "a_2.py", "a_3.py", "a_4.py", "a_5.py", "a_6.py", 
        "a_7.py", "a_8.py", "a_9.py", "a_10.py", "a_11.py"
    ]
    # Add scratchpads later if needed
    
    results = {}
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'r') as f:
            results = json.load(f)

    for strategy in strategies:
        if strategy in results and results[strategy].get("status") == "Completed.":
            print(f"Skipping {strategy}, already completed.")
            continue
            
        print(f"\n--- Processing {strategy} ---")
        strategy_path = os.path.join(ARCHIVE_DIR, strategy)
        
        try:
            backtest_id = trigger_backtest(PROJECT_ID, strategy_path, name=f"BatchV2: {strategy}")
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
                
                # Check for "Completed." (with a dot)
                if status == "Completed.":
                    # For V2 API, statistics might be nested in the last rolling window or summary
                    # Let's try to find them in the 'statistics' field if it exists, or look deeper
                    stats = bt.get("statistics", {})
                    if not stats:
                        # Fallback: look at the last rolling window's portfolioStatistics
                        rw = bt.get("rollingWindow", {})
                        if rw:
                            last_key = sorted(rw.keys())[-1]
                            stats = rw[last_key].get("portfolioStatistics", {})

                    results[strategy] = {
                        "backtestId": backtest_id,
                        "status": status,
                        "CAGR": stats.get("compoundingAnnualReturn") or stats.get("Compounding Annual Return"),
                        "MaxDD": stats.get("drawdown") or stats.get("Drawdown"),
                        "Sharpe": stats.get("sharpeRatio") or stats.get("Sharpe Ratio")
                    }
                    print(f"\n{strategy} Completed: CAGR {results[strategy]['CAGR']}, DD {results[strategy]['MaxDD']}")
                    break
                elif status in ["Failure", "RuntimeError", "Runtime Error", "Cancelled"]:
                    results[strategy] = {
                        "backtestId": backtest_id,
                        "status": status,
                        "error": bt.get("error", "Unknown error")
                    }
                    print(f"\n{strategy} failed with status: {status}")
                    break
                
                time.sleep(30)
                
            with open(RESULTS_FILE, 'w') as f:
                json.dump(results, f, indent=4)
                
        except Exception as e:
            print(f"Error processing {strategy}: {e}")

if __name__ == "__main__":
    main()
