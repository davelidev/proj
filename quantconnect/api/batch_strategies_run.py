import os, re, time, json, requests, hashlib, base64
from dotenv import load_dotenv

load_dotenv()

USER_ID    = os.environ.get("QC_USER_ID")
API_TOKEN  = os.environ.get("QC_API_TOKEN")
PROJECT_ID = os.environ.get("QC_PROJECT_ID")
BASE_URL   = os.environ.get("QC_BASE_URL", "https://www.quantconnect.com/api/v2")

STRATEGIES_DIR = "QuantConnect/strategies"
BASE_FILE      = os.path.join(STRATEGIES_DIR, "base.py")
RESULTS_JSON   = "QuantConnect/api/strategies_results.json"
STRATEGIES_MD  = os.path.join(STRATEGIES_DIR, "Strategies.md")
YEARS          = [str(y) for y in range(2014, 2026)]

STRATEGIES = [
    ("vol_breakout.py",        1),
    ("tech_dip.py",            2),
    ("leveraged_rebalance.py", 3),
    ("rsi_champion.py",        4),
    ("tqqq_dynamic.py",        5),
    ("expanding_breakout.py",  6),
]


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def get_headers():
    ts = str(int(time.time()))
    h  = hashlib.sha256(f"{API_TOKEN}:{ts}".encode()).hexdigest()
    a  = base64.b64encode(f"{USER_ID}:{h}".encode()).decode()
    return {"Authorization": f"Basic {a}", "Timestamp": ts}


def bundle(strategy_file):
    """Inline base.py into the sub-algo file to produce a self-contained main.py."""
    with open(BASE_FILE) as f:
        base_content = f.read()
    with open(os.path.join(STRATEGIES_DIR, strategy_file)) as f:
        algo_content = f.read()
    algo_content = algo_content.replace("from base import BaseSubAlgo, _make_standalone\n", "")
    return base_content + "\n\n" + algo_content


def upload_and_run(content, name):
    requests.post(f"{BASE_URL}/files/update", headers=get_headers(),
                  json={"projectId": PROJECT_ID, "name": "main.py", "content": content})
    r = requests.post(f"{BASE_URL}/compile/create", headers=get_headers(),
                      json={"projectId": PROJECT_ID}).json()
    if not r.get("success"):
        print(f"  Compile failed: {r}")
        return None
    time.sleep(3)
    r = requests.post(f"{BASE_URL}/backtests/create", headers=get_headers(),
                      json={"projectId": PROJECT_ID, "compileId": r["compileId"],
                            "backtestName": name}).json()
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


# ---------------------------------------------------------------------------
# Stats extraction
# ---------------------------------------------------------------------------

def extract_stats(res):
    stats = res.get("backtest", {}).get("statistics", {})
    if not stats:
        rw = res.get("backtest", {}).get("rollingWindow", {})
        if rw:
            stats = rw[sorted(rw.keys())[-1]].get("portfolioStatistics", {})

    def pct(k1, k2=None):
        v = stats.get(k1) or (stats.get(k2) if k2 else None)
        if v is None: return None
        v = float(str(v).replace('%', '').strip())
        return v * 100 if abs(v) < 1.0 else v

    def num(k1, k2=None):
        v = stats.get(k1) or (stats.get(k2) if k2 else None)
        if v is None: return None
        try: return float(str(v).replace('%', '').strip())
        except: return None

    cagr   = pct("Compounding Annual Return", "compoundingAnnualReturn")
    maxdd  = pct("Drawdown", "drawdown")
    sharpe = num("Sharpe Ratio", "sharpeRatio")
    total  = int(num("Total Orders", "totalOrders") or 0)
    wr_raw = stats.get("Win Rate") or stats.get("winRate") or "0"
    wr     = float(str(wr_raw).replace('%', '').strip())
    if wr > 1: wr /= 100
    win_n  = round(total * wr)
    loss_n = total - win_n
    wl     = round(win_n / loss_n, 2) if loss_n > 0 else 0
    pl     = num("Profit-Loss Ratio", "profitLossRatio")

    return {"CAGR": cagr, "MaxDD": maxdd, "Sharpe": sharpe,
            "Win": win_n, "Loss": loss_n, "WL": wl, "PL": pl}


def extract_yearly(res):
    rw = res.get("backtest", {}).get("rollingWindow") or {}
    by_year = {}
    for key, val in rw.items():
        if not key.startswith("M1_"): continue
        year = key[3:7]
        by_year.setdefault(year, []).append((key, val))
    result = {}
    for year in YEARS:
        entries = sorted(by_year.get(year, []), key=lambda x: x[0])
        if not entries: continue
        start_eq = float(entries[0][1]["portfolioStatistics"]["startEquity"])
        end_eq   = float(entries[-1][1]["portfolioStatistics"]["endEquity"])
        if start_eq > 0:
            result[year] = round((end_eq / start_eq - 1) * 100)
    return result


# ---------------------------------------------------------------------------
# Strategies.md update
# ---------------------------------------------------------------------------

def fmt_cell(val):
    if val is None: return "⚪ 0%"
    e = "🟢" if val > 0 else ("🔴" if val < 0 else "⚪")
    return f"{e} {val}%"


