"""Batch runner for cc/algos3/ — runs backtests and collects results."""
import os, sys, time, json, hashlib, base64, requests
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "api", ".env")
load_dotenv(dotenv_path)

USER_ID = os.environ.get("QC_USER_ID")
API_TOKEN = os.environ.get("QC_API_TOKEN")
PROJECT_ID = os.environ.get("QC_PROJECT_ID")
BASE_URL = os.environ.get("QC_BASE_URL", "https://www.quantconnect.com/api/v2")
TIMEOUT = 60

def get_auth_headers():
    timestamp = str(int(time.time()))
    token_hash = hashlib.sha256(f"{API_TOKEN}:{timestamp}".encode()).hexdigest()
    auth_64 = base64.b64encode(f"{USER_ID}:{token_hash}".encode()).decode()
    return {"Authorization": f"Basic {auth_64}", "Timestamp": timestamp}

def req(method, url, **kwargs):
    kwargs.setdefault("timeout", TIMEOUT)
    return requests.request(method, url, **kwargs)

def cancel_running_backtests(headers):
    """Cancel any in-progress backtests to free a cluster node."""
    try:
        r = req("GET", f"{BASE_URL}/backtests/list", headers=headers,
                params={"projectId": PROJECT_ID})
        data = r.json()
        for bt in data.get("backtests", []):
            status = bt.get("status", "")
            if "Progress" in status or "Queue" in status:
                bid = bt["backtestId"]
                req("POST", f"{BASE_URL}/backtests/update", headers=headers,
                    json={"projectId": PROJECT_ID, "backtestId": bid,
                          "name": bt["name"], "status": "Cancel"})
                print(f"  [cleanup] Cancelled stale backtest: {bt['name']} ({bid[:16]}...)")
    except Exception as e:
        print(f"  [cleanup] Warning: could not cancel stale backtests: {e}")

def run_backtest(filepath, name):
    headers = get_auth_headers()

    # Free a node before starting
    cancel_running_backtests(headers)
    time.sleep(2)

    with open(filepath, "r") as f:
        content = f.read()

    # 1. Upload
    try:
        r = req("POST", f"{BASE_URL}/files/update", headers=headers,
                json={"projectId": PROJECT_ID, "name": "main.py", "content": content})
    except Exception as e:
        return {"error": f"upload request failed: {e}"}
    if not r.json().get("success"):
        return {"error": f"upload failed: {r.json()}"}

    # 2. Compile
    try:
        r = req("POST", f"{BASE_URL}/compile/create", headers=headers,
                json={"projectId": PROJECT_ID})
    except Exception as e:
        return {"error": f"compile trigger failed: {e}"}
    cr = r.json()
    if not cr.get("success"):
        return {"error": f"compile trigger failed: {cr}"}
    compile_id = cr["compileId"]

    for _ in range(60):
        try:
            r = req("GET", f"{BASE_URL}/compile/read", headers=headers,
                    params={"projectId": PROJECT_ID, "compileId": compile_id})
        except Exception as e:
            time.sleep(2)
            continue
        data = r.json()
        status = data.get("state") or data.get("status") or data.get("compile", {}).get("status", "")
        if status == "BuildSuccess":
            break
        if status == "BuildError":
            logs = data.get("logs") or data.get("compile", {}).get("logs", [])
            return {"error": f"compile failed: {'; '.join(logs[:3])}"}
        time.sleep(2)
    else:
        return {"error": "compile timeout"}

    # 3. Create backtest
    try:
        r = req("POST", f"{BASE_URL}/backtests/create", headers=headers,
                json={"projectId": PROJECT_ID, "compileId": compile_id, "backtestName": name})
    except Exception as e:
        return {"error": f"backtest create failed: {e}"}
    br = r.json()
    if not br.get("success"):
        return {"error": f"backtest create failed: {br}"}
    bid = br["backtest"]["backtestId"]

    # 4. Poll until complete
    stat_retries = 0
    last_progress = -1
    stall_count = 0
    for _ in range(600):
        try:
            r = req("GET", f"{BASE_URL}/backtests/read", headers=headers,
                    params={"projectId": PROJECT_ID, "backtestId": bid})
        except Exception as e:
            print(f"\n  [!] request error: {e}, retrying...")
            time.sleep(5)
            continue
        data = r.json()
        if not data.get("success"):
            time.sleep(2)
            continue
        bt = data.get("backtest", {})
        status = bt.get("status", "")
        progress = float(bt.get("progress", 0)) * 100

        if status in ["Completed", "Completed."]:
            stats = bt.get("statistics", {})
            is_empty = not stats or (stats.get("Total Orders") == "0" and stats.get("Compounding Annual Return") == "0%")
            if is_empty and stat_retries < 15:
                stat_retries += 1
                time.sleep(3)
                continue

            cagr_raw = stats.get("Compounding Annual Return", "0%")
            max_dd_raw = stats.get("Drawdown", "0%")
            try:
                cagr_val = float(cagr_raw.strip('%'))
                max_dd_val = abs(float(max_dd_raw.strip('%')))
            except (ValueError, TypeError):
                cagr_val = max_dd_val = 0

            passed = cagr_val >= 28 and max_dd_val <= 58

            result = {
                "backtestId": bid,
                "status": "completed",
                "passed": passed,
                "cagr": f"{round(cagr_val)}%",
                "maxdd": f"-{round(max_dd_val)}%",
                "sharpe": stats.get("Sharpe Ratio", "0"),
                "win_pct": stats.get("Win Rate", "0%"),
                "pl_ratio": stats.get("Profit-Loss Ratio", "0"),
                "orders": stats.get("Total Orders", "0"),
                "cagr_val": cagr_val,
                "maxdd_val": max_dd_val,
            }

            yearly = extract_yearly(data)
            result["yearly"] = yearly
            return result

        if status in ["Failure", "RuntimeError", "Runtime Error", "Cancelled"]:
            return {"error": f"backtest failed: {status}", "backtestId": bid}

        # Detect stalls
        if progress == last_progress:
            stall_count += 1
        else:
            stall_count = 0
        last_progress = progress

        if stall_count > 30:
            return {"error": f"stalled at {progress:.1f}% for {stall_count * 2}s", "backtestId": bid}

        sys.stdout.write(f"\r  {name}: {status} ({progress:.1f}%)       ")
        sys.stdout.flush()
        time.sleep(2)
    else:
        return {"error": "backtest timeout", "backtestId": bid}

