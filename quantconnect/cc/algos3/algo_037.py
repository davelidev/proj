import numpy as np
from QuantConnect import *
from QuantConnect.Data.UniverseSelection import *

class Algo037(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        # Daily resolution for all data and rebalancing
        self.UniverseSettings.Resolution = Resolution.Daily
        self.Settings.RebalancePortfolioEveryDay = True

        # Add TQQQ as a permanent holding
        self.AddEquity("TQQQ", Resolution.Daily)
        self.basket = {"TQQQ": {}}   # track all symbols (TQQQ + universe)

        # Universe selection for top-10 mega-cap
        self.AddUniverse(self.CoarseSelectionFunction)

        # Strategy parameters
        self.momentum_window = 63          # 3 months
        self.decay_period = 20             # EMA span for momentum smoothing
        self.vol_window = 21
        self.vol_threshold = 0.02
        self.corr_window = 63
        self.corr_threshold = 0.5
        self.breadth_threshold = 0.4
        self.drawdown_threshold = 0.1
        self.drawdown_factor = 0.8

        # Track peak equity and drawdown
        self.peak = 0
        self.drawdown = 0


    def CoarseSelectionFunction(self, coarse):
        # Select top 10 stocks by dollar volume (mega‑cap proxy)
        sorted_by_vol = sorted(coarse,
                               key=lambda c: c.DollarVolume,
                               reverse=True)
        top10 = [c.Symbol for c in sorted_by_vol[:10] if c.HasFundamentalData]
        return top10


    def OnSecuritiesChanged(self, changes):
        # Add new universe symbols to the basket
        for added in changes.AddedSecurities:
            symbol = added.Symbol
            if symbol not in self.basket:
                self.basket[symbol] = {}

        # Remove symbols no longer in universe (but keep TQQQ)
        for removed in changes.RemovedSecurities:
            symbol = removed.Symbol
            if symbol in self.basket and symbol != "TQQQ":
                del self.basket[symbol]


    def OnData(self, data):
        # Update peak and drawdown from portfolio equity
        equity = self.Portfolio.TotalPortfolioValue
        if equity > self.peak:
            self.peak = equity
        self.drawdown = (self.peak - equity) / self.peak if self.peak > 0 else 0

        # Get list of all symbols in the basket
        symbols = list(self.basket.keys())
        if len(symbols) == 0:
            return

        # Fetch historical close prices for the required lookback
        lookback = self.momentum_window + self.decay_period + 5
        hist = self.History(symbols, lookback, Resolution.Daily)
        if hist.empty:
            return

        close = hist['close'].unstack(level=0).dropna(axis=1, how='any')
        if close.shape[0] < self.momentum_window:
            return

        # 1. Momentum signal with exponential decay
        # Compute the 63‑day momentum (rate of change)
        momentum_raw = close / close.shift(self.momentum_window) - 1
        # Apply an exponential moving average (span = decay_period) to the momentum series
        momentum_decayed = momentum_raw.ewm(span=self.decay_period, adjust=False).mean()
        # The final signal is the most recent value of the smoothed momentum
        signals = momentum_decayed.iloc[-1]

        # Keep only positive signals (long‑only momentum)
        signals = signals[signals > 0]
        if signals.empty:
            # No positive signals – go to cash
            for sym in symbols:
                self.SetHoldings(sym, 0)
            return

        # 2. Regime factors
        # Volatility regime (using TQQQ daily returns)
        returns = close.pct_change().dropna()
        vol_factor = 1.0
        if "TQQQ" in returns.columns:
            hist_vol = np.std(returns["TQQQ"].iloc[-self.vol_window:])
            if hist_vol > self.vol_threshold:
                vol_factor = 0.5

        # Correlation regime (average pairwise absolute correlation)
        corr_factor = 1.0
        if len(returns.columns) >= 2 and len(returns) >= self.corr_window:
            corr_mat = returns.iloc[-self.corr_window:].corr()
            utri_mask = np.triu(np.ones(corr_mat.shape), k=1).astype(bool)
            avg_corr = np.nanmean(np.abs(corr_mat.values[utri_mask]))
            if avg_corr > self.corr_threshold:
                corr_factor = 0.7

        # Breadth regime (fraction of symbols with positive signal)
        total_sym_count = len(symbols)
        positive_count = len(signals)
        breadth = positive_count / total_sym_count if total_sym_count > 0 else 0
        breadth_factor = 0.6 if breadth < self.breadth_threshold else 1.0

        # Drawdown regime
        dd_factor = self.drawdown_factor if self.drawdown > self.drawdown_threshold else 1.0

        # Combine scaling factors
        scaling = vol_factor * corr_factor * breadth_factor * dd_factor

        # 3. Position sizing
        # Raw weights = signal * scaling (only for symbols with positive signal)
        raw_weights = signals * scaling
        if raw_weights.sum() <= 0:
            for sym in symbols:
                self.SetHoldings(sym, 0)
            return

        # Ensure total weight ≤ 1 (no leverage)
        if raw_weights.sum() > 1.0:
            raw_weights /= raw_weights.sum()

        # 4. Place trades
        for sym in symbols:
            weight = raw_weights.get(sym, 0.0)
            self.SetHoldings(sym, weight)
