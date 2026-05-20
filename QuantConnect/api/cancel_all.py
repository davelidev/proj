import os, time, json, hashlib, base64, requests
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "api", ".env")
load_dotenv(dotenv_path)

USER_ID = os.environ.get("QC_USER_ID")
API_TOKEN = os.environ.get("QC_API_TOKEN")
PROJECT_ID = os.environ.get("QC_PROJECT_ID")
BASE_URL = os.environ.get("QC_BASE_URL", "https://www.quantconnect.com/api/v2")

def get_auth_headers():
    timestamp = str(int(time.time()))
    token_hash = hashlib.sha256(f"{API_TOKEN}:{timestamp}".encode()).hexdigest()
    auth_64 = base64.b64encode(f"{USER_ID}:{token_hash}".encode()).decode()
    return {"Authorization": f"Basic {auth_64}", "Timestamp": timestamp}

headers = get_auth_headers()
r = requests.get(f"{BASE_URL}/backtests/list", headers=headers, params={"projectId": PROJECT_ID})
data = r.json()

if data.get("success"):
    for bt in data.get("backtests", []):
        status = bt.get("status", "")
        if "Progress" in status or "Queue" in status or "Running" in status:
            print(f"Cancelling {bt['name']} ({bt['backtestId']})...")
            requests.post(f"{BASE_URL}/backtests/update", headers=headers,
                          json={"projectId": PROJECT_ID, "backtestId": bt["backtestId"],
                                "name": bt["name"], "status": "Cancel"})
else:
    print(f"Error listing backtests: {data}")
