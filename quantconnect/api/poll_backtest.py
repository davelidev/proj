import requests
import time
import hashlib
import base64
import os
import sys
from dotenv import load_dotenv

load_dotenv()

USER_ID = os.environ.get("QC_USER_ID")
API_TOKEN = os.environ.get("QC_API_TOKEN")
PROJECT_ID = "30379669"
BASE_URL = "https://www.quantconnect.com/api/v2"

def get_auth_headers():
    timestamp = str(int(time.time()))
    token_hash = hashlib.sha256(f"{API_TOKEN}:{timestamp}".encode('utf-8')).hexdigest()
    auth_str = f"{USER_ID}:{token_hash}"
    auth_64 = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
    return {"Authorization": f"Basic {auth_64}", "Timestamp": timestamp}

def get_backtest_status(project_id, backtest_id):
    try:
        resp = requests.get(
            f"{BASE_URL}/backtests/read",
            headers=get_auth_headers(),
            params={"projectId": project_id, "backtestId": backtest_id}
        )
        return resp.json()
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python poll_backtest.py <backtest_id>")
        sys.exit(1)
    
    bid = sys.argv[1]
    print(f"Polling backtest {bid}...")
    while True:
        res = get_backtest_status(PROJECT_ID, bid)
        if not res or not res.get("success"):
            print(f"Failed to get status: {res}")
            break
        
        bt = res.get("backtest", {})
        status = bt.get("status")
        progress = bt.get("progress", 0)
        print(f"Status: {status}, Progress: {float(progress)*100:.2f}%")
        
        if status in ["Completed", "Completed."]:
            stats = bt.get("statistics", {})
            if not stats:
                # Try to find stats in rolling window if not in top level
                rw = bt.get("rollingWindow", {})
                if rw:
                    last_key = sorted(rw.keys())[-1]
                    stats = rw[last_key].get("portfolioStatistics", {})
            
            print("\nBacktest Completed!")
            print(f"CAGR: {stats.get('Compounding Annual Return') or stats.get('compoundingAnnualReturn')}")
            print(f"Drawdown: {stats.get('Drawdown') or stats.get('drawdown')}")
            print(f"Sharpe Ratio: {stats.get('Sharpe Ratio') or stats.get('sharpeRatio')}")
            break
        elif status in ["Failure", "RuntimeError", "Cancelled"]:
            print(f"Backtest failed with status: {status}")
            break
        
        time.sleep(10)
