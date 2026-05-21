#!/usr/bin/env python3
"""
Prune non-passing entries from ccNNN backtests, catalog, and algo files.

Usage:
    python3 cc/prune.py 002           # prune cc002
    python3 cc/prune.py 018 019       # prune multiple
    python3 cc/prune.py --all         # prune all ccNNN where NNN >= 2
    python3 cc/prune.py --dry-run     # show what would be removed, no changes
"""

import argparse, json, os, sys, glob

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "json", "config.json")


def _get_folder(cc, cfg):
    files = cfg.get("files", [])
    try:
        n = int(cc[2:])
        if 0 <= n < len(files):
            return files[n]
    except (ValueError, TypeError):
        pass
    return cc


def is_prunable(cc):
    """Return True if this batch should be pruned, per config.json."""
    if not os.path.exists(CONFIG_PATH):
        return True
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)
    global_prune = cfg.get("global", {}).get("prune", True)
    folder       = _get_folder(cc, cfg)
    return cfg.get(folder, {}).get("prune", global_prune)


def load_backtest(cc):
    """Load backtest file (tries .json first, then .jsonl). Returns list of {id, passed, ...} dicts."""
    json_path = os.path.join(SCRIPT_DIR, "backtests", f"backtest_{cc}.json")
    jsonl_path = os.path.join(SCRIPT_DIR, "backtests", f"backtest_{cc}.jsonl")

    if os.path.exists(jsonl_path):
        entries = []
        with open(jsonl_path) as f:
            for line in f:
                line = line.strip()
                if line:
                    entries.append(json.loads(line))
        return entries, jsonl_path, "jsonl"
    elif os.path.exists(json_path):
        data = load_json(json_path)
        entries = []
        for k, v in data.items():
            v["id"] = k  # dict keys are the IDs, inject into value
            entries.append(v)
        return entries, json_path, "json"
    return [], None, None


def save_backtest(entries, path, fmt):
    """Write backtest entries back to file."""
    if fmt == "jsonl":
        with open(path, "w") as f:
            for e in entries:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")
    else:
        data = {e["id"]: {k: v for k, v in e.items() if k != "id"} for e in entries}
        with open(path, "w") as f:
            json.dump(data, f, ensure_ascii=False)


def load_json(path):
    with open(path) as f:
        return json.load(f)


def load_catalog(cc):
    """Load catalog JSONL. Returns (metadata_entries, strategy_entries)."""
    path = os.path.join(SCRIPT_DIR, "json", f"{cc}.jsonl")
    if not os.path.exists(path):
        return [], [], path
    metadata = []
    strategies = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            e = json.loads(line)
            if e.get("type") == "strategy":
                strategies.append(e)
            else:
                metadata.append(e)
    return metadata, strategies, path


def save_catalog(metadata, strategies, path):
    with open(path, "w") as f:
        for e in metadata:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
        for s in strategies:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")


def find_algo_files(cc):
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            cfg = json.load(f)
        folder = _get_folder(cc, cfg)
    else:
        folder = cc
    return sorted(glob.glob(os.path.join(SCRIPT_DIR, "cc_algos", folder, f"{cc}_*.py")))


def prune(cc, dry_run=False):
    """Prune non-passing entries for one cc version. Returns summary dict."""
    bt_entries, bt_path, bt_fmt = load_backtest(cc)
    if not bt_entries:
        return {"cc": cc, "error": "no backtest file found"}

    metadata, strategies, catalog_path = load_catalog(cc)

    passing_ids = {e["id"] for e in bt_entries if e.get("passed") is True}
    non_passing_bt = [e for e in bt_entries if e.get("passed") is not True]

    keep_strategies = [s for s in strategies if s["id"] in passing_ids]
    remove_strategies = [s for s in strategies if s["id"] not in passing_ids]

    keep_files = {s["file"] for s in keep_strategies}
    algo_files = find_algo_files(cc)
    delete_files = [f for f in algo_files if os.path.basename(f) not in keep_files]
    keep_files_list = [f for f in algo_files if os.path.basename(f) in keep_files]

    result = {
        "cc": cc,
        "bt_path": bt_path,
        "bt_fmt": bt_fmt,
        "bt_total": len(bt_entries),
        "bt_passing": len(passing_ids),
        "bt_remove": len(non_passing_bt),
        "catalog_total": len(strategies),
        "catalog_keep": len(keep_strategies),
        "catalog_remove": len(remove_strategies),
        "algo_total": len(algo_files),
        "algo_keep": len(keep_files_list),
        "algo_delete": len(delete_files),
        "passing_ids": sorted(passing_ids),
        "keep_files": sorted(keep_files),
        "delete_files": delete_files,
    }

    if dry_run:
        return result

    # Write backtest
    bt_keep = [e for e in bt_entries if e["id"] in passing_ids]
    save_backtest(bt_keep, bt_path, bt_fmt)

    # Write catalog
    save_catalog(metadata, keep_strategies, catalog_path)

    # Delete algo files
    for f in delete_files:
        os.remove(f)

    return result


def main():
    parser = argparse.ArgumentParser(description="Prune non-passing ccNNN entries")
    parser.add_argument("ccs", nargs="*", help="cc versions to prune (e.g. 002 018)")
    parser.add_argument("--all", action="store_true", help="prune all ccNNN where NNN >= 2")
    parser.add_argument("--dry-run", action="store_true", help="show what would be done, no changes")
    args = parser.parse_args()

    if args.all:
        # Find all catalog files
        ccs = []
        for f in sorted(glob.glob(os.path.join(SCRIPT_DIR, "json", "cc*.jsonl"))):
            name = os.path.basename(f)
            num = name[2:5]  # "001" from "cc001.jsonl"
            if int(num) >= 2:
                ccs.append(f"cc{num}")
    elif args.ccs:
        ccs = [f"cc{a.zfill(3)}" for a in args.ccs]
    else:
        parser.print_help()
        sys.exit(1)

    total = {"bt_remove": 0, "catalog_remove": 0, "algo_delete": 0}

    for cc in ccs:
        if not is_prunable(cc):
            print(f"{cc}: skipped (prune: false in config.json)")
            continue
        result = prune(cc, dry_run=args.dry_run)
        if "error" in result:
            print(f"{cc}: {result['error']}")
            continue

        status = "[DRY RUN] " if args.dry_run else ""
        print(f"{status}{cc}: {result['bt_passing']}/{result['bt_total']} backtests pass, "
              f"keeping {result['catalog_keep']}/{result['catalog_total']} catalog, "
              f"keeping {result['algo_keep']}/{result['algo_total']} algos")
        if result["passing_ids"]:
            print(f"  Passing IDs: {result['passing_ids']}")
            print(f"  Files kept: {result['keep_files']}")

        if args.dry_run and result["algo_delete"]:
            print(f"  Would delete {result['algo_delete']} algo files")
            for f in result["delete_files"][:10]:
                print(f"    {os.path.basename(f)}")
            if len(result["delete_files"]) > 10:
                print(f"    ... and {len(result['delete_files']) - 10} more")

        total["bt_remove"] += result["bt_remove"]
        total["catalog_remove"] += result["catalog_remove"]
        total["algo_delete"] += result["algo_delete"]
        print()

    print(f"{status}Total: {total['bt_remove']} backtest entries, "
          f"{total['catalog_remove']} catalog entries, "
          f"{total['algo_delete']} algo files {'would be ' if args.dry_run else ''}removed")


if __name__ == "__main__":
    main()
