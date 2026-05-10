#!/bin/bash

# Comprehensive batch runner for all 200 validated strategies
cd /Users/daveli/Desktop/proj/QuantConnect

# Initialize log
echo "algo_num,name,batch,cagr,maxdd,sharpe,pass,backtest_id" > cc3.log

COMPLETED=0
PASSED=0
CLUSTER_FULL_COUNT=0
MAX_QUEUE=5  # Don't queue more than 5 backtests at a time

# Check cluster capacity before attempting submissions
check_cluster_capacity() {
    # Try a test submission to see if cluster has capacity
    python3 << 'PYEOF'
import requests
import hashlib
import base64
import time
import os
from dotenv import load_dotenv

load_dotenv("api/.env")

USER_ID = os.environ.get("QC_USER_ID")
API_TOKEN = os.environ.get("QC_API_TOKEN")
BASE_URL = os.environ.get("QC_BASE_URL", "https://www.quantconnect.com/api/v2")

def get_auth_headers():
    timestamp = str(int(time.time()))
    token_hash = hashlib.sha256(f"{API_TOKEN}:{timestamp}".encode()).hexdigest()
    auth_64 = base64.b64encode(f"{USER_ID}:{token_hash}".encode()).decode()
    return {"Authorization": f"Basic {auth_64}", "Timestamp": timestamp}

# List recent backtests to estimate queue depth
headers = get_auth_headers()
try:
    resp = requests.get(f"{BASE_URL}/backtests", headers=headers, params={"limit": 10})
    data = resp.json()
    if data.get("success"):
        backtests = data.get("backtests", [])
        running = [b for b in backtests if b.get("status") in ["Running", "Queued"]]
        print(f"Queue depth: {len(running)} active/queued")
        if len(running) >= 5:
            print("CLUSTER_BUSY")
        else:
            print("CLUSTER_READY")
    else:
        print("CLUSTER_UNKNOWN")
except:
    print("CLUSTER_UNKNOWN")
PYEOF
}

echo "Starting batch submission of 200 strategies..."
echo "Target: CAGR ≥ 28% AND |MaxDD| ≤ 58%"
echo ""

