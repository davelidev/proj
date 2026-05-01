import os
import sys
import time
import json
import requests
import hashlib
import base64
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

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 api/run_qc_backtest.py <file_path> <backtest_name>")
        sys.exit(1)

    filepath = sys.argv[1]
    name = sys.argv[2]

    with open(filepath, "r") as f:
        content = f.read()

    headers = get_auth_headers()
    
    # 1. Update project file (main.py)
    print(f"Uploading {filepath} to main.py...")
    resp = requests.post(f"{BASE_URL}/files/update", headers=headers,
                         json={"projectId": PROJECT_ID, "name": "main.py", "content": content})
    if not resp.json().get("success"):
        print(f"Failed to upload: {resp.json()}")
        sys.exit(1)

    # 2. Compile
    print("Compiling...")
    resp = requests.post(f"{BASE_URL}/compile/create", headers=headers,
                         json={"projectId": PROJECT_ID})
    cr = resp.json()
    if not cr.get("success"):
        print(f"Compile failed: {cr}")
        sys.exit(1)
    
    compile_id = cr["compileId"]

    # 3. Create Backtest
    print("Waiting for compile to register...")
    time.sleep(5)
    print(f"Starting backtest '{name}'...")
    resp = requests.post(f"{BASE_URL}/backtests/create", headers=headers,
                         json={"projectId": PROJECT_ID, "compileId": compile_id, "backtestName": name})
    br = resp.json()
    if not br.get("success"):
        print(f"Backtest trigger failed: {br}")
        sys.exit(1)

    bid = br["backtest"]["backtestId"]
    print(f"Backtest ID: {bid}")

if __name__ == "__main__":
    main()
