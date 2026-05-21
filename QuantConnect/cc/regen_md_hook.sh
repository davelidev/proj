#!/bin/bash
f="$1"

# File path case: any cc/.../*.jsonl edit via Write|Edit tool
if echo "$f" | grep -qE 'cc/.*\.jsonl$'; then
    batch=$(basename "$f" | grep -oE 'cc[0-9]+' | head -1)
    if [ -n "$batch" ]; then
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
        catalog="cc/json/$batch.jsonl"
        [ -f "$catalog" ] && python3 cc/generate_md.py "$catalog" --skip-bt
    fi
fi
