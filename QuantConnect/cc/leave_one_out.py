"""
Leave-one-out backtest runner for the ensemble.
For each sub-algo, removes it from ultAlgo.py, bundles, and runs a backtest.
Results saved incrementally to cc/leave_one_out_results.json.
Generates cc/md/ensemble_leave_one_out.md on completion.

Usage:
    python3 cc/leave_one_out.py              # run all 17 leave-one-out + baseline
    python3 cc/leave_one_out.py --table-only  # regenerate md from existing results
"""

import os, sys, re, json, time, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ULTRA_ALGO = os.path.join(ROOT, "cc/cc_algos/ensemble/utils/ultAlgo.py")
BUNDLE_PY  = os.path.join(ROOT, "cc/cc_algos/ensemble/utils/bundle.py")
ENSEMBLE_PY = os.path.join(ROOT, "cc/cc_algos/ensemble/merged/ensemble.py")
RESULTS_PATH = os.path.join(ROOT, "cc/leave_one_out_results.json")
MD_OUT = os.path.join(ROOT, "cc/md/ensemble_leave_one_out.md")

# Map: (catalog_id, class_name, module_name, short_id, display_name)
SUB_ALGOS = [
    ( 1, "LeveragedRebalanceSub",  "leveraged_rebalance", "LevRebal",    "TQQQ 60% Annual Rebalance"),
    ( 2, "RSIDipChampionSub",      "rsi_champion",        "RSIDip",       "QQQ RSI(2) Dip"),
    ( 3, "TQQQDynamicSub",         "tqqq_dynamic",        "TQQQDyn",      "TQQQ Dynamic Sizing"),
    ( 4, "ExpandingBreakoutSub",   "expanding_breakout",  "ExpandBreak",  "TQQQ Expanding Range Breakout"),
    ( 5, "TQQQSMA150Sub",          "tqqq_sma150",         "TQQQSMA150",   "QQQ SMA(150) Trend"),
    ( 6, "IBSATRStopSub",          "ibs_atr_stop",        "IBSATRStop",   "TQQQ IBS Extreme + ATR Stop"),
    ( 8, "ROC20Sub",               "roc20",               "ROC20",        "ROC(20) Zero Cross"),
    ( 9, "UpDay20Sub",             "upday20",             "UpDay20",      "Up-Day Count(20)"),
    (10, "TII20Sub",               "tii20",               "TII20",        "TII(20) Trend Intensity"),
    (11, "Price126DSub",           "price126d",           "Price126D",    "Price 126D Percentile"),
    (12, "TrendStretchExitSub",    "trend_stretch_exit",  "StretchExit",  "Trend Stretch Exit"),
    (13, "AntiMartingaleSub",      "anti_martingale",     "AntiMartin",   "TQQQ Anti-Martingale Pyramid"),
    (14, "Donchian200MidlineSub",  "donchian200_midline", "D200Mid",      "Donchian-200 Midline"),
    (15, "ROCD200TrailSub",        "roc_d200_trail",      "ROCD200Trail", "ROC+D200 + 7% Trail Exit"),
    (16, "TQQQPyramidSub",        "tqqq_pyramid",        "TQQQPyramid",  "TQQQ Pyramid (10%/day)"),
    (17, "RangeExpandedSub",      "range_expanded",      "RangeExp",     "Range Expanded 110%"),
    (18, "MFI14HystSub",          "mfi14_hyst",          "MFI14Hyst",    "MFI14_Hyst"),
]

# Known baseline from ensemble.md
BASELINE = {
    "key": "baseline",
    "name": "Full Ensemble (17 algos)",
    "cagr": 37, "maxdd": 34, "sharpe": 0.978,
    "yearly": {"2014":38,"2015":4,"2016":1,"2017":87,"2018":-3,"2019":59,
               "2020":119,"2021":61,"2022":-19,"2023":85,"2024":47,"2025":36},
}


