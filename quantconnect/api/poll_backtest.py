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
        print(f"Status: {status} ({progress:.2f}%)", end="\r", flush=True)
        
        if status in ["Completed", "Completed."]:
            print("\nBacktest Completed!\n")
            stats = bt.get("statistics", {})
            
            # Map metrics to their QuantConnect API keys
            cagr_raw = stats.get("Compounding Annual Return", "0%")
            max_dd_raw = stats.get("Drawdown", "0%")
            
            # Remove decimals and format (e.g., "42.782%" -> "43%")
            cagr = f"{round(float(cagr_raw.strip('%')))}%"
            max_dd = f"-{round(float(max_dd_raw.strip('%')))}%"
            
            sharpe = stats.get("Sharpe Ratio", "0")
            trades = stats.get("Total Orders", "0")
            win_pct = stats.get("Win Rate", "0%")
            loss_pct = stats.get("Loss Rate", "0%")
            pl_ratio = stats.get("Profit-Loss Ratio", "0")

            # Output Aligned Terminal Table
            header = f"{'CAGR':<7} | {'MaxDD':<7} | {'Sharpe':<8} | {'Trades':<8} | {'Win %':<8} | {'Loss %':<8} | {'P/L Ratio':<10}"
            divider = "-" * len(header)
            row = f"{cagr:<7} | {max_dd:<7} | {sharpe:<8} | {trades:<8} | {win_pct:<8} | {loss_pct:<8} | {pl_ratio:<10}"
            
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
