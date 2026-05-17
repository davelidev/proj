#!/usr/bin/env python3
"""
Generate cc<N>.md from cc<N>.json + backtest_cc<N>.json.
If backtest_cc<N>.json is missing, runs backtests via QuantConnect API first.

Usage:
    python3 cc/generate_md.py json/cc3.json            # json/cc3.json → md/cc3.md
    python3 cc/generate_md.py json/cc3.json --skip-bt  # skip backtests, md only
    python3 cc/generate_md.py                          # defaults to json/cc1.json
"""

import os, sys, json, time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJ_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)
sys.path.insert(0, os.path.join(PROJ_ROOT, "api"))


def load_json(path):
    with open(path) as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def resolve_paths(cc_json_path):
    base = os.path.splitext(os.path.basename(cc_json_path))[0]
    backtest_path = os.path.join(SCRIPT_DIR, "backtests", f"backtest_{base}.json")
    md_path = os.path.join(SCRIPT_DIR, "md", f"{base}.md")
    return backtest_path, md_path


def run_missing_backtests(strategies, backtest_path, md_path=None):
    """Run backtests for strategies that lack results. Saves incrementally.

    If md_path is provided, regenerate the markdown after each completed
    backtest so cc<N>.md reflects live progress.
    """
    from batch_runner import run_backtest

    existing = {}
    if os.path.exists(backtest_path):
        existing = load_json(backtest_path)

    results = dict(existing)
    ran_any = False

    def _regen_md():
        if md_path:
            try:
                generate_markdown(strategies, results, md_path)
            except Exception as e:
                print(f"  [warn] live md regen failed: {e}")

    _regen_md()  # initial render with whatever results exist

    for sid, meta in strategies.items():
        key = str(sid)

        # Skip if already completed
        if key in results and "error" not in results[key] and results[key].get("status") == "completed":
            continue

        # Skip if no file to run
        file_name = meta.get("file")
        algo_dir = meta.get("algo_dir")
        if not file_name or not algo_dir:
            continue
        filepath = os.path.join(SCRIPT_DIR, algo_dir, file_name)
        if not os.path.exists(filepath):
            results[key] = {"error": f"file not found: {filepath}"}
            save_json(backtest_path, results)
            _regen_md()
            continue

        name = f"Strategy-{sid}"
        print(f"\n{'='*60}")
        print(f"Running {name} ({filepath})")
        print(f"{'='*60}")
        sys.stdout.flush()

        time.sleep(5)  # avoid QC rate limits
        result = run_backtest(filepath, name)
        results[key] = result
        ran_any = True

        if "error" in result:
            print(f"  [ERROR] {name}: {result['error']}")
        else:
            pf = "PASS" if result.get("passed") else "FAIL"
            print(f"  [{pf}] {name}: CAGR={result.get('cagr')}, MaxDD={result.get('maxdd')}")

        save_json(backtest_path, results)
        _regen_md()
        time.sleep(1)

    if ran_any:
        print(f"\nBacktest results saved to: {backtest_path}")
    return results


def derive_trade_stats(bt):
    """Compute win_count / loss_count / wl_ratio / profit_ratio from a backtest
    result dict. Returns dict of strings (or '—' if data unavailable).

    Logic verified against the historical cc1.json stats block:
      orders=2654, win_pct=38% → win=1009, loss=1645, wl=0.61, pl=2.14
    """
    out = {"win_count": "—", "loss_count": "—", "wl_ratio": "—", "profit_ratio": "—"}
    if not bt or "error" in bt:
        return out

    orders_raw = bt.get("orders")
    win_pct_raw = bt.get("win_pct")
    try:
        orders = int(str(orders_raw).replace(",", ""))
        win_pct = float(str(win_pct_raw).rstrip("%"))
    except (TypeError, ValueError):
        # No orders/win_pct data — leave profit_ratio as-is from QC if present.
        pl = bt.get("pl_ratio")
        if pl not in (None, "", "0"):
            out["profit_ratio"] = str(pl)
        return out

    wins   = round(orders * win_pct / 100.0)
    losses = orders - wins
    out["win_count"]  = str(wins)
    out["loss_count"] = str(losses)
    out["wl_ratio"]   = "—" if losses == 0 else f"{wins / losses:.2f}"

    # QC reports pl_ratio="0" when there are no losing trades (division by zero).
    # Only surface a real ratio.
    pl = bt.get("pl_ratio")
    if pl not in (None, "", "0") and losses > 0:
        out["profit_ratio"] = str(pl)
    return out


def _is_displayable(meta, r):
    """Show a strategy in the markdown if it passes the cutoff, or fails very narrowly
    while still having an extremely low drawdown (<= 30%)."""
    if not r or "error" in r:
        return False
    cagr_val = r.get("cagr_val", 0) or 0
    maxdd_val = r.get("maxdd_val", 0) or 0
    if cagr_val >= 28 and maxdd_val <= 58:
        return True
    # near-miss with very low DD: at least 22% CAGR AND <=30% DD
    if cagr_val >= 22 and maxdd_val <= 30:
        return True
    return False


