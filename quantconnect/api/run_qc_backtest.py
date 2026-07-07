import os
import warnings
# Silence warnings at the earliest possible moment
os.environ["PYTHONWARNINGS"] = "ignore"
warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL")

import re
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

BASE_PY_PATH = "/Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/utils/base.py"

def get_auth_headers():
    timestamp = str(int(time.time()))
    token_hash = hashlib.sha256(f"{API_TOKEN}:{timestamp}".encode()).hexdigest()
    auth_64 = base64.b64encode(f"{USER_ID}:{token_hash}".encode()).decode()
    return {"Authorization": f"Basic {auth_64}", "Timestamp": timestamp}

def upload_file(name, content, headers):
    """Update a project file, creating it first if it doesn't exist yet."""
    resp = requests.post(f"{BASE_URL}/files/update", headers=headers,
                         json={"projectId": PROJECT_ID, "name": name, "content": content})
    if resp.json().get("success"):
        return True
    # File may not exist yet — create it.
    resp = requests.post(f"{BASE_URL}/files/create", headers=headers,
                         json={"projectId": PROJECT_ID, "name": name, "content": content})
    return resp.json().get("success", False)

def consolidate_with_base(content, base_content):
    """Inline base.py into content if it contains 'from base import' lines."""
    if "from base import" not in content:
        return content
    # Strip AlgorithmImports from base (content already has it at the top)
    base_stripped = re.sub(r"^from AlgorithmImports import \*[ \t]*\n", "", base_content, flags=re.MULTILINE)
    # Remove all 'from base import ...' lines from target
    content = re.sub(r"^from base import [^\n]*\n", "", content, flags=re.MULTILINE)
    # Insert base body right after 'from AlgorithmImports import *'
    def _insert(m):
        return m.group(0) + "\n" + base_stripped.rstrip() + "\n\n"
    content = re.sub(r"from AlgorithmImports import \*[ \t]*\n", _insert, content, count=1)
    return content


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 api/run_qc_backtest.py <file_path> <backtest_name>")
        sys.exit(1)

    filepath = sys.argv[1]
    name = sys.argv[2]

    with open(filepath, "r") as f:
        content = f.read()

    with open(BASE_PY_PATH, "r") as f:
        base_content = f.read()

    content = consolidate_with_base(content, base_content)

    headers = get_auth_headers()

    # 1. Upload consolidated content as main.py (base.py inlined if needed).
    print(f"Uploading {filepath} to main.py...", file=sys.stderr)
    if not upload_file("main.py", content, headers):
        print("Failed to upload main.py", file=sys.stderr)
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

    # 4. Create Backtest — retry with backoff when QC throttles ("Too many
    # backtest requests; please slow down"), which happens during batch runs.
    print(f"Starting backtest '{name}'...", file=sys.stderr)
    br = None
    for attempt in range(8):
        # Fresh headers each attempt: the auth timestamp must stay current across backoffs.
        resp = requests.post(f"{BASE_URL}/backtests/create", headers=get_auth_headers(),
                             json={"projectId": PROJECT_ID, "compileId": compile_id, "backtestName": name})
        br = resp.json()
        if br.get("success"):
            break
        errs = str(br.get("errors", ""))
        if "Too many" in errs or "slow down" in errs or "rate" in errs.lower():
            wait = min(120, 15 * (attempt + 1))
            print(f"  Rate limited; retrying in {wait}s (attempt {attempt + 1}/8)...", file=sys.stderr)
            time.sleep(wait)
            continue
        # Non-throttle error: fail fast.
        print(f"Backtest trigger failed: {br}", file=sys.stderr)
        sys.exit(1)

    if not br or not br.get("success"):
        print(f"Backtest trigger failed after retries: {br}", file=sys.stderr)
        sys.exit(1)

    bid = br["backtest"]["backtestId"]
    print(f"BACKTEST_ID={bid}")

if __name__ == "__main__":
    main()
