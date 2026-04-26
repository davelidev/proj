import os
import sys
import time
import json

from run_qc_backtest import trigger_backtest, PROJECT_ID
from poll_backtest import get_backtest_status
from get_yearly_stats import extract_yearly_returns

strategies = [
    {
        "file": "strategy_36.py",
        "name": "TQQQ/TECL/SOXL Rotator",
        "desc": "Strategy 36: Expanding Strong Trend + TQQQ/SOXL/TECL Rotator\n*   **Logic:** Strategy 35 + Rotate to strongest momentum among TQQQ, SOXL, TECL."
    },
    {
        "file": "strategy_37.py",
        "name": "TQQQ/SOXL Expanding High Exit",
        "desc": "Strategy 37: Expanding Strong Trend + SOXL + High Exit\n*   **Logic:** Strategy 35 + Exit at 20-Day High instead of trailing stop."
    },
    {
        "file": "strategy_38.py",
        "name": "TQQQ/SOXL Expanding VIX 1.10",
        "desc": "Strategy 38: Expanding Strong Trend + SOXL + VIX 1.10\n*   **Logic:** Strategy 35 + Exit only on extreme VIX backwardation (>1.10)."
    }
]

log_file = "QuantConnect/research_log.md"

def main():
    with open(log_file, "a") as f:
        f.write("\n")
        
    for strat in strategies:
        print(f"\n--- Running {strat['name']} ---")
        bt_id = trigger_backtest(PROJECT_ID, f"QuantConnect/{strat['file']}", strat['name'])
        if not bt_id:
            print("Failed to trigger backtest.")
            continue
            
        print(f"Backtest ID: {bt_id}")
        
        cagr, draw, sharpe = None, None, None
        while True:
            res = get_backtest_status(PROJECT_ID, bt_id)
            if not res or not res.get("success"):
                break
            
            bt = res.get("backtest", {})
            status = bt.get("status")
            if status in ["Completed", "Completed."]:
                stats = bt.get("statistics", {})
                if not stats:
                    rw = bt.get("rollingWindow", {})
                    if rw:
                        last_key = sorted(rw.keys())[-1]
                        stats = rw[last_key].get("portfolioStatistics", {})
                cagr = stats.get('Compounding Annual Return') or stats.get('compoundingAnnualReturn')
                draw = stats.get('Drawdown') or stats.get('drawdown')
                sharpe = stats.get('Sharpe Ratio') or stats.get('sharpeRatio')
                break
            elif status in ["Failure", "RuntimeError", "Runtime Error", "Cancelled"]:
                print(f"Failed with status: {status}")
                break
                
            time.sleep(10)
            
        if cagr is None:
            continue
            
        print(f"CAGR: {cagr}, DD: {draw}, Sharpe: {sharpe}")
        
        res = get_backtest_status(PROJECT_ID, bt_id)
        yearly = extract_yearly_returns(res)
        
        log_entry = f"\n## {strat['desc']}\n*   **Backtest ID:** {bt_id}\n*   **Results:** CAGR {cagr}, MaxDD {draw}, Sharpe {sharpe}.\n*   **Yearly Returns:** {json.dumps(yearly)}\n"
        with open(log_file, "a") as f:
            f.write(log_entry)
            
        print("Logged results.")

if __name__ == "__main__":
    main()