def generate_markdown(strategies, backtest_results, output_path):
    """Generate cc<N>.md from strategy metadata + backtest results."""
    all_ordered = sorted(strategies.items(), key=lambda x: int(x[0]))
    ordered = [(sid, meta) for sid, meta in all_ordered
               if _is_displayable(meta, backtest_results.get(sid, {}))]
    lines = []

    # --- Header ---
    lines.append("# Archived Strategy Backtests")
    lines.append("")
    lines.append("*Strategies removed from active tracking if: CAGR < 28%, MaxDD > 58%, or Overfit ≥ 8/10.*")
    lines.append("")

    # --- Summary Table ---
    H = "| #                    | Pass | Category        | CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio | Overfit |"
    S = "| :------------------- | :--- | :-------------- | :--- | :---- | :----- | :---- | :----- | :-------- | :----------- | :------ |"
    lines.append(H)
    lines.append(S)

    for sid, meta in ordered:
        r = backtest_results.get(sid, {})
        cagr = r.get("cagr", "—")
        maxdd = r.get("maxdd", "—")
        sharpe = r.get("sharpe", "—")
        overfit = meta.get("overfit", "—")

        # Trade-count stats derived from backtest results (was previously stored
        # in cc<N>.json meta.stats; moved here so the columns auto-refresh).
        stats = derive_trade_stats(r)
        win_count = stats["win_count"]
        loss_count = stats["loss_count"]
        wl_ratio = stats["wl_ratio"]
        profit_ratio = stats["profit_ratio"]

        # Pass/fail status — dedicated column rather than icon-prefixed link.
        # An "error" entry (e.g. missing source file) shows "—", not a failure.
        cagr_val = r.get("cagr_val", 0) or 0
        maxdd_val = r.get("maxdd_val", 0) or 0
        if not r or "error" in r:
            pass_cell = "—"
        elif cagr_val >= 28 and maxdd_val <= 58:
            pass_cell = "✅"
        else:
            pass_cell = "❌"

        link = f"[{sid}](#strategy-{sid})"
        row = f"| {link:<20} | {pass_cell:<4} | {meta.get('category', '—'):<15} | {cagr:<4} | {maxdd:<5} | {sharpe:<6} | {win_count:<5} | {loss_count:<5} | {wl_ratio:<8} | {profit_ratio:<12} | {overfit:<6} |"
        lines.append(row)

    lines.append("")
    lines.append("")
    lines.append("---")

    # --- Detail Sections ---
    years = list(range(2014, 2026))
    year_labels = [str(y)[2:] for y in years]

    for sid, meta in ordered:
        r = backtest_results.get(sid, {})
        lines.append(f"## Strategy-{sid}")

        name = meta.get("name", f"Strategy {sid}")
        lines.append(f"### {name}")
        lines.append("")

        desc = meta.get("description", "")
        if desc:
            lines.append(f"**Description:** {desc}")
            lines.append("")

        overfit_notes = meta.get("overfit_notes", "")
        if overfit_notes:
            lines.append(f"*Overfit {meta.get('overfit', '—')} — {overfit_notes}*")
            lines.append("")

        # Strategy rules
        rules = meta.get("rules", [])
        for rule in rules:
            if isinstance(rule, dict):
                lines.append(f"- **{rule['label']}:** {rule['text']}")
            else:
                lines.append(f"- {rule}")
        if rules:
            lines.append("")

        # Stats table — everything derived from the backtest result now
        stats = derive_trade_stats(r)
        cagr = r.get("cagr", "—")
        maxdd = r.get("maxdd", "—")
        sharpe = r.get("sharpe", "—")
        win_count = stats["win_count"]
        loss_count = stats["loss_count"]
        wl_ratio = stats["wl_ratio"]
        profit_ratio = stats["profit_ratio"]

        lines.append("| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |")
        lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
        lines.append(f"| {cagr} | {maxdd} | {sharpe} | {win_count} | {loss_count} | {wl_ratio} | {profit_ratio} |")
        lines.append("")

        # Yearly returns table
        yearly = r.get("yearly", {})
        lines.append("| " + " | ".join(year_labels) + " |")
        lines.append("| " + " | ".join([":---" for _ in year_labels]) + " |")

        yearly_cells = []
        for y in years:
            val = yearly.get(str(y))
            if val is not None:
                try:
                    v = int(val)
                    color = "🟢" if v > 0 else ("🔴" if v < 0 else "⚪")
                except (ValueError, TypeError):
                    color = "⚪"
                yearly_cells.append(f"{color} {val}%")
            else:
                yearly_cells.append("—")
        lines.append("| " + " | ".join(yearly_cells) + " |")
        lines.append("")

        # Code embed
        vault_path = meta.get("vault_path", "")
        if not vault_path:
            algo_dir = meta.get("algo_dir", "algos1")
            file_name = meta.get("file", "")
            if file_name:
                vault_path = f"vault://QuantConnect/cc/{algo_dir}/{file_name}"

        if vault_path:
            display_name = vault_path.rsplit("/", 1)[-1]
            lines.append(f"> [!code]- Click to view: {display_name}")
            lines.append("> ```embed-python")
            lines.append(f'> PATH: "{vault_path}"')
            lines.append("> ```")
            lines.append("")

        lines.append("")
        lines.append("---")
        lines.append("")

    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    print(f"Markdown generated: {output_path}")


def main():
    cc_json_path = None
    skip_bt = False
    for a in sys.argv[1:]:
        if a == "--skip-bt":
            skip_bt = True
        else:
            cc_json_path = a

    if not cc_json_path:
        cc_json_path = os.path.join(SCRIPT_DIR, "json", "cc1.json")

    if not os.path.exists(cc_json_path):
        print(f"Error: {cc_json_path} not found")
        sys.exit(1)

    backtest_path, md_path = resolve_paths(cc_json_path)

    data = load_json(cc_json_path)
    strategies = data.get("strategies", {})
    if not strategies:
        print("Error: no 'strategies' key found in JSON")
        sys.exit(1)

    if skip_bt:
        backtest_results = load_json(backtest_path) if os.path.exists(backtest_path) else {}
    else:
        backtest_results = run_missing_backtests(strategies, backtest_path, md_path=md_path)

    generate_markdown(strategies, backtest_results, md_path)


if __name__ == "__main__":
    main()
