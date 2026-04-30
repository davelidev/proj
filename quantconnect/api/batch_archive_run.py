import os
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
BASE_URL = os.environ.get("QC_BASE_URL")

ARCHIVE_DIR = "QuantConnect/archive"
OUTPUT_FILE = "QuantConnect/archive/Backtests.md"
RESULTS_JSON = "QuantConnect/api/archive_batch_results.json"

def get_auth_headers():
    timestamp = str(int(time.time()))
    token_hash = hashlib.sha256(f"{API_TOKEN}:{timestamp}".encode('utf-8')).hexdigest()
    auth_str = f"{USER_ID}:{token_hash}"
    auth_64 = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
    return {"Authorization": f"Basic {auth_64}", "Timestamp": timestamp}

def update_project_file(content):
    requests.post(f"{BASE_URL}/files/update", headers=get_auth_headers(),
                 json={"projectId": PROJECT_ID, "name": "main.py", "content": content})

def trigger_backtest(name):
    compile_resp = requests.post(f"{BASE_URL}/compile/create", headers=get_auth_headers(),
                                json={"projectId": PROJECT_ID}).json()
    if not compile_resp.get("success"): return None
    cid = compile_resp["compileId"]
    time.sleep(2)
    bt_resp = requests.post(f"{BASE_URL}/backtests/create", headers=get_auth_headers(),
                           json={"projectId": PROJECT_ID, "compileId": cid, "backtestName": name}).json()
    return bt_resp.get("backtest", {}).get("backtestId")

def get_status(bid):
    try:
        return requests.get(f"{BASE_URL}/backtests/read", headers=get_auth_headers(),
                          params={"projectId": PROJECT_ID, "backtestId": bid}).json()
    except: return None

def extract_yearly(res):
    rolling = res.get("backtest", {}).get("rollingWindow", {})
    if not rolling: return {}
    sorted_keys = sorted(rolling.keys())
    yearly_equity = {}
    for key in sorted_keys:
        if "_" not in key: continue
        year = key.split("_")[1][:4]
        equity = float(rolling[key].get("portfolioStatistics", {}).get("endEquity", 100000))
        yearly_equity[year] = equity
    final = {}
    prev = float(rolling[sorted_keys[0]].get("portfolioStatistics", {}).get("startEquity", 100000))
    for y in sorted(yearly_equity.keys()):
        val = (yearly_equity[y] / prev) - 1
        final[y] = round(val * 100)
        prev = yearly_equity[y]
    return final

def to_float(val):
    if val is None: return None
    try:
        return float(str(val).replace('%',''))
    except:
        return None

def main():
    strategies = [f for f in os.listdir(ARCHIVE_DIR) if f.endswith(".py")]
    strategies.sort()
    
    results = {}
    if os.path.exists(RESULTS_JSON):
        with open(RESULTS_JSON, 'r') as f:
            results = json.load(f)

    for strategy in strategies:
        if strategy in results and results[strategy].get("status") == "Completed.":
            continue
            
        print(f"--- Running {strategy} ---")
        with open(os.path.join(ARCHIVE_DIR, strategy), 'r') as f:
            content = f.read()
        
        update_project_file(content)
        bid = trigger_backtest(f"Archive: {strategy}")
        if not bid: 
            print(f"Failed to trigger {strategy}")
            continue
            
        while True:
            res = get_status(bid)
            if not res: break
            status = res.get("backtest", {}).get("status")
            progress = res.get("backtest", {}).get("progress", 0)
            print(f"Status: {status}, Progress: {float(progress)*100:.2f}%", end="\r")
            
            if status == "Completed.":
                stats = res.get("backtest", {}).get("statistics", {})
                if not stats:
                    rw = res.get("backtest", {}).get("rollingWindow", {})
                    if rw: stats = rw[sorted(rw.keys())[-1]].get("portfolioStatistics", {})
                
                results[strategy] = {
                    "id": bid,
                    "status": status,
                    "CAGR": stats.get("compoundingAnnualReturn") or stats.get("Compounding Annual Return"),
                    "MaxDD": stats.get("drawdown") or stats.get("Drawdown"),
                    "Sharpe": stats.get("sharpeRatio") or stats.get("Sharpe Ratio"),
                    "Yearly": extract_yearly(res)
                }
                break
            elif status in ["Failure", "RuntimeError", "Cancelled"]:
                # Mark as failed to skip next time
                results[strategy] = {"status": status}
                break
            time.sleep(10)
            
        with open(RESULTS_JSON, 'w') as f:
            json.dump(results, f, indent=4)

    # Generate Markdown (two-table format)
    completed = {s: r for s, r in results.items() if r.get("status") == "Completed."}
    years = ["2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"]

    def fmt_row(s, r):
        cagr_val = to_float(r['CAGR'])
        dd_val = to_float(r['MaxDD'])
        sharpe_val = to_float(r['Sharpe'])
        if cagr_val is not None and abs(cagr_val) < 1.0: cagr_val *= 100
        if dd_val is not None and abs(dd_val) < 1.0: dd_val *= 100
        cagr = f"{cagr_val:.0f}%" if cagr_val is not None else "N/A"
        dd = f"-{abs(dd_val):.0f}%" if dd_val is not None else "N/A"
        sharpe = f"{sharpe_val:.2f}" if sharpe_val is not None else "N/A"
        return s, cagr, dd, sharpe

    md = "# Archived Strategy Backtests\n\n"
    md += "| Strategy | CAGR | MaxDD | Sharpe |\n"
    md += "| :--- | :--- | :--- | :--- |\n"
    for s in sorted(completed.keys()):
        _, cagr, dd, sharpe = fmt_row(s, completed[s])
        md += f"| {s} | {cagr} | {dd} | {sharpe} |\n"

    md += "\n"
    md += "| Strategy | " + " | ".join(y[2:] for y in years) + " |\n"
    md += "| :--- | " + " | ".join(":---" for _ in years) + " |\n"
    for s in sorted(completed.keys()):
        yearly = completed[s].get("Yearly", {})
        row = f"| {s} | "
        for year in years:
            val = yearly.get(year)
            if val is None:
                row += "- | "
            else:
                emoji = "🟢" if val > 0 else "🔴" if val < 0 else "⚪"
                row += f"{emoji} {val}% | "
        md += row + "\n"

    with open(OUTPUT_FILE, "w") as f:
        f.write(md)
    print("\nDone! Updated " + OUTPUT_FILE)

if __name__ == "__main__":
    main()
