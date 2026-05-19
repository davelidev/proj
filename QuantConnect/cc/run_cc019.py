"""cc019 batch runner — reads cc_algos/cc019_NNN.py, saves to backtests/backtest_cc019.json"""
import os, sys, time, json, hashlib, base64, requests
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "api", ".env")
load_dotenv(dotenv_path)

USER_ID    = os.environ.get("QC_USER_ID")
API_TOKEN  = os.environ.get("QC_API_TOKEN")
PROJECT_ID = os.environ.get("QC_PROJECT_ID")
BASE_URL   = os.environ.get("QC_BASE_URL", "https://www.quantconnect.com/api/v2")
TIMEOUT    = 60

def get_auth_headers():
    timestamp  = str(int(time.time()))
    token_hash = hashlib.sha256(f"{API_TOKEN}:{timestamp}".encode()).hexdigest()
    auth_64    = base64.b64encode(f"{USER_ID}:{token_hash}".encode()).decode()
    return {"Authorization": f"Basic {auth_64}", "Timestamp": timestamp}

def req(method, url, **kwargs):
    kwargs.setdefault("timeout", TIMEOUT)
    return requests.request(method, url, **kwargs)

def cancel_running_backtests(headers):
    try:
        r    = req("GET", f"{BASE_URL}/backtests/list", headers=headers, params={"projectId": PROJECT_ID})
        data = r.json()
        for bt in data.get("backtests", []):
            status = bt.get("status", "")
            if "Progress" in status or "Queue" in status:
                bid = bt["backtestId"]
                req("POST", f"{BASE_URL}/backtests/update", headers=headers,
                    json={"projectId": PROJECT_ID, "backtestId": bid, "name": bt["name"], "status": "Cancel"})
                print(f"  [cleanup] Cancelled: {bt['name']} ({bid[:16]}...)")
    except Exception as e:
        print(f"  [cleanup] Warning: {e}")

def run_backtest(filepath, name):
    headers = get_auth_headers()
    cancel_running_backtests(headers)
    time.sleep(2)

    with open(filepath) as f:
        content = f.read()

    # Upload
    r = req("POST", f"{BASE_URL}/files/update", headers=headers,
            json={"projectId": PROJECT_ID, "name": "main.py", "content": content})
    if not r.json().get("success"):
        return {"error": f"upload failed: {r.json()}"}

    # Compile
    r = req("POST", f"{BASE_URL}/compile/create", headers=headers, json={"projectId": PROJECT_ID})
    cr = r.json()
    if not cr.get("success"):
        return {"error": f"compile trigger failed: {cr}"}
    compile_id = cr["compileId"]

    for _ in range(60):
        r    = req("GET", f"{BASE_URL}/compile/read", headers=headers,
                   params={"projectId": PROJECT_ID, "compileId": compile_id})
        data = r.json()
        status = data.get("state") or data.get("status") or data.get("compile", {}).get("status", "")
        if status == "BuildSuccess":
            break
        if status == "BuildError":
            logs = data.get("logs") or data.get("compile", {}).get("logs", [])
            return {"error": f"compile failed: {'; '.join(str(l) for l in logs[:3])}"}
        time.sleep(2)
    else:
        return {"error": "compile timeout"}

    # Create backtest
    r  = req("POST", f"{BASE_URL}/backtests/create", headers=headers,
             json={"projectId": PROJECT_ID, "compileId": compile_id, "backtestName": name})
    br = r.json()
    if not br.get("success"):
        return {"error": f"backtest create failed: {br}"}
    bid = br["backtest"]["backtestId"]

    # Poll
    stat_retries = 0; last_progress = -1; stall_count = 0
    for _ in range(600):
        try:
            r    = req("GET", f"{BASE_URL}/backtests/read", headers=headers,
                       params={"projectId": PROJECT_ID, "backtestId": bid})
            data = r.json()
        except Exception as e:
            time.sleep(5); continue
        if not data.get("success"):
            time.sleep(2); continue
        bt       = data.get("backtest", {})
        status   = bt.get("status", "")
        progress = float(bt.get("progress", 0)) * 100

        if status in ["Completed", "Completed."]:
            stats    = bt.get("statistics", {})
            is_empty = not stats or (stats.get("Total Orders") == "0" and stats.get("Compounding Annual Return") == "0%")
            if is_empty and stat_retries < 15:
                stat_retries += 1; time.sleep(3); continue

            cagr_raw  = stats.get("Compounding Annual Return", "0%")
            maxdd_raw = stats.get("Drawdown", "0%")
            try:
                cagr_val  = float(cagr_raw.strip('%'))
                maxdd_val = abs(float(maxdd_raw.strip('%')))
            except (ValueError, TypeError):
                cagr_val = maxdd_val = 0

            passed = cagr_val >= 28 and maxdd_val <= 58
            result = {
                "backtestId": bid, "status": "completed", "passed": passed,
                "cagr": f"{round(cagr_val)}%", "maxdd": f"-{round(maxdd_val)}%",
                "sharpe": stats.get("Sharpe Ratio", "0"),
                "win_pct": stats.get("Win Rate", "0%"),
                "pl_ratio": stats.get("Profit-Loss Ratio", "0"),
                "orders": stats.get("Total Orders", "0"),
                "cagr_val": cagr_val, "maxdd_val": maxdd_val,
            }
            result["yearly"] = extract_yearly(data)
            return result

        if status in ["Failure", "RuntimeError", "Runtime Error", "Cancelled"]:
            return {"error": f"backtest failed: {status}", "backtestId": bid}

        if progress == last_progress:
            stall_count += 1
        else:
            stall_count = 0
        last_progress = progress
        if stall_count > 30:
            return {"error": f"stalled at {progress:.1f}%", "backtestId": bid}

        sys.stdout.write(f"\r  {name}: {status} ({progress:.1f}%)       ")
        sys.stdout.flush()
        time.sleep(2)
    else:
        return {"error": "backtest timeout", "backtestId": bid}

