#!/usr/bin/env python3
"""
Generate <batch>.md from <catalog>.jsonl + backtest_cc<NNN>.jsonl.

Usage:
    python3 cc/generate_md.py cc/json/cc005.jsonl            # md only if --skip-bt
    python3 cc/generate_md.py cc/json/ensemble.jsonl --skip-bt
    python3 cc/generate_md.py                                # defaults to strategies.jsonl
"""

import argparse, os, sys, json, time

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
PROJ_ROOT   = os.path.dirname(SCRIPT_DIR)
CONFIG_PATH = os.path.join(SCRIPT_DIR, "json", "config.json")

sys.path.insert(0, SCRIPT_DIR)
sys.path.insert(0, os.path.join(PROJ_ROOT, "api"))


# ---------------------------------------------------------------------------
# Config helpers
# ---------------------------------------------------------------------------

def _load_cfg():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {}


def _get_folder(catalog_name, cfg):
    """Map a catalog stem (e.g. 'cc005', 'ensemble', 'strategies') to its folder."""
    files = cfg.get("files", [])
    try:
        n = int(catalog_name[2:])
        if 0 <= n < len(files):
            return files[n]
    except (ValueError, TypeError):
        pass
    for key, val in cfg.items():
        if isinstance(val, dict) and val.get("catalog") == catalog_name:
            return key
    return catalog_name


def _get_batch_id(folder, cfg):
    """Return ccNNN for a folder name (e.g. 'ensemble' → 'cc000')."""
    files = cfg.get("files", [])
    try:
        return f"cc{files.index(folder):03d}"
    except ValueError:
        return folder


def load_batch_config(catalog_name):
    """Merge global + per-folder config. Returns dict with '_folder' key."""
    cfg    = _load_cfg()
    folder = _get_folder(catalog_name, cfg)
    out    = dict(cfg.get("global", {}))
    out.update(cfg.get(folder, {}))
    out["_folder"] = folder
    return out


# ---------------------------------------------------------------------------
# I/O
# ---------------------------------------------------------------------------

def load_jsonl(path):
    """Return (metadata_dict, strategies_dict keyed by id)."""
    metadata   = {}
    strategies = {}
    with open(path) as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)
            if obj.get("type") == "metadata":
                metadata = obj
            elif obj.get("type") == "strategy":
                sid = obj.pop("id")
                strategies[sid] = obj
    return metadata, strategies


def load_backtest(path):
    """Load backtest results from .jsonl or .json. Returns dict keyed by id."""
    jsonl = path if path.endswith(".jsonl") else path.replace(".json", ".jsonl")
    json_ = path if path.endswith(".json")  else path.replace(".jsonl", ".json")
    if os.path.exists(jsonl):
        results = {}
        with open(jsonl) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                obj = json.loads(line)
                results[obj.pop("id")] = obj
        return results
    if os.path.exists(json_):
        with open(json_) as f:
            return json.load(f)
    return {}


