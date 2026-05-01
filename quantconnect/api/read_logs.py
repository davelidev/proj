import os
import sys
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

import time

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 api/read_logs.py <backtest_id>")
        sys.exit(1)

    bid = sys.argv[1]
    headers = get_auth_headers()

    resp = requests.get(f"{BASE_URL}/backtests/read", headers=headers,
                        params={"projectId": PROJECT_ID, "backtestId": bid})
    data = resp.json()
    if not data.get("success"):
        print(f"Error: {data}")
        sys.exit(1)
        
    bt = data.get("backtest", {})
    logs = bt.get("logs", [])
    if not logs:
        print("No logs found.")
    else:
        for log in logs:
            print(log)

if __name__ == "__main__":
    main()
