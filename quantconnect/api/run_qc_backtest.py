import os
import warnings
# Silence warnings at the earliest possible moment
os.environ["PYTHONWARNINGS"] = "ignore"
warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL")

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
    print(f"Uploading {filepath} to main.py...", file=sys.stderr)
    resp = requests.post(f"{BASE_URL}/files/update", headers=headers,
                         json={"projectId": PROJECT_ID, "name": "main.py", "content": content})
    if not resp.json().get("success"):
        print(f"Failed to upload: {resp.json()}", file=sys.stderr)
        sys.exit(1)

    # 2. Compile
    print("Compiling...", file=sys.stderr)
    resp = requests.post(f"{BASE_URL}/compile/create", headers=headers,
                         json={"projectId": PROJECT_ID})
    cr = resp.json()
    if not cr.get("success"):
        print(f"Compile trigger failed: {cr}", file=sys.stderr)
        sys.exit(1)
    
    compile_id = cr["compileId"]
    print(f"Compile ID: {compile_id}", file=sys.stderr)

    # 3. Poll Compile Status
    iterations = 0
    while True:
        resp = requests.get(f"{BASE_URL}/compile/read", headers=headers,
                            params={"projectId": PROJECT_ID, "compileId": compile_id})
        data = resp.json()
        if not data.get("success"):
            print(f"Error reading compile: {data}", file=sys.stderr)
            sys.exit(1)
            
        # QC API can return status/state in different places
        status = data.get("state") or data.get("status") or data.get("compile", {}).get("status", "")
        print(f"Compile Status: {status or '(waiting)'}...", end="\r", file=sys.stderr, flush=True)
        
        if status == "BuildSuccess":
            print("\nCompile Successful!", file=sys.stderr)
            break
        elif status == "BuildError":
            print("\nCompile Failed!", file=sys.stderr)
            logs = data.get("logs") or data.get("compile", {}).get("logs", [])
            for log in logs:
                print(f"  {log}", file=sys.stderr)
            sys.exit(1)
            
        time.sleep(2)

    # 4. Create Backtest
    print(f"Starting backtest '{name}'...", file=sys.stderr)
    resp = requests.post(f"{BASE_URL}/backtests/create", headers=headers,
                         json={"projectId": PROJECT_ID, "compileId": compile_id, "backtestName": name})
    br = resp.json()
    if not br.get("success"):
        print(f"Backtest trigger failed: {br}", file=sys.stderr)
        sys.exit(1)

    bid = br["backtest"]["backtestId"]
    print(f"BACKTEST_ID={bid}")

if __name__ == "__main__":
    main()