def save_backtest(path, results):
    out = path if path.endswith(".jsonl") else path.replace(".json", ".jsonl")
    with open(out, "w") as f:
        for sid, res in results.items():
            f.write(json.dumps({"id": sid, **res}, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Backtest runner
# ---------------------------------------------------------------------------

def run_missing_backtests(strategies, backtest_path, md_path=None, show_all=False, batch_cfg=None):
    from batch_runner import run_backtest

    results = dict(load_backtest(backtest_path))

    def _regen():
        if md_path:
            try:
                generate_markdown(strategies, results, md_path, show_all, batch_cfg)
            except Exception as e:
                print(f"  [warn] live md regen failed: {e}")

    _regen()

    for sid, meta in strategies.items():
        if sid in results and "error" not in results[sid] and results[sid].get("status") == "completed":
            continue
        file_name = meta.get("file")
        algo_dir  = meta.get("algo_dir")
        if not file_name or not algo_dir:
            continue
        filepath = os.path.join(SCRIPT_DIR, algo_dir, file_name)
        if not os.path.exists(filepath):
            results[sid] = {"error": f"file not found: {filepath}"}
            save_backtest(backtest_path, results)
            _regen()
            continue

        name = f"Strategy-{sid}"
        print(f"\n{'='*60}\nRunning {name} ({filepath})\n{'='*60}")
        sys.stdout.flush()

        time.sleep(5)
        result = run_backtest(filepath, name)
        results[sid] = result

        if "error" in result:
            print(f"  [ERROR] {name}: {result['error']}")
        else:
            pf = "PASS" if result.get("passed") else "FAIL"
            print(f"  [{pf}] {name}: CAGR={result.get('cagr')}, MaxDD={result.get('maxdd')}")

        save_backtest(backtest_path, results)
        _regen()
        time.sleep(1)

    return results


# ---------------------------------------------------------------------------
# Markdown generation
# ---------------------------------------------------------------------------

def _derive_trade_stats(bt):
    out = {"win_count": "—", "loss_count": "—", "wl_ratio": "—", "profit_ratio": "—"}
    if not bt or "error" in bt:
        return out
    try:
        orders  = int(str(bt.get("orders", "")).replace(",", ""))
        win_pct = float(str(bt.get("win_pct", "")).rstrip("%"))
    except (TypeError, ValueError):
        pl = bt.get("pl_ratio")
        if pl not in (None, "", "0"):
            out["profit_ratio"] = str(pl)
        return out

    wins   = round(orders * win_pct / 100.0)
    losses = orders - wins
    out["win_count"]  = str(wins)
    out["loss_count"] = str(losses)
    out["wl_ratio"]   = "—" if losses == 0 else f"{wins / losses:.2f}"
    pl = bt.get("pl_ratio")
    if pl not in (None, "", "0") and losses > 0:
        out["profit_ratio"] = str(pl)
    return out


def _is_displayable(r, show_all):
    if not r or "error" in r or r.get("status") != "completed":
        return False
    if show_all:
        return True
    cagr  = r.get("cagr_val", 0) or 0
    maxdd = r.get("maxdd_val", 0) or 0
    return (cagr >= 28 and maxdd <= 58) or (cagr >= 22 and maxdd <= 30)


def generate_markdown(strategies, backtest_results, output_path, show_all=False, batch_cfg=None):
    batch_cfg  = batch_cfg or {}
    all_rows   = sorted(strategies.items(), key=lambda x: int(x[0]))
    visible    = [(sid, meta) for sid, meta in all_rows
                  if _is_displayable(backtest_results.get(sid, {}), show_all)]
    lines      = []
    years      = list(range(2014, 2026))
    year_labels = [str(y)[2:] for y in years]

    title = batch_cfg.get("name", batch_cfg.get("_folder", "Archived Strategy Backtests"))
    lines += [f"# {title}", ""]
    if not show_all:
        lines += ["*Strategies removed from active tracking if: CAGR < 28%, MaxDD > 58%, or Overfit ≥ 8/10.*", ""]

    # Summary table — # uses row position, not id
    lines.append("| #                    | Pass | Category        | CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio | Overfit |")
    lines.append("| :------------------- | :--- | :-------------- | :--- | :---- | :----- | :---- | :----- | :-------- | :----------- | :------ |")
    for row_num, (sid, meta) in enumerate(visible, 1):
        r      = backtest_results.get(sid, {})
        stats  = _derive_trade_stats(r)
        cagr   = r.get("cagr_val", 0) or 0
        maxdd  = r.get("maxdd_val", 0) or 0
        if not r or "error" in r:
            pass_cell = "—"
        elif cagr >= 28 and maxdd <= 58:
            pass_cell = "✅"
        else:
            pass_cell = "❌"
        link = f"[{row_num}](#strategy-{row_num})"
        lines.append(
            f"| {link:<20} | {pass_cell:<4} | {meta.get('category','—'):<15} | "
            f"{r.get('cagr','—'):<4} | {r.get('maxdd','—'):<5} | {r.get('sharpe','—'):<6} | "
            f"{stats['win_count']:<5} | {stats['loss_count']:<5} | {stats['wl_ratio']:<8} | "
            f"{stats['profit_ratio']:<12} | {meta.get('overfit','—'):<6} |"
        )

    lines += ["", "", "---"]

    # Detail sections — anchors match row_num
    for row_num, (sid, meta) in enumerate(visible, 1):
        r      = backtest_results.get(sid, {})
        stats  = _derive_trade_stats(r)
        lines.append(f"## Strategy-{row_num}")

        name      = meta.get("name", f"Strategy {row_num}")
        file_name = meta.get("file", "")
        if file_name and not name.endswith(f"({file_name})"):
            name = f"{name} ({file_name})"
        lines += [f"### {name}", ""]

        desc = meta.get("description", "")
        if desc:
            lines += [f"**Description:** {desc}", ""]

        overfit_notes = meta.get("overfit_notes", "")
        if overfit_notes:
            lines += [f"*Overfit {meta.get('overfit','—')} — {overfit_notes}*", ""]

        for rule in meta.get("rules", []):
            lines.append(f"- **{rule['label']}:** {rule['text']}" if isinstance(rule, dict) else f"- {rule}")
        if meta.get("rules"):
            lines.append("")

        # Stats table
        lines += [
            "| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
            f"| {r.get('cagr','—')} | {r.get('maxdd','—')} | {r.get('sharpe','—')} | "
            f"{stats['win_count']} | {stats['loss_count']} | {stats['wl_ratio']} | {stats['profit_ratio']} |",
            "",
        ]

        # Yearly returns
        yearly = r.get("yearly", {})
        lines.append("| " + " | ".join(year_labels) + " |")
        lines.append("| " + " | ".join([":---"] * len(year_labels)) + " |")
        cells = []
        for y in years:
            val = yearly.get(str(y))
            if val is not None:
                try:
                    v = int(val)
                    color = "🟢" if v > 0 else ("🔴" if v < 0 else "⚪")
                except (ValueError, TypeError):
                    color = "⚪"
                cells.append(f"{color} {val}%")
            else:
                cells.append("—")
        lines += ["| " + " | ".join(cells) + " |", ""]

        # Code embed
        vault_path = meta.get("vault_path") or (
            f"vault://QuantConnect/cc/{meta['algo_dir']}/{file_name}"
            if meta.get("algo_dir") and file_name else ""
        )
        if vault_path:
            display = vault_path.rsplit("/", 1)[-1]
            lines += [
                f"> [!code]- Click to view: {display}",
                "> ```embed-python",
                f'> PATH: "{vault_path}"',
                "> ```", "",
            ]

        lines += ["", "---", ""]

    with open(output_path, "w") as f:
        f.write("\n".join(lines))
    print(f"Markdown generated: {output_path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate batch .md from catalog .jsonl")
    parser.add_argument("cc_jsonl", nargs="?", default=None)
    parser.add_argument("--skip-bt", action="store_true")
    args = parser.parse_args()

    cc_jsonl_path = args.cc_jsonl or os.path.join(SCRIPT_DIR, "json", "strategies.jsonl")
    if not os.path.exists(cc_jsonl_path):
        print(f"Error: {cc_jsonl_path} not found")
        sys.exit(1)

    cfg          = _load_cfg()
    catalog_name = os.path.splitext(os.path.basename(cc_jsonl_path))[0]
    batch_cfg    = load_batch_config(catalog_name)
    folder       = batch_cfg.get("_folder", catalog_name)
    batch_id     = _get_batch_id(folder, cfg)
    show_all     = not batch_cfg.get("prune", True)

    md_path      = os.path.join(SCRIPT_DIR, "md", f"{folder}.md")
    bt_jsonl     = os.path.join(SCRIPT_DIR, "backtests", f"backtest_{batch_id}.jsonl")
    bt_json      = os.path.join(SCRIPT_DIR, "backtests", f"backtest_{batch_id}.json")
    backtest_path = bt_jsonl if os.path.exists(bt_jsonl) else bt_json

    metadata, strategies = load_jsonl(cc_jsonl_path)
    if not strategies:
        print("Error: no strategies found in JSONL")
        sys.exit(1)

    if args.skip_bt:
        backtest_results = load_backtest(backtest_path)
    else:
        backtest_results = run_missing_backtests(strategies, backtest_path, md_path, show_all, batch_cfg)

    generate_markdown(strategies, backtest_results, md_path, show_all, batch_cfg)


if __name__ == "__main__":
    main()
