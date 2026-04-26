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
PROJECT_ID = os.environ.get("QC_PROJECT_ID")
BASE_URL = os.environ.get("QC_BASE_URL")

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

def verify(bid):
    res = get_backtest_status(PROJECT_ID, bid)
    rolling = res.get("backtest", {}).get("rollingWindow", {})
    
    sorted_keys = sorted(rolling.keys())
    
    start_equity = float(rolling[sorted_keys[0]].get("portfolioStatistics", {}).get("startEquity", 100000))
    print(f"Initial Start Equity: {start_equity}")
    
    multiplier = 1.0
    prev_equity = start_equity
    
    for key in sorted_keys:
        if "_" not in key: continue
        year = key.split("_")[1][:4]
        end_equity = float(rolling[key].get("portfolioStatistics", {}).get("endEquity"))
        
        annual_return = (end_equity / prev_equity) - 1
        print(f"Year {year}: End Equity = {end_equity:,.2f}, Return = {annual_return*100:.2f}%")
        
        multiplier *= (1 + annual_return)
        prev_equity = end_equity
        
    total_return_calc = (multiplier - 1) * 100
    print(f"\nCalculated Total Return: {total_return_calc:,.3f}%")
    
    actual_total = res.get("backtest", {}).get("statistics", {}).get("Total Net Profit", "0").replace("%", "").replace(",", "")
    print(f"API Reported Total Return: {actual_total}%")

if __name__ == "__main__":
    verify("6286a46e5d87071c52fae9f1307f3e84")
