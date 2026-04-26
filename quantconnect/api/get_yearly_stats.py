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

def extract_yearly_returns(res):
    if not res.get("success"):
        return None
    
    rolling = res.get("backtest", {}).get("rollingWindow", {})
    if not rolling:
        return None
        
    sorted_keys = sorted(rolling.keys())
    
    # Track equity at the end of each year
    yearly_equity = {}
    for key in sorted_keys:
        if "_" not in key: continue
        date_str = key.split("_")[1]
        year = date_str[:4]
        
        equity = float(rolling[key].get("portfolioStatistics", {}).get("endEquity", 100000))
        yearly_equity[year] = equity

    final_yearly = {}
    prev_equity = float(res.get("backtest", {}).get("rollingWindow", {}).get(sorted_keys[0], {}).get("portfolioStatistics", {}).get("startEquity", 100000))
    
    for year in sorted(yearly_equity.keys()):
        current_equity = yearly_equity[year]
        # Return = (End / Start) - 1
        year_return = (current_equity / prev_equity) - 1
        final_yearly[year] = round(year_return * 100)
        prev_equity = current_equity
        
    return final_yearly

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_yearly_stats.py <backtest_id>")
        sys.exit(1)
    
    bid = sys.argv[1]
    res = get_backtest_status(PROJECT_ID, bid)
    yearly = extract_yearly_returns(res)
    if yearly:
        print(json.dumps(yearly))
    else:
        print("{}")
