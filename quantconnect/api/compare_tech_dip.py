import os, time, json, hashlib, base64, requests
from dotenv import load_dotenv

load_dotenv()
USER_ID    = os.environ.get("QC_USER_ID")
API_TOKEN  = os.environ.get("QC_API_TOKEN")
PROJECT_ID = os.environ.get("QC_PROJECT_ID")
BASE_URL   = os.environ.get("QC_BASE_URL", "https://www.quantconnect.com/api/v2")

STRATEGIES_DIR = "QuantConnect/strategies"
BASE_FILE      = os.path.join(STRATEGIES_DIR, "base.py")


def get_headers():
    ts = str(int(time.time()))
    h  = hashlib.sha256(f"{API_TOKEN}:{ts}".encode()).hexdigest()
    a  = base64.b64encode(f"{USER_ID}:{h}".encode()).decode()
    return {"Authorization": f"Basic {a}", "Timestamp": ts}


def bundle(strategy_file):
    with open(BASE_FILE) as f:
        base_content = f.read()
    with open(os.path.join(STRATEGIES_DIR, strategy_file)) as f:
        algo_content = f.read()
    algo_content = algo_content.replace("from base import BaseSubAlgo, _make_standalone\n", "")
    return base_content + "\n\n" + algo_content


def run_backtest(content, name):
    requests.post(f"{BASE_URL}/files/update", headers=get_headers(),
                  json={"projectId": PROJECT_ID, "name": "main.py", "content": content})
    time.sleep(2)
    r = requests.post(f"{BASE_URL}/compile/create", headers=get_headers(),
                      json={"projectId": PROJECT_ID}).json()
    if not r.get("success"):
        print(f"  Compile failed: {r}")
        return None
    compile_id = r["compileId"]
    time.sleep(5)
    r = requests.post(f"{BASE_URL}/backtests/create", headers=get_headers(),
                      json={"projectId": PROJECT_ID, "compileId": compile_id,
                            "backtestName": name}).json()
    if not r.get("backtest", {}).get("backtestId"):
        print(f"  Backtest create failed: {r}")
    return r.get("backtest", {}).get("backtestId")


def poll(bid):
    while True:
        res = requests.get(f"{BASE_URL}/backtests/read", headers=get_headers(),
                           params={"projectId": PROJECT_ID, "backtestId": bid}).json()
        status   = res.get("backtest", {}).get("status", "")
        progress = float(res.get("backtest", {}).get("progress", 0)) * 100
        print(f"  {status} {progress:.0f}%  ", end="\r")
        if status == "Completed.":
            print()
            return res
        if status in ("Failure", "RuntimeError", "Cancelled"):
            print(f"\n  Failed: {status}")
            return None
        time.sleep(10)


def get_trades(res):
    bt     = res.get("backtest", {})
    stats  = bt.get("statistics", {})
    tp     = bt.get("totalPerformance", {}) or {}
    if tp:
        print(f"  totalPerformance keys: {list(tp.keys())}")
    trades = tp.get("closedTrades", []) or []
    # Also check orders in runtimeStatistics
    rt = bt.get("runtimeStatistics", {}) or {}
    return trades, stats, rt



def main():
    print("--- Running ORIGINAL (tech_dip_orig.py) ---")
    orig_content = bundle("tech_dip_orig.py")
    bid_orig = run_backtest(orig_content, "TechDip-Original")
    if not bid_orig:
        print("Failed to start original")
        return
    res_orig = poll(bid_orig)

    print("--- Running SUB-ALGO (tech_dip_sub.py) ---")
    sub_content = bundle("tech_dip_sub.py")
    bid_sub = run_backtest(sub_content, "TechDip-SubAlgo")
    if not bid_sub:
        print("Failed to start sub-algo")
        return
    res_sub = poll(bid_sub)

    trades_orig, stats_orig, rt_orig = get_trades(res_orig)
    trades_sub,  stats_sub,  rt_sub  = get_trades(res_sub)

    print(f"\n{'':20} {'ORIGINAL':>12} {'SUB-ALGO':>12}")
    print(f"{'CAGR':20} {stats_orig.get('Compounding Annual Return','?'):>12} {stats_sub.get('Compounding Annual Return','?'):>12}")
    print(f"{'Total Orders':20} {stats_orig.get('Total Orders','?'):>12} {stats_sub.get('Total Orders','?'):>12}")
    print(f"{'Win Rate':20} {stats_orig.get('Win Rate','?'):>12} {stats_sub.get('Win Rate','?'):>12}")
    print(f"{'Sharpe':20} {stats_orig.get('Sharpe Ratio','?'):>12} {stats_sub.get('Sharpe Ratio','?'):>12}")
    print(f"\nClosed trades — original: {len(trades_orig)}, sub-algo: {len(trades_sub)}")

    def fmt_trade(t):
        sym   = t.get("Symbol", {}).get("Value", "?") if isinstance(t.get("Symbol"), dict) else t.get("Symbol", "?")
        entry = t.get("EntryTime", "")[:10]
        exit_ = t.get("ExitTime",  "")[:10]
        pnl   = t.get("ProfitLoss", 0)
        return f"{entry} -> {exit_} {sym:6} pnl={pnl:+.0f}"

    orig_strs = [fmt_trade(t) for t in trades_orig]
    sub_strs  = [fmt_trade(t) for t in trades_sub]
    orig_set  = set(orig_strs)
    sub_set   = set(sub_strs)

    only_orig = sorted(orig_set - sub_set)
    only_sub  = sorted(sub_set  - orig_set)
    print(f"Common: {len(orig_set & sub_set)}  Only-orig: {len(only_orig)}  Only-sub: {len(only_sub)}")
    print(f"\nOnly in ORIGINAL ({len(only_orig)}):")
    for t in only_orig[:30]: print(f"  {t}")
    print(f"\nOnly in SUB-ALGO ({len(only_sub)}):")
    for t in only_sub[:30]: print(f"  {t}")

    with open("QuantConnect/api/tech_dip_comparison.json", "w") as f:
        json.dump({"orig_id": bid_orig, "sub_id": bid_sub,
                   "orig_trades": trades_orig, "sub_trades": trades_sub,
                   "orig_stats": stats_orig, "sub_stats": stats_sub}, f, indent=2)
    print("\nFull comparison saved to tech_dip_comparison.json")


if __name__ == "__main__":
    main()
