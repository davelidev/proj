#!/bin/bash
f="$1"

# File path case: any cc/.../*.jsonl edit via Write|Edit tool
if echo "$f" | grep -qE 'cc/.*\.jsonl$'; then
    batch=$(basename "$f" | grep -oE 'cc[0-9]+' | head -1)
    if [ -z "$batch" ]; then
        # Named catalog (e.g. ensemble.jsonl, strategies.jsonl) — pass path directly
        [ -f "$f" ] && python3 cc/generate_md.py "$f" --skip-bt
    else
        catalog="cc/json/$batch.jsonl"
        [ -f "$catalog" ] && python3 cc/generate_md.py "$catalog" --skip-bt
    fi

# Bash command case: run_cc_batch.py ccNNN or run_cc_batch.py NNN
elif echo "$f" | grep -q 'run_cc_batch'; then
    batch=$(echo "$f" | grep -oE 'cc[0-9]+' | head -1)
    if [ -z "$batch" ]; then
        num=$(echo "$f" | grep -oE 'run_cc_batch\.py\s+[0-9]+' | grep -oE '[0-9]+$')
        [ -n "$num" ] && batch=$(printf "cc%03d" "$num")
    fi
    if [ -n "$batch" ]; then
        python3 - <<PYEOF
import json, os, sys
sys.path.insert(0, 'cc')
CONFIG = 'cc/json/config.json'
batch = '$batch'
cfg = json.load(open(CONFIG)) if os.path.exists(CONFIG) else {}
files = cfg.get('files', [])
try:
    folder = files[int(batch[2:])]
except:
    folder = batch
catalog = cfg.get(folder, {}).get('catalog', folder)
path = f'cc/json/{catalog}.jsonl'
if os.path.exists(path):
    os.execlp('python3', 'python3', 'cc/generate_md.py', path, '--skip-bt')
PYEOF
    fi
fi
