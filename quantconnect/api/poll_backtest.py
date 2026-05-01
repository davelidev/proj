import os
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
        print(f"Status: {status} ({progress:.2f}%)", end="\r")
        
        if status in ["Completed", "Completed."]:
            print("\nBacktest Completed!")
            stats = bt.get("statistics", {})
            print("\nStatistics:")
            for key, val in stats.items():
                print(f"  {key}: {val}")
            break
            
        if status in ["Failure", "RuntimeError", "Runtime Error", "Cancelled"]:
            print(f"\nBacktest failed with status: {status}")
            print(f"Error: {bt.get('error', 'Unknown error')}")
            break
            
        time.sleep(10)

if __name__ == "__main__":
    main()
