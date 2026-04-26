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
    yearly_returns = {}
    
    # QuantConnect rollingWindow has keys like "M1_20231231"
    # We want to find the last month of each year to get the cumulative profit for that year
    # Actually, it's easier to just calculate it from the totalNetProfit if available 
    # Or look at the "portfolioStatistics" in the window
    
    sorted_keys = sorted(rolling.keys())
    
    # Mapping years to the last profit value seen in that year
    years_data = {}
    for key in sorted_keys:
        if "_" not in key: continue
        date_str = key.split("_")[1]
        year = date_str[:4]
        
        profit = float(rolling[key].get("portfolioStatistics", {}).get("totalNetProfit", 0))
        years_data[year] = profit * 100 # Convert to percentage

    # yearly_returns[year] = current_total_profit - previous_total_profit
    # This is rough but gives a sense of yearly performance
    final_yearly = {}
    prev_profit = 0
    for year in sorted(years_data.keys()):
        total_profit = years_data[year]
        # This formula is slightly off for compounding but good for a row summary
        final_yearly[year] = round(total_profit - prev_profit)
        prev_profit = total_profit
        
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
