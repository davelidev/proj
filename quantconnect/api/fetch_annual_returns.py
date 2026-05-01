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

bids = {
    "S1": "55be8f049e538bae17672a8afcd57392",
    "S2": "11f33db6f0d8185b32d73523a24b0caa",
    "S3": "1e8cef5d083b1e732561194a3dc0ef50",
    "S4": "dcaf482b6031d3c6c45b1227df68e84c",
    "S5": "71053f9fa498111ac6fc121a6a32308d",
    "S6": "ef41f32475fa9dcd288c0d3f9a91c441",
    "S7": "4c16c0af188a6221c336bac4f09b1a8a",
}

years = list(range(2014, 2026))

def annual_returns(rw):
    by_year = {}
    for key, val in rw.items():
        # skip non-M1 keys
        if not key.startswith("M1_"):
            continue
        try:
            year = int(key[3:7])
        except ValueError:
            continue
        by_year.setdefault(year, []).append((key, val))
    result = {}
    for year in years:
        entries = sorted(by_year.get(year, []), key=lambda x: x[0])
        if not entries:
            continue
        start_eq = float(entries[0][1]["portfolioStatistics"]["startEquity"])
        end_eq = float(entries[-1][1]["portfolioStatistics"]["endEquity"])
        if start_eq > 0:
            result[year] = round((end_eq / start_eq - 1) * 100)
    return result

print(f"{'':4} | " + " | ".join(f"'{y-2000:02d}" for y in years))
print("-" * 110)

for name, bid in bids.items():
    try:
        resp = requests.get(f"{BASE_URL}/backtests/read", headers=get_headers(),
                            params={"projectId": PROJECT_ID, "backtestId": bid})
        data = resp.json()
        rw = data.get("backtest", {}).get("rollingWindow", {})
        ar = annual_returns(rw)
        def fmt(y):
            v = ar.get(y)
            return f"{v:+4}%" if v is not None else "  N/A"
        row = " | ".join(fmt(y) for y in years)
        print(f"{name:4} | {row}")
    except Exception as e:
        print(f"{name:4} | ERROR: {e}", file=sys.stderr)
    time.sleep(0.3)
