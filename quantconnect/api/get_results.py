import requests
import time
import hashlib
import base64
import os
import sys
import json
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
    resp = requests.get(
        f"{BASE_URL}/backtests/read",
        headers=get_auth_headers(),
        params={"projectId": project_id, "backtestId": backtest_id}
    )
    return resp.json()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_results.py <backtest_id>")
        sys.exit(1)
    
    bid = sys.argv[1]
    res = get_backtest_status(PROJECT_ID, bid)
    print(json.dumps(res, indent=4))
