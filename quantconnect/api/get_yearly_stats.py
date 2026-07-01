import os
import warnings
# Silence warnings at the earliest possible moment
os.environ["PYTHONWARNINGS"] = "ignore"
warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL")

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
    # QC's rollingWindow contains trailing-window slices keyed
    # "M{months}_YYYYMMDD" (e.g. M12_20151231 = trailing 12 months ending
    # 2015-12-31, i.e. exactly calendar year 2015). Use each M12 window
    # ending Dec 31 directly — its own start->end IS the calendar-year return.
    #
    # Do NOT chain December endEquity across windows: consecutive trailing
    # windows are sampled at slightly different year-boundary equities
    # (e.g. 2014 window ends 141543 but 2015 window starts 138541), so the
    # ~2% mismatch swamps near-flat years and distorts them toward 0%.
    rolling = res.get("backtest", {}).get("rollingWindow", {})
    if not rolling: return {}

    final = {}
    for key, val in rolling.items():
        if not key.startswith("M12_") or not key.endswith("1231"):
            continue
        year = key.split("_")[1][:4]
        ps = val.get("portfolioStatistics", {})
        start_eq = float(ps.get("startEquity", 0) or 0)
        end_eq = float(ps.get("endEquity", 0) or 0)
        if start_eq > 0:
            final[year] = round((end_eq / start_eq - 1) * 100)
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
    
    sorted_years = sorted(yearly.keys())
    
    # Width calculation: Emojis are 2 cells wide, but len() sees them as 1.
    col_width = 8
    header_parts = []
    divider_parts = []
    row_parts = []
    
    for y in sorted_years:
        ret = yearly[y]
        emoji = "🟢" if ret > 0 else "🔴" if ret < 0 else "⚪"
        content = f"{emoji} {ret}%"
        
        # Header
        header_parts.append(f"{y:<{col_width}}")
        
        # Divider
        divider_parts.append("-" * col_width)
        
        # Row Content: Manual Padding for emoji visual width
        # Python len() sees emoji as 1, but terminal renders as 2.
        # So visual_len = len(content) + 1
        visual_len = len(content) + 1
        padding = max(0, col_width - visual_len)
        row_parts.append(content + (" " * padding))
        
    print(" | ".join(header_parts))
    print("-+-".join(divider_parts))
    print(" | ".join(row_parts))


if __name__ == "__main__":
    main()