def update_strategies_md(all_results):
    with open(STRATEGIES_MD) as f:
        lines = f.readlines()

    in_section         = None
    after_stats_sep    = False
    after_yearly_sep   = False
    stats_header_seen  = False
    yearly_header_seen = False

    for i, line in enumerate(lines):

        # ---- Top-level summary table rows ----
        for filename, num in STRATEGIES:
            if filename not in all_results: continue
            r = all_results[filename]
            if r.get("status") != "Completed.": continue
            s  = r["stats"]
            yr = r["yearly"]
            cagr   = f"{s['CAGR']:.0f}%"   if s.get("CAGR")   is not None else "—"
            maxdd  = f"-{abs(s['MaxDD']):.0f}%" if s.get("MaxDD") is not None else "—"
            sharpe = f"{s['Sharpe']:.3f}"   if s.get("Sharpe") is not None else "—"
            win    = str(s.get("Win",  "—"))
            loss   = str(s.get("Loss", "—"))
            wl     = f"{s['WL']:.2f}"       if s.get("WL")     else "—"
            pl     = f"{s['PL']:.2f}"       if s.get("PL")     is not None else "—"

            # Stats summary row  (single space before closing |)
            if re.match(rf'^\| ✅ \[{num}\]\(#strategy-{num}\) \|', line):
                parts   = [p.strip() for p in line.split("|")]
                cat     = parts[2]
                overfit = parts[10] if len(parts) > 10 else "—"
                lines[i] = f"| ✅ [{num}](#strategy-{num}) | {cat} | {cagr} | {maxdd} | {sharpe} | {win} | {loss} | {wl} | {pl} | {overfit} |\n"

            # Yearly summary row (two spaces before closing |)
            elif re.match(rf'^\| ✅ \[{num}\]\(#strategy-{num}\)  \|', line):
                yr_cells = " | ".join(fmt_cell(yr.get(y)) for y in YEARS)
                lines[i] = f"| ✅ [{num}](#strategy-{num})  | {yr_cells} |\n"

        # ---- Per-strategy sections ----
        m = re.match(r'^## Strategy-(\d+)', line)
        if m:
            in_section         = int(m.group(1))
            stats_header_seen  = False
            after_stats_sep    = False
            yearly_header_seen = False
            after_yearly_sep   = False
            continue

        if in_section is None: continue
        fname = next((f for f, n in STRATEGIES if n == in_section), None)
        if not fname or fname not in all_results: continue
        r = all_results[fname]
        if r.get("status") != "Completed.": continue

        s  = r["stats"]
        yr = r["yearly"]
        cagr   = f"{s['CAGR']:.0f}%"       if s.get("CAGR")   is not None else "—"
        maxdd  = f"-{abs(s['MaxDD']):.0f}%" if s.get("MaxDD")  is not None else "—"
        sharpe = f"{s['Sharpe']:.3f}"       if s.get("Sharpe") is not None else "—"
        win    = str(s.get("Win",  "—"))
        loss   = str(s.get("Loss", "—"))
        wl     = f"{s['WL']:.2f}"           if s.get("WL")     else "—"
        pl     = f"{s['PL']:.2f}"           if s.get("PL")     is not None else "—"

        # Stats table header
        if "| CAGR | MaxDD | Sharpe | Win # |" in line:
            stats_header_seen = True
            after_stats_sep   = False
            continue

        if stats_header_seen and line.startswith("| :---"):
            after_stats_sep   = True
            stats_header_seen = False
            continue

        if after_stats_sep:
            lines[i]       = f"| {cagr} | {maxdd} | {sharpe} | {win} | {loss} | {wl} | {pl} |\n"
            after_stats_sep = False
            continue

        # Yearly table header within section
        if re.match(r'^\| 14\s+\| 15\s+\|', line):
            yearly_header_seen = True
            after_yearly_sep   = False
            continue

        if yearly_header_seen and line.startswith("| :---"):
            after_yearly_sep   = True
            yearly_header_seen = False
            continue

        if after_yearly_sep:
            yr_cells         = " | ".join(fmt_cell(yr.get(y)) for y in YEARS)
            lines[i]         = f"| {yr_cells} |\n"
            after_yearly_sep = False
            continue

    with open(STRATEGIES_MD, "w") as f:
        f.writelines(lines)

    print("Strategies.md updated.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    import sys
    only = sys.argv[1] if len(sys.argv) > 1 else None

    results = {}
    if os.path.exists(RESULTS_JSON):
        with open(RESULTS_JSON) as f:
            results = json.load(f)

    for filename, num in STRATEGIES:
        if only and only not in filename:
            continue
        if results.get(filename, {}).get("status") == "Completed.":
            print(f"Skipping Strategy-{num} ({filename}) — cached")
            continue

        print(f"\n--- Strategy-{num}: {filename} ---")
        content = bundle(filename)
        bid = upload_and_run(content, f"Strategy-{num}: {filename}")
        if not bid:
            print("  Could not start backtest")
            continue

        res = poll(bid)
        if not res:
            results[filename] = {"status": "Failed"}
        else:
            raw_stats = res.get("backtest", {}).get("statistics", {})
        results[filename] = {
            "status":    "Completed.",
            "id":        bid,
            "raw_stats": raw_stats,
            "stats":     extract_stats(res),
            "yearly":    extract_yearly(res),
        }

        with open(RESULTS_JSON, "w") as f:
            json.dump(results, f, indent=4)

    print("\n--- Updating Strategies.md ---")
    update_strategies_md(results)
    print("Done.")


if __name__ == "__main__":
    main()
