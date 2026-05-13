import os, requests, hashlib, base64, time, json
from dotenv import load_dotenv
load_dotenv()
USER_ID = os.environ["QC_USER_ID"]
API_TOKEN = os.environ["QC_API_TOKEN"]
PROJECT_ID = os.environ["QC_PROJECT_ID"]
BASE_URL = os.environ.get("QC_BASE_URL", "https://www.quantconnect.com/api/v2")
ts = str(int(time.time()))
h = hashlib.sha256(f"{API_TOKEN}:{ts}".encode()).hexdigest()
a = base64.b64encode(f"{USER_ID}:{h}".encode()).decode()
headers = {"Authorization": f"Basic {a}", "Timestamp": ts}
resp = requests.get(f"{BASE_URL}/backtests/read", headers=headers,
                    params={"projectId": PROJECT_ID, "backtestId": "55be8f049e538bae17672a8afcd57392"})
data = resp.json()
bt = data.get("backtest", {})
print("All bt keys:", list(bt.keys()))
rw = bt.get("rollingWindow", {})
print("rollingWindow keys (first 10):", list(rw.keys())[:10])
print("rollingWindow sample:", json.dumps(dict(list(rw.items())[:2]), indent=2, ensure_ascii=False) if rw else "empty")
