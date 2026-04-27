import os
import time
import json
from run_qc_backtest import trigger_backtest, PROJECT_ID
from poll_backtest import get_backtest_status

STRATEGIES_TO_RUN = [
    "vol_breakout.py",
    # "dip_buy_tech.py", # Already have stats
    "leveraged_rebalance.py",
    "conservative_rotation.py",
    "defensive_rotation.py",
    "rsi_champion.py",
    "dip_buy_tqqq.py",
    "holy_grail_refined.py"
]

STRATEGY_DIR = "strategies"
RESULTS_FILE = "api/main_strategies_stats.json"

def main():
    results = {}
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'r') as f:
            results = json.load(f)

    # Add dip_buy_tech.py if not present (from previous run)
    if "dip_buy_tech.py" not in results:
        results["dip_buy_tech.py"] = {
            "backtestId": "e3f393e426a43cbb59d83409066569c3",
            "Win Rate": "52%",
            "Loss Rate": "48%",
            "Total Orders": "71",
            "Profit-Loss Ratio": "3.43",
            "Net Profit": "2543.721%",
            "CAGR": "31.352%",
            "MaxDD": "49.100%",
            "Sharpe": "0.883"
        }

    for strat_file in STRATEGIES_TO_RUN:
        if strat_file in results and results[strat_file].get("status") == "Completed":
            print(f"Skipping {strat_file}, already completed.")
            continue
            
        print(f"\n--- Processing {strat_file} ---")
        strat_path = os.path.join(STRATEGY_DIR, strat_file)
        
        try:
            backtest_id = trigger_backtest(PROJECT_ID, strat_path, name=f"Stats: {strat_file}")
            if not backtest_id:
                print(f"Failed to trigger {strat_file}")
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
                
                if status in ["Completed", "Completed."]:
                    stats = bt.get("statistics", {})
                    if not stats:
                        rw = bt.get("rollingWindow", {})
                        if rw:
                            last_key = sorted(rw.keys())[-1]
                            stats = rw[last_key].get("portfolioStatistics", {})

                    results[strat_file] = {
                        "backtestId": backtest_id,
                        "status": "Completed",
                        "CAGR": stats.get("Compounding Annual Return") or stats.get("compoundingAnnualReturn"),
                        "MaxDD": stats.get("Drawdown") or stats.get("drawdown"),
                        "Sharpe": stats.get("Sharpe Ratio") or stats.get("sharpeRatio"),
                        "Win Rate": stats.get("Win Rate"),
                        "Loss Rate": stats.get("Loss Rate"),
                        "Total Orders": stats.get("Total Orders"),
                        "Profit-Loss Ratio": stats.get("Profit-Loss Ratio"),
                        "Net Profit": stats.get("Net Profit")
                    }
                    print(f"\n{strat_file} Completed.")
                    break
                elif status in ["Failure", "RuntimeError", "Runtime Error", "Cancelled"]:
                    print(f"\n{strat_file} failed with status: {status}")
                    break
                
                time.sleep(20)
                
            with open(RESULTS_FILE, 'w') as f:
                json.dump(results, f, indent=4)
                
        except Exception as e:
            print(f"Error processing {strat_file}: {e}")

if __name__ == "__main__":
    main()
