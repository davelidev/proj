import requests
import time
import hashlib
import base64
import os
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
# Get these from https://www.quantconnect.com/settings
USER_ID = os.environ.get("QC_USER_ID", "YOUR_USER_ID")
API_TOKEN = os.environ.get("QC_API_TOKEN", "YOUR_API_TOKEN")

# Find the project ID in the URL of your project: e.g. quantconnect.com/terminal/process/1234567
PROJECT_ID = "30379669"
BASE_URL = "https://www.quantconnect.com/api/v2"

def get_auth_headers():
    """Generates the required authentication headers for QuantConnect API."""
    timestamp = str(int(time.time()))
    # Hash format: sha256(API_TOKEN + ":" + timestamp)
    token_hash = hashlib.sha256(f"{API_TOKEN}:{timestamp}".encode('utf-8')).hexdigest()
    # Auth format: base64(USER_ID + ":" + token_hash)
    auth_str = f"{USER_ID}:{token_hash}"
    auth_64 = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
    
    return {
        "Authorization": f"Basic {auth_64}",
        "Timestamp": timestamp
    }

def update_project_file(project_id, filename, content):
    """Updates a file in the QuantConnect project."""
    print(f"Updating {filename} in project {project_id}...")
    try:
        resp = requests.post(
            f"{BASE_URL}/files/update",
            headers=get_auth_headers(),
            json={
                "projectId": project_id,
                "name": filename,
                "content": content
            }
        )
        return resp.json().get("success")
    except Exception as e:
        print(f"API Error updating file: {e}")
        return False

def trigger_backtest(project_id, strategy_file, name="API Backtest"):
    if USER_ID == "YOUR_USER_ID" or API_TOKEN == "YOUR_API_TOKEN":
        print("Please update your QC_USER_ID and QC_API_TOKEN configuration in .env.")
        return

    # 1. Read the local strategy file
    with open(strategy_file, 'r') as f:
        content = f.read()

    # 2. Update main.py in the project
    if not update_project_file(project_id, "main.py", content):
        print("Failed to update main.py")
        return

    # 3. Request a Compile (Required to get a compileId)
    print(f"Compiling project {project_id}...")
    try:
        resp = requests.post(
            f"{BASE_URL}/compile/create",
            headers=get_auth_headers(),
            json={"projectId": project_id}
        )
        compile_resp = resp.json()
    except Exception as e:
        print(f"API Error: {e}")
        raise e

    if not compile_resp.get("success"):
        raise Exception(f"Compile failed: {compile_resp.get('errors')}")

    compile_id = compile_resp["compileId"]
    print(f"Compile successful. ID: {compile_id}")

    # Wait a moment for compile to be registered
    time.sleep(2)

    # 4. Trigger the Backtest
    print(f"Triggering backtest: {name}...")
    try:
        resp = requests.post(
            f"{BASE_URL}/backtests/create",
            headers=get_auth_headers(),
            json={
                "projectId": project_id,
                "compileId": compile_id,
                "backtestName": name
            }
        )
        backtest_resp = resp.json()
    except Exception as e:
        print(f"API Error: {e}")
        raise e

    if backtest_resp.get("success"):
        backtest_id = backtest_resp['backtest']['backtestId']
        print(f"Backtest started successfully! ID: {backtest_id}")
        print(f"View it on the portal: https://www.quantconnect.com/terminal/process/{project_id}?backtestId={backtest_id}")
        return backtest_id
    else:
        print(f"Failed to start backtest: {backtest_resp.get('errors')}")
        return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python run_qc_backtest.py <strategy_file_path> [backtest_name]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    test_name = sys.argv[2] if len(sys.argv) > 2 else f"Backtest {os.path.basename(file_path)}"
    trigger_backtest(PROJECT_ID, file_path, test_name)
