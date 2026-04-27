import requests
import time
import hashlib
import base64
import os
import sys
import json
import random
from dotenv import load_dotenv

from get_yearly_stats import extract_yearly_returns

load_dotenv()

USER_ID = os.environ.get("QC_USER_ID")
API_TOKEN = os.environ.get("QC_API_TOKEN")
PROJECT_ID = os.environ.get("QC_PROJECT_ID")
BASE_URL = os.environ.get("QC_BASE_URL")

RESEARCH_LOG = "research/research_log.md"
STRATEGY_TEMPLATE = "research/strategy_template_v3.py"

def get_auth_headers():
    timestamp = str(int(time.time()))
    token_hash = hashlib.sha256(f"{API_TOKEN}:{timestamp}".encode('utf-8')).hexdigest()
    auth_str = f"{USER_ID}:{token_hash}"
    auth_64 = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
    return {"Authorization": f"Basic {auth_64}", "Timestamp": timestamp}

def update_main_py(content):
    requests.post(f"{BASE_URL}/files/update", headers=get_auth_headers(), 
                 json={"projectId": PROJECT_ID, "name": "main.py", "content": content})

def create_compile():
    resp = requests.post(f"{BASE_URL}/compile/create", headers=get_auth_headers(), 
                        json={"projectId": PROJECT_ID}).json()
    return resp.get("compileId")

def create_backtest(compile_id, name, parameters):
    resp = requests.post(f"{BASE_URL}/backtests/create", headers=get_auth_headers(), 
                        json={
                            "projectId": PROJECT_ID,
                            "compileId": compile_id,
                            "backtestName": name,
                            "parameters": parameters
                        }).json()
    return resp.get("backtest", {}).get("backtestId")

def get_backtest_status(backtest_id):
    try:
        resp = requests.get(f"{BASE_URL}/backtests/read", headers=get_auth_headers(),
                           params={"projectId": PROJECT_ID, "backtestId": backtest_id})
        return resp.json()
    except: return {"success": False}

def format_yearly_table(yearly_dict):
    if not yearly_dict: return ""
    years = sorted(yearly_dict.keys())
    header = "| " + " | ".join(years) + " |"
    divider = "| " + " | ".join([":---" for _ in years]) + " |"
    values = "| " + " | ".join([f"{'🟢' if v>0 else '🔴' if v<0 else '⚪'} {v}%" for v in [yearly_dict[y] for y in years]]) + " |"
    return f"\n{header}\n{divider}\n{values}\n"

def main():
    print("Starting Automated Optimization Engine V3 (Target: Next 300 Iterations)...", flush=True)
    
    with open(STRATEGY_TEMPLATE, "r") as f:
        template_content = f.read()
    
    print("Uploading and Compiling Template V3...", flush=True)
    update_main_py(template_content)
    compile_id = create_compile()
    if not compile_id:
        print("Compile failed. Exiting.")
        return
    
    time.sleep(10)
    
    for i in range(1, 301): # Next 300
        params = {
            "adx_thresh": f"{random.uniform(15, 30):.2f}",
            "vix_ratio_limit": f"{random.uniform(0.95, 1.15):.3f}",
            "atr_mult": f"{random.uniform(2.5, 4.0):.2f}",
            "mom_period": str(random.choice([10, 21, 42, 63]))
        }
        
        test_name = f"Auto-Opt V3 Iteration {i}"
        print(f"\n--- [{i}/300] Triggering: {test_name} ---", flush=True)
        bt_id = create_backtest(compile_id, test_name, params)
        
        if not bt_id:
            print("Rate limit or API error. Waiting 60s...", flush=True)
            time.sleep(60)
            bt_id = create_backtest(compile_id, test_name, params)
            if not bt_id: continue
            
        print(f"Backtest ID: {bt_id}", flush=True)
        
        while True:
            res = get_backtest_status(bt_id)
            if not res or not res.get("success"): break
            bt = res.get("backtest", {})
            status = bt.get("status")
            progress = bt.get("progress", 0)
            print(f"Status: {status}, Progress: {float(progress)*100:.2f}%", flush=True)
            
            if status in ["Completed", "Completed."]:
                stats = bt.get("statistics", {})
                if not stats:
                    rw = bt.get("rollingWindow", {})
                    if rw:
                        last_key = sorted(rw.keys())[-1]
                        stats = rw[last_key].get("portfolioStatistics", {})
                
                cagr_str = (stats.get('Compounding Annual Return') or stats.get('compoundingAnnualReturn') or "0").replace('%','')
                draw_str = (stats.get('Drawdown') or stats.get('drawdown') or "0").replace('%','')
                sharpe_str = stats.get('Sharpe Ratio') or stats.get('sharpeRatio') or "0"
                
                cagr = float(cagr_str)
                draw = float(draw_str)
                sharpe = float(sharpe_str)
                
                print(f"Result: CAGR {cagr}%, MaxDD {draw}%, Sharpe {sharpe}", flush=True)
                
                if cagr > 30 and draw < 57:
                    print("✅ WINNER! Logging to research_log.md...", flush=True)
                    yearly = extract_yearly_returns(res)
                    total_profit = stats.get("Total Net Profit") or stats.get("totalNetProfit") or "N/A"
                    
                    log_entry = f"""
---

## Strategy Iteration V3-{i} ({bt_id})

**Core Concept:** Strategy 38 Evolution (Expanding Range + Rotation). 
*   **Parameters:** {json.dumps(params, indent=2)}
*   **Total Return:** {total_profit}
*   **CAGR / Max Drawdown:** {cagr}% / -{draw}%
*   **Sharpe Ratio:** {sharpe}
*   **Yearly Returns:**
{format_yearly_table(yearly)}

> [!code]- Click to view: iteration_v3_{i}.py
> ```embed-python
> PATH: "vault://QuantConnect/strategy_template_v3.py"
> ```
"""
                    with open(RESEARCH_LOG, "a") as f:
                        f.write(log_entry)
                break
            elif status in ["Failure", "RuntimeError", "Runtime Error", "Cancelled"]:
                print(f"Backtest failed: {status}", flush=True)
                break
            time.sleep(20)

if __name__ == "__main__":
    main()
