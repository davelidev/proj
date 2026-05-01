import os
import sys
import time
import requests
import hashlib
import base64
import json
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

def extract_yearly(res):
    rolling = res.get("backtest", {}).get("rollingWindow", {})
    if not rolling: return {}
    sorted_keys = sorted(rolling.keys())
    yearly_equity = {}
    for key in sorted_keys:
        # Expected format: "RollingWindow_YYYY_MM_DD"
        if "_" not in key: continue
        parts = key.split("_")
        if len(parts) < 2: continue
        year = parts[1][:4]
        equity = float(rolling[key].get("portfolioStatistics", {}).get("endEquity", 100000))
        yearly_equity[year] = equity
    
    final = {}
    # Find the starting equity from the first window
    first_key = sorted_keys[0]
    prev = float(rolling[first_key].get("portfolioStatistics", {}).get("startEquity", 100000))
    
    for y in sorted(yearly_equity.keys()):
        val = (yearly_equity[y] / prev) - 1
        final[y] = round(val * 100)
        prev = yearly_equity[y]
    return final

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 api/get_yearly_stats.py <backtest_id>")
        sys.exit(1)

    bid = sys.argv[1]
    headers = get_auth_headers()

    resp = requests.get(f"{BASE_URL}/backtests/read", headers=headers,
                        params={"projectId": PROJECT_ID, "backtestId": bid})
    data = resp.json()
    if not data.get("success"):
        print(f"Error: {data}")
        sys.exit(1)
        
    yearly = extract_yearly(data)
    print("\nYearly Returns:")
    for year, ret in yearly.items():
        emoji = "🟢" if ret > 0 else "🔴" if ret < 0 else "⚪"
        print(f"  {year}: {emoji} {ret}%")

if __name__ == "__main__":
    main()