def extract_yearly(data):
    rolling = data.get("backtest", {}).get("rollingWindow", {})
    if not rolling:
        return {}
    sorted_keys = sorted(rolling.keys())
    yearly_equity = {}
    for key in sorted_keys:
        if "_" not in key:
            continue
        parts = key.split("_")
        if len(parts) < 2:
            continue
        year = parts[1][:4]
        equity = float(rolling[key].get("portfolioStatistics", {}).get("endEquity", 100000))
        yearly_equity[year] = equity

    final = {}
    first_key = sorted_keys[0]
    prev = float(rolling[first_key].get("portfolioStatistics", {}).get("startEquity", 100000))
    for y in sorted(yearly_equity.keys()):
        val = (yearly_equity[y] / prev) - 1
        final[y] = round(val * 100)
        prev = yearly_equity[y]
    return final

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    algos_dir = os.path.join(script_dir, "algos3")
    outpath = os.path.join(script_dir, "results3.json")

    if len(sys.argv) > 1:
        nums = []
        for arg in sys.argv[1:]:
            if "-" in arg:
                s, e = arg.split("-")
                nums.extend(range(int(s), int(e) + 1))
            else:
                nums.append(int(arg))
    else:
        nums = list(range(31, 61))

    # Load existing results (resume support)
    results = {}
    if os.path.exists(outpath):
        with open(outpath) as f:
            results = json.load(f)

    for n in nums:
        key = str(n)
        # Skip if already completed successfully
        if key in results and "error" not in results[key] and results[key].get("status") == "completed":
            r = results[key]
            pf = "✅" if r.get("passed") else "❌"
            print(f"[resume] Skipping Algo{n:03d} — {pf} CAGR={r['cagr']}, MaxDD={r['maxdd']}, Sharpe={r['sharpe']}")
            continue
        # Re-run if errored
        if key in results:
            print(f"[retry] Re-running Algo{n:03d} (previous: {results[key].get('error', 'unknown error')})")

        filepath = os.path.join(algos_dir, f"algo_{n:03d}.py")
        if not os.path.exists(filepath):
            print(f"\n{algo_}{n:03d}: file not found, skipping")
            continue
        name = f"Algo{n:03d}"
        print(f"\n{'='*60}")
        print(f"Running {name} ({filepath})")
        print(f"{'='*60}")
        sys.stdout.flush()
        result = run_backtest(filepath, name)
        results[key] = result
        if "error" in result:
            print(f"\n  ❌ {name}: {result['error']}")
        else:
            pf = "✅" if result["passed"] else "❌"
            print(f"\n  {pf} {name}: CAGR={result['cagr']}, MaxDD={result['maxdd']}, Sharpe={result['sharpe']}")

        # Save incrementally
        with open(outpath, "w") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        time.sleep(1)

    print(f"\n\nResults saved to: {outpath}")

    # Print summary table
    print("\n\n## Summary Table")
    print("| # | Name | CAGR | MaxDD | Sharpe | Orders | Win % | P/L | Pass |")
    print("|---|------|------|-------|--------|--------|-------|-----|------|")
    for n in nums:
        result = results.get(str(n), {})
        n_str = f"{n:03d}"
        if "error" in result:
            print(f"| {n_str} | Algo{n_str} | ERROR | | | | | | ❌ |")
        elif result.get("status") == "completed":
            print(f"| {n_str} | Algo{n_str} | {result['cagr']} | {result['maxdd']} | {result['sharpe']} | {result['orders']} | {result['win_pct']} | {result['pl_ratio']} | {'✅' if result['passed'] else '❌'} |")
        else:
            print(f"| {n_str} | Algo{n_str} | PENDING | | | | | | |")

if __name__ == "__main__":
    main()
