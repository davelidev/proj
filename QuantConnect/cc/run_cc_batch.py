"""Run backtests for a cc catalog batch.

Usage:
    python3 run_cc_batch.py cc017               # all entries in cc017 catalog
    python3 run_cc_batch.py cc018 1-50          # algo file nums 1-50
    python3 run_cc_batch.py cc019 5 12 20       # specific algo file nums
    python3 run_cc_batch.py 19 5-10             # '19' expands to 'cc019'
"""
import os, sys, time, json

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'api'))
from batch_runner import run_backtest

SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH  = os.path.join(SCRIPT_DIR, 'json', 'config.json')


def _get_folder(batch, cfg):
    files = cfg.get('files', [])
    try:
        n = int(batch[2:])
        if 0 <= n < len(files):
            return files[n]
    except (ValueError, TypeError):
        pass
    return batch


def _get_catalog_name(folder, cfg):
    return cfg.get(folder, {}).get('catalog', folder)


def load_config(batch):
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)
    folder = _get_folder(batch, cfg)
    resolved = dict(cfg.get('global', {}))
    resolved.update(cfg.get(folder, {}))
    resolved['_folder'] = folder
    resolved['_catalog'] = _get_catalog_name(folder, cfg)
    return resolved


def load_catalog(batch):
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            cfg = json.load(f)
        folder  = _get_folder(batch, cfg)
        catalog = _get_catalog_name(folder, cfg)
    else:
        catalog = batch
    path = os.path.join(SCRIPT_DIR, 'json', f'{catalog}.jsonl')
    entries = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            if obj.get('type') == 'strategy':
                entries.append({'id': obj['id'], 'file': obj['file']})
    return entries


def load_results(outpath):
    jsonl = outpath if outpath.endswith('.jsonl') else outpath.replace('.json', '.jsonl')
    json_ = outpath if outpath.endswith('.json') else outpath.replace('.jsonl', '.json')
    results = {}
    if os.path.exists(jsonl):
        with open(jsonl) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                obj = json.loads(line)
                sid = obj.pop('id')
                results[sid] = obj
    elif os.path.exists(json_):
        with open(json_) as f:
            results = json.load(f)
    return results


def save_results(results, outpath):
    out = outpath if outpath.endswith('.jsonl') else outpath.replace('.json', '.jsonl')
    with open(out, 'w') as f:
        for sid, res in results.items():
            f.write(json.dumps({'id': sid, **res}, ensure_ascii=False) + '\n')


def parse_nums(args):
    nums = set()
    for arg in args:
        if '-' in arg:
            s, e = arg.split('-', 1)
            nums.update(range(int(s), int(e) + 1))
        else:
            nums.add(int(arg))
    return nums


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    raw_arg = sys.argv[1]
    if raw_arg.startswith('cc'):
        raw_arg = raw_arg[2:]
    batch = f'cc{raw_arg.zfill(3)}'
    label = f'CC{int(raw_arg)}'   # CC17, CC18, CC19

    catalog = load_catalog(batch)
    if not catalog:
        print(f'No entries in catalog for {batch}')
        sys.exit(1)

    if len(sys.argv) > 2:
        nums = parse_nums(sys.argv[2:])
        catalog = [
            e for e in catalog 
            if e['file'].replace('.py', '').split('/')[-1].isdigit() and int(e['file'].replace('.py', '').split('/')[-1]) in nums
        ]

    batch_cfg = load_config(batch)
    algos_dir = os.path.join(SCRIPT_DIR, 'cc_algos', batch_cfg.get('_folder', batch))
    outpath   = os.path.join(SCRIPT_DIR, 'backtests', f'backtest_{batch}.jsonl')
    results   = load_results(outpath)

    for entry in catalog:
        sid   = entry['id']
        fname = entry['file']
        
        base_name = fname.replace('.py', '').split('/')[-1]
        try:
            n = int(base_name)
            name = f'{label}_{n:03d}'
        except ValueError:
            name = f'{label}_{base_name}'

        if sid in results and 'error' not in results[sid] and results[sid].get('status') == 'completed':
            r  = results[sid]
            pf = '✅' if r.get('passed') else '❌'
            print(f'[resume] Skipping {fname} — {pf} CAGR={r["cagr"]}, MaxDD={r["maxdd"]}')
            continue
        if sid in results:
            print(f'[retry] Re-running {fname} ({results[sid].get("error", "?")})')

        filepath = os.path.join(algos_dir, fname)
        if not os.path.exists(filepath):
            filepath_utils = os.path.join(algos_dir, "utils", fname)
            if os.path.exists(filepath_utils):
                filepath = filepath_utils

        if not os.path.exists(filepath):
            print(f'{fname}: not found, skipping')
            continue

        # Bundle standalone sub-algo or full ensemble if bundler exists
        folder = batch_cfg.get('_folder', batch)
        bundle_script = os.path.join(SCRIPT_DIR, 'cc_algos', folder, 'utils', 'bundle.py')
        if os.path.exists(bundle_script):
            import subprocess
            try:
                if "ultAlgo" in fname:
                    subprocess.run(["python3", bundle_script], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    filepath = os.path.join(SCRIPT_DIR, 'cc_algos', folder, 'merged', 'ensemble.py')
                else:
                    subprocess.run(["python3", bundle_script, filepath], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    filepath = os.path.join(SCRIPT_DIR, 'cc_algos', folder, 'merged', 'standalone.py')
            except Exception as e:
                print(f"  [bundle error] Failed to bundle {fname}: {e}")

        print(f"\n{'='*60}\nRunning {fname}\n{'='*60}")
        sys.stdout.flush()

        result       = run_backtest(filepath, name)
        results[sid] = result
        if 'error' in result:
            print(f'\n  ❌ {fname}: {result["error"]}')
        else:
            pf = '✅' if result['passed'] else '❌'
            print(f'\n  {pf} {fname}: CAGR={result["cagr"]}, MaxDD={result["maxdd"]}, Sharpe={result["sharpe"]}')

        save_results(results, outpath)
        if 'error' in result:
            time.sleep(5)
        else:
            time.sleep(2)

    print('\n\n## Summary')
    print('| File | CAGR | MaxDD | Sharpe | Pass |')
    print('|------|------|-------|--------|------|')
    for entry in catalog:
        r     = results.get(entry['id'], {})
        fname = entry['file']
        if 'error' in r:
            print(f'| {fname} | ERROR | | | ❌ |')
        elif r.get('status') == 'completed':
            pf = '✅' if r.get('passed') else '❌'
            print(f'| {fname} | {r["cagr"]} | {r["maxdd"]} | {r["sharpe"]} | {pf} |')


if __name__ == '__main__':
    main()