def extract_yearly(data):
    rolling = data.get("backtest", {}).get("rollingWindow", {})
    if not rolling:
        return {}
    sorted_keys   = sorted(rolling.keys())
    yearly_equity = {}
    for key in sorted_keys:
        if "_" not in key:
            continue
        year   = key.split("_")[1][:4]
        equity = float(rolling[key].get("portfolioStatistics", {}).get("endEquity", 100000))
        yearly_equity[year] = equity

    final    = {}
    prev     = float(rolling[sorted_keys[0]].get("portfolioStatistics", {}).get("startEquity", 100000))
    for y in sorted(yearly_equity):
        final[y] = round((yearly_equity[y] / prev - 1) * 100)
        prev      = yearly_equity[y]
    return final

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    algos_dir  = os.path.join(script_dir, "cc_algos")
    outpath    = os.path.join(script_dir, "backtests", "backtest_cc019.jsonl")

    if len(sys.argv) > 1:
        nums = []
        for arg in sys.argv[1:]:
            if "-" in arg:
                s, e = arg.split("-")
                nums.extend(range(int(s), int(e) + 1))
            else:
                nums.append(int(arg))
    else:
        nums = list(range(1, 101))

    results = {}
    if os.path.exists(outpath):
        with open(outpath) as f:
            for line in f:
                line = line.strip()
                if not line: continue
                obj = json.loads(line)
                sid = obj.pop("id")
                results[sid] = obj
    elif os.path.exists(outpath.replace(".jsonl", ".json")):
        with open(outpath.replace(".jsonl", ".json")) as f:
            results = json.load(f)

    for n in nums:
        key = str(950 + n)
        if key in results and "error" not in results[key] and results[key].get("status") == "completed":
            r  = results[key]
            pf = "✅" if r.get("passed") else "❌"
            print(f"[resume] Skipping cc019_{n:03d} — {pf} CAGR={r['cagr']}, MaxDD={r['maxdd']}")
            continue
        if key in results:
            print(f"[retry] Re-running cc019_{n:03d} ({results[key].get('error','?')})")

        filepath = os.path.join(algos_dir, f"cc019_{n:03d}.py")
        if not os.path.exists(filepath):
            print(f"cc019_{n:03d}: not found, skipping")
            continue

        name = f"CC19_{n:03d}"
        print(f"\n{'='*60}\nRunning cc019_{n:03d}.py\n{'='*60}")
        sys.stdout.flush()

        result       = run_backtest(filepath, name)
        results[key] = result
        if "error" in result:
            print(f"\n  ❌ cc019_{n:03d}: {result['error']}")
        else:
            pf = "✅" if result["passed"] else "❌"
            print(f"\n  {pf} cc019_{n:03d}: CAGR={result['cagr']}, MaxDD={result['maxdd']}, Sharpe={result['sharpe']}")

        with open(outpath, "w") as f:
            for sid, res in results.items():
                f.write(json.dumps({"id": sid, **res}, ensure_ascii=False) + "\n")
        time.sleep(1)

    # Summary
    print("\n\n## Summary")
    print("| # | CAGR | MaxDD | Sharpe | Pass |")
    print("|---|------|-------|--------|------|")
    for n in nums:
        r = results.get(str(950 + n), {})
        if "error" in r:
            print(f"| {n:03d} | ERROR | | | ❌ |")
        elif r.get("status") == "completed":
            pf = "✅" if r.get("passed") else "❌"
            print(f"| {n:03d} | {r['cagr']} | {r['maxdd']} | {r['sharpe']} | {pf} |")

if __name__ == "__main__":
    main()