# ---------------------------------------------------------------------------
# QC API (inlined from batch_runner.py to avoid subprocess overhead)
# ---------------------------------------------------------------------------

import hashlib, base64, requests
from dotenv import load_dotenv

load_dotenv(os.path.join(ROOT, "api/.env"))
USER_ID    = os.environ.get("QC_USER_ID")
API_TOKEN  = os.environ.get("QC_API_TOKEN")
PROJECT_ID = os.environ.get("QC_PROJECT_ID")
BASE_URL   = os.environ.get("QC_BASE_URL", "https://www.quantconnect.com/api/v2")

def auth():
    ts = str(int(time.time()))
    h  = hashlib.sha256(f"{API_TOKEN}:{ts}".encode()).hexdigest()
    b  = base64.b64encode(f"{USER_ID}:{h}".encode()).decode()
    return {"Authorization": f"Basic {b}", "Timestamp": ts}

def cancel_stale():
    try:
        r = requests.get(f"{BASE_URL}/backtests/list", headers=auth(),
                         params={"projectId": PROJECT_ID}, timeout=30)
        for bt in r.json().get("backtests", []):
            st = bt.get("status", "")
            if "Progress" in st or "Queue" in st:
                requests.post(f"{BASE_URL}/backtests/update", headers=auth(),
                              json={"projectId": PROJECT_ID, "backtestId": bt["backtestId"],
                                    "name": bt["name"], "status": "Cancel"}, timeout=30)
    except Exception:
        pass

def run_backtest(filepath, name):
    cancel_stale()
    time.sleep(2)
    with open(filepath) as f:
        content = f.read()

    h = auth()
    r = requests.post(f"{BASE_URL}/files/update", headers=h,
                      json={"projectId": PROJECT_ID, "name": "main.py", "content": content}, timeout=60)
    if not r.json().get("success"):
        return {"error": f"upload failed: {r.json()}"}

    h = auth()
    r = requests.post(f"{BASE_URL}/compile/create", headers=h,
                      json={"projectId": PROJECT_ID}, timeout=60)
    cr = r.json()
    if not cr.get("success"):
        return {"error": f"compile trigger: {cr}"}
    compile_id = cr["compileId"]

    for _ in range(60):
        h = auth()
        r = requests.get(f"{BASE_URL}/compile/read", headers=h,
                         params={"projectId": PROJECT_ID, "compileId": compile_id}, timeout=30)
        data = r.json()
        status = data.get("state") or data.get("status") or data.get("compile", {}).get("status", "")
        if status == "BuildSuccess":
            break
        if status == "BuildError":
            logs = data.get("logs") or data.get("compile", {}).get("logs", [])
            return {"error": f"build error: {'; '.join(str(l) for l in logs[:3])}"}
        time.sleep(2)
    else:
        return {"error": "compile timeout"}

    h = auth()
    r = requests.post(f"{BASE_URL}/backtests/create", headers=h,
                      json={"projectId": PROJECT_ID, "compileId": compile_id, "backtestName": name}, timeout=60)
    br = r.json()
    if not br.get("success"):
        return {"error": f"backtest create: {br}"}
    bid = br["backtest"]["backtestId"]

    stat_retries = 0
    for _ in range(600):
        h = auth()
        r = requests.get(f"{BASE_URL}/backtests/read", headers=h,
                         params={"projectId": PROJECT_ID, "backtestId": bid}, timeout=30)
        data = r.json()
        if not data.get("success"):
            time.sleep(2)
            continue
        bt = data.get("backtest", {})
        status = bt.get("status", "")
        progress = float(bt.get("progress", 0)) * 100

        if status in ["Completed", "Completed."]:
            stats = bt.get("statistics", {})
            if (not stats or stats.get("Compounding Annual Return") == "0%") and stat_retries < 15:
                stat_retries += 1
                time.sleep(3)
                continue

            cagr_val  = float(stats.get("Compounding Annual Return", "0%").strip("%"))
            maxdd_val = abs(float(stats.get("Drawdown", "0%").strip("%")))
            sharpe    = stats.get("Sharpe Ratio", "0")
            yearly    = extract_yearly(data)

            return {
                "backtestId": bid, "status": "completed",
                "cagr": round(cagr_val), "maxdd": round(maxdd_val),
                "sharpe": float(sharpe) if sharpe else 0.0,
                "yearly": yearly,
            }

        if status in ["Failure", "RuntimeError", "Cancelled"]:
            return {"error": f"backtest {status}", "backtestId": bid}

        sys.stdout.write(f"\r  {name}: {progress:.1f}%        ")
        sys.stdout.flush()
        time.sleep(2)

    return {"error": "timeout", "backtestId": bid}


