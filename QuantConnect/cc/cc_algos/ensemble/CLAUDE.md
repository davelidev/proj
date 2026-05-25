# ensemble/

Each `NNN.py` file is a `BaseSubAlgo` subclass — not a standalone `QCAlgorithm`. To run a backtest, first generate a standalone bundle:

```bash
python3 cc/cc_algos/ensemble/utils/bundle.py cc/cc_algos/ensemble/NNN.py
# outputs: cc/cc_algos/ensemble/merged/standalone.py
```

Then upload and run:

```bash
python3 api/run_qc_backtest.py cc/cc_algos/ensemble/merged/standalone.py "ensemble/NNN <ClassName>"
python3 api/poll_backtest.py <BACKTEST_ID>
python3 api/get_yearly_stats.py <BACKTEST_ID>
```
