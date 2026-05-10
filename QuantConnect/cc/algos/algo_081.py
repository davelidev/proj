from AlgorithmImports import *


class Algo081(QCAlgorithm):
    """Risk Parity QQQ/IEF/GLD: weights inverse to 20-day realized volatility.
    Rebalance only when any leg drifts >5% from target. Sum of weights = 1.0."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.ief = self.AddEquity("IEF", Resolution.Daily).Symbol
        self.gld = self.AddEquity("GLD", Resolution.Daily).Symbol
        self.assets = [self.qqq, self.ief, self.gld]

        self.lookback = 20
        self.drift_threshold = 0.05

        self.target_weights = {sym: 0.0 for sym in self.assets}

        self.SetWarmUp(self.lookback + 5, Resolution.Daily)

    def _compute_target_weights(self):
        vols = {}
        for sym in self.assets:
            hist = self.History(sym, self.lookback + 1, Resolution.Daily)
            if hist is None or hist.empty:
                return None
            try:
                closes = hist["close"]
            except Exception:
                return None
            if len(closes) < self.lookback + 1:
                return None
            rets = closes.pct_change().dropna()
            if len(rets) < 2:
                return None
            v = float(rets.std())
            if v <= 0 or v != v:  # NaN guard
                return None
            vols[sym] = v

        inv = {sym: 1.0 / v for sym, v in vols.items()}
        total_inv = sum(inv.values())
        if total_inv <= 0:
            return None
        return {sym: inv[sym] / total_inv for sym in self.assets}

    def OnData(self, data):
        if self.IsWarmingUp:
            return

        new_targets = self._compute_target_weights()
        if new_targets is None:
            return

        # Compute current actual portfolio weights
        equity = float(self.Portfolio.TotalPortfolioValue)
        if equity <= 0:
            return

        current_weights = {}
        for sym in self.assets:
            holding_value = float(self.Portfolio[sym].HoldingsValue)
            current_weights[sym] = holding_value / equity

        # Check drift vs new targets
        max_drift = 0.0
        for sym in self.assets:
            d = abs(current_weights[sym] - new_targets[sym])
            if d > max_drift:
                max_drift = d

        # If never invested, force initial allocation
        any_invested = any(self.Portfolio[s].Invested for s in self.assets)

        if (not any_invested) or max_drift > self.drift_threshold:
            self.target_weights = new_targets
            for sym in self.assets:
                self.SetHoldings(sym, self.target_weights[sym])