def extract_yearly(data):
    rolling = data.get("backtest", {}).get("rollingWindow", {})
    if not rolling:
        return {}
    sorted_keys = sorted(rolling.keys())
    yearly_equity = {}
    for key in sorted_keys:
        if "_" not in key:
            continue
        year = key.split("_")[1][:4]
        eq = float(rolling[key].get("portfolioStatistics", {}).get("endEquity", 100000))
        yearly_equity[year] = eq
    final = {}
    first = sorted_keys[0]
    prev = float(rolling[first].get("portfolioStatistics", {}).get("startEquity", 100000))
    for y in sorted(yearly_equity):
        final[y] = round(((yearly_equity[y] / prev) - 1) * 100)
        prev = yearly_equity[y]
    return final


# ---------------------------------------------------------------------------
# ultAlgo.py patching
# ---------------------------------------------------------------------------

def make_patched_ultAlgo(orig_src, exclude_class, exclude_module):
    """Returns modified ultAlgo.py content with one sub-algo removed."""
    src = orig_src

    # Remove import line
    src = re.sub(rf"^from {re.escape(exclude_module)} import {re.escape(exclude_class)}\n",
                 "", src, flags=re.MULTILINE)

    # Remove sub_algo instantiation line (handles optional trailing comma and spaces)
    src = re.sub(rf"^\s+{re.escape(exclude_class)}\(self,\s*['\"].*?['\"],?\s*\),?\n",
                 "", src, flags=re.MULTILINE)

    return src


def bundle_ensemble():
    """Run bundle.py to regenerate merged/ensemble.py."""
    import subprocess
    result = subprocess.run(
        ["python3", BUNDLE_PY],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"bundle failed:\n{result.stderr}")


# ---------------------------------------------------------------------------
# Markdown table generation
# ---------------------------------------------------------------------------

