import os
import warnings
os.environ["PYTHONWARNINGS"] = "ignore"
warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL")

import sys
import time
import requests
import hashlib
import base64
from dotenv import load_dotenv

load_dotenv()

USER_ID = os.environ.get("QC_USER_ID")
API_TOKEN = os.environ.get("QC_API_TOKEN")
PROJECT_ID = os.environ.get("QC_PROJECT_ID")
BASE_URL = os.environ.get("QC_BASE_URL", "https://www.quantconnect.com/api/v2")

def get_auth_headers():
    timestamp = str(int(time.time()))
    token_hash = hashlib.sha256(f"{API_TOKEN}:{timestamp}".encode()).hexdigest()
    auth_64 = base64.b64encode(f"{USER_ID}:{token_hash}".encode()).decode()
    return {"Authorization": f"Basic {auth_64}", "Timestamp": timestamp}

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 api/poll_backtest.py <backtest_id>")
        sys.exit(1)

    bid = sys.argv[1]
    headers = get_auth_headers()

    while True:
        resp = requests.get(f"{BASE_URL}/backtests/read", headers=headers,
                            params={"projectId": PROJECT_ID, "backtestId": bid})
        data = resp.json()
        if not data.get("success"):
            print(f"Error reading backtest: {data}")
            sys.exit(1)
            
        bt = data.get("backtest", {})
        status = bt.get("status", "")
        progress = float(bt.get("progress", 0)) * 100
        
        # Clear the line with spaces to prevent trailing artifacts
        status_line = f"Status: {status} ({progress:.2f}%)"
        print(f"\r{status_line:<50}", end="", flush=True)
        
        if status in ["Completed", "Completed."]:
            stats = bt.get("statistics", {})
            
            # Check if stats are actually populated. 
            # Often QC returns a 'Completed' status before the summary stats are aggregated.
            # We check if 'Total Orders' is "0" and 'Compounding Annual Return' is "0%" as a proxy for 'not ready'.
            is_empty = not stats or (stats.get("Total Orders") == "0" and stats.get("Compounding Annual Return") == "0%")
            
            if is_empty:
                time.sleep(2)
                continue

            print("\nBacktest Completed!\n")
            
            # Map metrics to their QuantConnect API keys
            cagr_raw = stats.get("Compounding Annual Return", "0%")
            max_dd_raw = stats.get("Drawdown", "0%")
            
            # Remove decimals and format
            try:
                cagr = f"{round(float(cagr_raw.strip('%')))}%"
                max_dd = f"-{round(float(max_dd_raw.strip('%')))}%"
            except (ValueError, TypeError):
                cagr = cagr_raw
                max_dd = max_dd_raw
            
            sharpe = stats.get("Sharpe Ratio", "0")
            trades = stats.get("Total Orders", "0")
            win_pct = stats.get("Win Rate", "0%")
            loss_pct = stats.get("Loss Rate", "0%")
            pl_ratio = stats.get("Profit-Loss Ratio", "0")

            # Output Aligned Terminal Table
            cols = [
                ("CAGR", cagr, 6),
                ("MaxDD", max_dd, 6),
                ("Sharpe", sharpe, 8),
                ("Trades", trades, 8),
                ("Win %", win_pct, 8),
                ("Loss %", loss_pct, 8),
                ("P/L Ratio", pl_ratio, 9)
            ]
            
            header = " | ".join(f"{c:<{w}}" for c, v, w in cols)
            row    = " | ".join(f"{v:<{w}}" for c, v, w in cols)
            divider = "-" * len(header)
            
            print(header)
            print(divider)
            print(row)
            break
            
        if status in ["Failure", "RuntimeError", "Runtime Error", "Cancelled"]:
            print(f"\nBacktest failed with status: {status}")
            print(f"Error: {bt.get('error', 'Unknown error')}")
            break
            
        time.sleep(2)

if __name__ == "__main__":
    main()
