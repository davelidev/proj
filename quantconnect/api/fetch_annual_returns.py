import os, sys, requests, hashlib, base64, time
from dotenv import load_dotenv
load_dotenv()

USER_ID = os.environ["QC_USER_ID"]
API_TOKEN = os.environ["QC_API_TOKEN"]
PROJECT_ID = os.environ["QC_PROJECT_ID"]
BASE_URL = os.environ.get("QC_BASE_URL", "https://www.quantconnect.com/api/v2")

def get_headers():
    ts = str(int(time.time()))
    h = hashlib.sha256(f"{API_TOKEN}:{ts}".encode()).hexdigest()
    a = base64.b64encode(f"{USER_ID}:{h}".encode()).decode()
    return {"Authorization": f"Basic {a}", "Timestamp": ts}

def annual_returns(bid):
    resp = requests.get(f"{BASE_URL}/backtests/read", headers=get_headers(),
                        params={"projectId": PROJECT_ID, "backtestId": bid})
    rw = resp.json().get("backtest", {}).get("rollingWindow", {})
    by_year = {}
    for key, val in rw.items():
        if not key.startswith("M1_"): continue
        try: year = int(key[3:7])
        except ValueError: continue
        by_year.setdefault(year, []).append((key, val))
    result = {}
    for year in range(2014, 2026):
        entries = sorted(by_year.get(year, []), key=lambda x: x[0])
        if not entries: continue
        start_eq = float(entries[0][1]["portfolioStatistics"]["startEquity"])
        end_eq = float(entries[-1][1]["portfolioStatistics"]["endEquity"])
        if start_eq > 0:
            result[year] = round((end_eq / start_eq - 1) * 100)
    return result

if len(sys.argv) < 2:
    print("Usage: python3 api/fetch_annual_returns.py <backtest_id>")
    sys.exit(1)

bid = sys.argv[1]
ar = annual_returns(bid)
print(f"{'Year':<6} {'Return':>7}")
print("-" * 14)
for y, v in sorted(ar.items()):
    emoji = "🟢" if v >= 0 else "🔴"
    print(f"{y}   {emoji} {v:+}%")