def generate_md(results):
    baseline = BASELINE
    yr_cols = [str(2000+i) for i in range(14, 26)]

    lines = []
    lines.append("# Ensemble Leave-One-Out Analysis")
    lines.append("")
    lines.append("*Each row = ensemble with that sub-algo removed. Delta = vs full ensemble.*")
    lines.append("")

    # Summary table
    lines.append("## Summary")
    lines.append("")
    lines.append("| Removed | Name | CAGR | dCAGR | MaxDD | dDD | Sharpe | dSharpe |")
    lines.append("| :-- | :-- | ---: | ---: | ---: | ---: | ---: | ---: |")

    # Baseline row
    bc, bdd, bs = baseline["cagr"], baseline["maxdd"], baseline["sharpe"]
    lines.append(f"| — | **Full Ensemble (baseline)** | **{bc}%** | — | **-{bdd}%** | — | **{bs:.3f}** | — |")

    rows = []
    for sid, cls, mod, short, name in SUB_ALGOS:
        key = f"S{sid:02d}"
        r = results.get(key)
        if not r or "error" in r:
            rows.append((0, key, name, None, None, None))
            continue
        dc = r["cagr"] - bc
        ddd = r["maxdd"] - bdd   # positive = worse (bigger drawdown)
        ds = r["sharpe"] - bs
        rows.append((dc, key, name, r["cagr"], r["maxdd"], r["sharpe"], dc, ddd, ds))

    # Sort by dCAGR descending (removing this algo hurt the most = most valuable)
    rows.sort(key=lambda x: x[0])

    for row in rows:
        key, name = row[1], row[2]
        sid = int(key[1:])
        if len(row) < 7 or row[3] is None:
            lines.append(f"| {key} | {name} | — | — | — | — | — | — |")
            continue
        _, _, _, cagr, maxdd, sharpe, dc, ddd, ds = row
        dc_str  = f"{dc:+d}%"
        ddd_str = f"{ddd:+d}%"
        ds_str  = f"{ds:+.3f}"
        lines.append(f"| {key} | {name} | {cagr}% | {dc_str} | -{maxdd}% | {ddd_str} | {sharpe:.3f} | {ds_str} |")

    lines.append("")

    # Yearly table
    lines.append("## Yearly Returns")
    lines.append("")
    yr_hdr = "| Removed | Name | " + " | ".join(f"'{y[2:]}" for y in yr_cols) + " |"
    yr_sep = "| :-- | :-- | " + " | ".join(":---:" for _ in yr_cols) + " |"
    lines.append(yr_hdr)
    lines.append(yr_sep)

    # Baseline
    byr = baseline["yearly"]
    def fmt(v):
        if v is None: return "—"
        return f"+{v}%" if v > 0 else f"{v}%"
    bl_cells = " | ".join(fmt(byr.get(y)) for y in yr_cols)
    lines.append(f"| — | **Full Ensemble** | {bl_cells} |")

    for row in sorted(rows, key=lambda x: int(x[1][1:])):
        key, name = row[1], row[2]
        r = results.get(key)
        if not r or "error" in r:
            yr_cells = " | ".join("—" for _ in yr_cols)
        else:
            yr = r.get("yearly", {})
            yr_cells = " | ".join(fmt(yr.get(y)) for y in yr_cols)
        lines.append(f"| {key} | {name} | {yr_cells} |")

    lines.append("")

    with open(MD_OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"\nTable written to {MD_OUT}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    table_only = "--table-only" in sys.argv

    # Load existing results
    results = {}
    if os.path.exists(RESULTS_PATH):
        with open(RESULTS_PATH) as f:
            results = json.load(f)

    if table_only:
        generate_md(results)
        return

    orig_ultAlgo = open(ULTRA_ALGO).read()

    try:
        for sid, cls, mod, short, name in SUB_ALGOS:
            key = f"S{sid:02d}"

            if key in results and "error" not in results[key]:
                r = results[key]
                print(f"[skip] {key} {name}: CAGR={r['cagr']}% MaxDD={r['maxdd']}% Sharpe={r['sharpe']:.3f}")
                continue

            print(f"\n{'='*60}")
            print(f"Running: minus {key} ({name})")
            print(f"{'='*60}")

            # Patch ultAlgo.py
            patched = make_patched_ultAlgo(orig_ultAlgo, cls, mod)
            with open(ULTRA_ALGO, "w") as f:
                f.write(patched)

            # Bundle
            bundle_ensemble()

            # Backtest
            result = run_backtest(ENSEMBLE_PY, f"LOO minus {key}")

            if "error" in result:
                print(f"\n  ERROR: {result['error']}")
            else:
                dc = result["cagr"] - BASELINE["cagr"]
                ds = result["sharpe"] - BASELINE["sharpe"]
                print(f"\n  CAGR={result['cagr']}% ({dc:+d}%)  "
                      f"MaxDD={result['maxdd']}%  Sharpe={result['sharpe']:.3f} ({ds:+.3f})")

            results[key] = result

            # Save incrementally
            with open(RESULTS_PATH, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)

            time.sleep(5)

    finally:
        # Always restore original ultAlgo.py
        with open(ULTRA_ALGO, "w") as f:
            f.write(orig_ultAlgo)
        print("\nRestored original ultAlgo.py")

    generate_md(results)


if __name__ == "__main__":
    main()