# Main submission loop
for ALGO_NUM in {001..200}; do
  FILE="cc/algos3/algo_${ALGO_NUM}.py"
  NAME="Algo${ALGO_NUM}"

  if [ ! -f "$FILE" ]; then
    echo "[$(printf %02d $((COMPLETED / 60)):$(printf %02d $((COMPLETED % 60))))] [$ALGO_NUM/200] SKIPPED (file not found)"
    ((COMPLETED++))
    continue
  fi

  printf "[%02d:%02d] [%3d/200] Submitting %s" $((COMPLETED / 60)) $((COMPLETED % 60)) $ALGO_NUM "$NAME"

  # Try to submit with cluster capacity awareness
  BACKTEST_ID=""
  RETRY_COUNT=0
  MAX_RETRIES=5
  WAIT_TIME=30

  while [ -z "$BACKTEST_ID" ] && [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    SUBMIT_RESULT=$(python3 api/run_qc_backtest.py "$FILE" "$NAME" 2>&1)

    if echo "$SUBMIT_RESULT" | grep -q "BACKTEST_ID="; then
      BACKTEST_ID=$(echo "$SUBMIT_RESULT" | grep "BACKTEST_ID=" | cut -d= -f2 | tr -d ' ')
      printf " → BID:%s\n" "$BACKTEST_ID"
      break
    elif echo "$SUBMIT_RESULT" | grep -qi "no spare nodes\|cluster\|queue"; then
      ((CLUSTER_FULL_COUNT++))
      ((RETRY_COUNT++))
      if [ $RETRY_COUNT -ge 3 ]; then
        printf " ⏳ Cluster full (wait $WAIT_TIME s)..."
        sleep $WAIT_TIME
        WAIT_TIME=$((WAIT_TIME < 120 ? WAIT_TIME + 30 : 120))
      else
        printf " ↻ retry $RETRY_COUNT..."
        sleep 5
      fi
    else
      printf " ✗ ERROR\n"
      echo "  Details: $(echo "$SUBMIT_RESULT" | grep -i "error\|failed" | head -1)"
      break
    fi
  done

  if [ -z "$BACKTEST_ID" ]; then
    printf "  FAILED submission\n"
    echo "$ALGO_NUM,$NAME,batch,—,—,—,FAIL,no-id" >> cc3.log
    ((COMPLETED++))
    continue
  fi

  # Poll for results (timeout 600000ms = 10 min per strategy)
  POLL_RESULT=$(timeout 600 python3 api/poll_backtest.py "$BACKTEST_ID" 2>&1)
  POLL_EXIT=$?

  if [ $POLL_EXIT -eq 124 ]; then
    printf "  ⏱️  TIMEOUT (still running)\n"
    echo "$ALGO_NUM,$NAME,batch,—,—,—,PENDING,$BACKTEST_ID" >> cc3.log
    ((COMPLETED++))
    continue
  fi

  # Extract metrics with flexible regex patterns
  CAGR=$(echo "$POLL_RESULT" | grep -oiE "cagr|return|annual.*return" -A 1 | tail -1 | grep -oE "[0-9.-]+" | head -1)
  MAXDD=$(echo "$POLL_RESULT" | grep -oiE "maximum.*drawdown|max drawdown" -A 1 | tail -1 | grep -oE "[0-9.-]+" | head -1)
  SHARPE=$(echo "$POLL_RESULT" | grep -oiE "sharpe" -A 1 | tail -1 | grep -oE "[0-9.-]+" | head -1)

  # Fallback: try to extract from summary line
  if [ -z "$CAGR" ] || [ -z "$MAXDD" ]; then
    CAGR=$(echo "$POLL_RESULT" | grep -iE "backtest.*return|return.*%" | sed 's/.*\([0-9.-]*\)%.*/\1/' | head -1)
    MAXDD=$(echo "$POLL_RESULT" | grep -iE "drawdown|dd" | sed 's/.*\([0-9.-]*\)%.*/\1/' | head -1)
  fi

  CAGR=${CAGR:=—}
  MAXDD=${MAXDD:=—}
  SHARPE=${SHARPE:=—}

  # Evaluate pass criteria: CAGR >= 28 AND |MaxDD| <= 58
  PASS="FAIL"
  if [ "$CAGR" != "—" ] && [ "$MAXDD" != "—" ]; then
    CAGR_INT=$(printf "%.0f" $(echo "$CAGR" | sed 's/%//'))
    MAXDD_INT=$(printf "%.0f" $(echo "$MAXDD" | sed 's/%//'))
    MAXDD_ABS=${MAXDD_INT#-}

    if [ "$CAGR_INT" -ge 28 ] && [ "$MAXDD_ABS" -le 58 ]; then
      PASS="PASS"
      ((PASSED++))
      printf "  ✓ PASS (CAGR=%s%% DD=%s%%)\n" "$CAGR" "$MAXDD"
    else
      printf "  ✗ Fail (CAGR=%s%% DD=%s%%)\n" "$CAGR" "$MAXDD"
    fi
  else
    printf "  ⚠ Incomplete results (CAGR=%s DD=%s)\n" "$CAGR" "$MAXDD"
  fi

  echo "$ALGO_NUM,$NAME,batch,$CAGR,$MAXDD,$SHARPE,$PASS,$BACKTEST_ID" >> cc3.log

  ((COMPLETED++))

  # Show progress every 20
  if [ $((COMPLETED % 20)) -eq 0 ]; then
    echo ""
    echo ">>> Progress: $COMPLETED/200 | Passed: $PASSED | Rate: $(echo "scale=0; $PASSED * 100 / $COMPLETED" | bc)% | Cluster-full events: $CLUSTER_FULL_COUNT"
    echo ""
  fi

  # Rate limit: small sleep between submissions
  sleep 2
done

echo ""
echo "==================================================================="
echo "=== FINAL RESULTS ==="
echo "Completed: $COMPLETED/200"
echo "Passed: $PASSED"
echo "Pass Rate: $(echo "scale=1; $PASSED * 100 / 200" | bc)%"
echo "Cluster-full retries: $CLUSTER_FULL_COUNT"
echo ""
echo "=== Top Results (by Sharpe) ==="
if [ $(wc -l < cc3.log) -gt 1 ]; then
    tail -1 cc3.log
    sort -t, -k6 -rn cc3.log | head -10
fi
