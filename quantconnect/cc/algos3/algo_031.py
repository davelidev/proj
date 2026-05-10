import numpy as np
from datetime import datetime, timedelta
from clr import AddReference
AddReference("System")
AddReference("QuantConnect.Common")
AddReference("QuantConnect.Indicators")
AddReference("QuantConnect.Algorithm")
AddReference("QuantConnect.Algorithm.Framework")

from System import *
from QuantConnect import *
from QuantConnect.Algorithm import QCAlgorithm
from QuantConnect.Data.UniverseSelection import *
from QuantConnect.Indicators import *

class Algo031(QCAlgorithm):
    """Multi-horizon momentum vote with adaptive sizing using vol, correlation and drawdown cycles"""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        # Only explicitly added ticker
        self.AddEquity("TQQQ", Resolution.Daily)

        # Dynamic universe for top 10 mega-cap stocks
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseFilter, self.FineFilter)

        # Storage for basket symbols and data
        self.basket = {}

        # Equity tracking for drawdown
        self.portfolioValue = []
        self.highWaterMark = self.Portfolio.TotalPortfolioValue

        # Cache for history requests (avoid redundant calls)
        self.historyCache = {}

    def CoarseFilter(self, coarse):
        # Keep only stocks with price > $10 and sufficient daily volume
        filtered = [c for c in coarse if c.HasFundamentalData and c.Price > 10 and c.Volume > 1000000]
        # Sort by market cap descending and take top 100 for fine filter
        sorted_by_dollar = sorted(filtered, key=lambda x: x.DollarVolume, reverse=True)
        return [x.Symbol for x in sorted_by_dollar[:100]]

    def FineFilter(self, fine):
        # Sort by fundamental market cap descending and take top 10
        sorted_by_market_cap = sorted(fine, key=lambda f: f.MarketCap, reverse=True)
        top10 = sorted_by_market_cap[:10]
        return [f.Symbol for f in top10]

    def OnSecuritiesChanged(self, changes):
        # Update basket with current universe symbols
        for added in changes.AddedSecurities:
            symbol = added.Symbol
            if symbol not in self.basket:
                self.basket[symbol] = {}
        for removed in changes.RemovedSecurities:
            symbol = removed.Symbol
            if symbol in self.basket:
                del self.basket[symbol]

    def OnData(self, data):
        if not data.Bars.Count:
            return

        # Clear history cache each day
        self.historyCache.clear()

        # 1. Compute multi-horizon momentum signals for basket stocks
        signals = {}
        for symbol in self.basket:
            sig = self.ComputeMomentumSignal(symbol)
            if sig is not None:
                signals[symbol] = sig

        if not signals:
            return

        # 2. Regime estimation from TQQQ (volatility proxy)
        tqqq_vol = self.EstimateVolatility("TQQQ", 63)
        vol_mult = 1.0
        if tqqq_vol > 0.30:
            vol_mult = 0.5
        elif tqqq_vol > 0.15:
            vol_mult = 0.8

        # 3. Average correlation among basket stocks (if enough symbols)
        corr_mult = 1.0
        if len(signals) >= 2:
            avg_corr = self.AveragePairwiseCorrelation(list(signals.keys()), 63)
            # Reduce weight if correlation is high (above 0.5)
            if avg_corr > 0.5:
                corr_mult = max(0.5, 1.0 - (avg_corr - 0.5) * 2)  # linear reduction

        # 4. Portfolio drawdown
        current_value = self.Portfolio.TotalPortfolioValue
        self.portfolioValue.append(current_value)
        if current_value > self.highWaterMark:
            self.highWaterMark = current_value
        dd = (self.highWaterMark - current_value) / self.highWaterMark
        dd_mult = 1.0
        if dd > 0.20:
            dd_mult = 0.5  # cut in half when drawdown > 20%
        elif dd > 0.10:
            dd_mult = 0.8

        # 5. Build final weights
        weights = {}
        for sym, sig in signals.items():
            # Signal: +1 for long, -1 for short, 0 for neutral
            weight = sig * 0.1  # base equal weight per name (10 names => 0.1)
            weight *= vol_mult
            weight *= corr_mult
            weight *= dd_mult
            weights[sym] = weight

        # Normalize weights so total absolute weight <= 1
        total_abs = sum(abs(w) for w in weights.values())
        if total_abs > 1:
            scale = 1.0 / total_abs
            for sym in weights:
                weights[sym] *= scale

        # 6. Rebalance
        for sym, w in weights.items():
            self.SetHoldings(sym, w)

        # Log some diagnostics
        self.Log(f"Date: {self.Time}, VolMult: {vol_mult:.2f}, CorrMult: {corr_mult:.2f}, DDMult: {dd_mult:.2f}")

    def ComputeMomentumSignal(self, symbol):
        """Returns +1 (long), -1 (short), 0 (neutral) based on majority vote over 5/10/21/63d returns."""
        lookbacks = [5, 10, 21, 63]
        returns = []
        for lb in lookbacks:
            ret = self.GetReturn(symbol, lb)
            if ret is None:
                return None
            returns.append(ret)
        # Count positive returns
        pos_count = sum(1 for r in returns if r > 0)
        if pos_count >= 3:
            return 1
        elif pos_count <= 1:
            return -1
        else:
            return 0

    def GetReturn(self, symbol, period):
        """Compute simple return over 'period' days using History."""
        key = (symbol, period)
        if key in self.historyCache:
            return self.historyCache[key]

        # Need at least period+1 bars: current close and close period days ago
        history = self.History([symbol], period + 1, Resolution.Daily)
        if history.empty or len(history) < period + 1:
            return None

        closes = history.loc[symbol].close.values
        current_close = closes[-1]
        past_close = closes[0]
        ret = (current_close - past_close) / past_close
        self.historyCache[key] = ret
        return ret

    def EstimateVolatility(self, ticker, period):
        """Annualized volatility using daily log returns over period days."""
        symbol = Symbol.Create(ticker, SecurityType.Equity, Market.USA)
        history = self.History([symbol], period + 1, Resolution.Daily)
        if history.empty or len(history) < period + 1:
            return 0.20  # fallback

        closes = history.loc[symbol].close.values
        log_returns = np.diff(np.log(closes))
        daily_vol = np.std(log_returns)
        ann_vol = daily_vol * np.sqrt(252)
        return ann_vol

    def AveragePairwiseCorrelation(self, symbols, period):
        """Average Pearson correlation of daily returns over period days."""
        if len(symbols) < 2:
            return 0.0

        # Collect returns matrix: rows = days, cols = symbols
        history = self.History(symbols, period + 1, Resolution.Daily)
        if history.empty:
            return 0.0

        # Build DataFrame of closes
        closes_df = history['close'].unstack(level=0)
        returns_df = closes_df.pct_change().dropna()
        if returns_df.shape[0] < 2:
            return 0.0

        corr_matrix = returns_df.corr()
        # Average the upper triangle
        n = len(symbols)
        total_corr = 0.0
        count = 0
        for i in range(n):
            for j in range(i+1, n):
                if j < len(corr_matrix.columns) and i < len(corr_matrix.columns):
                    total_corr += corr_matrix.iloc[i, j]
                    count += 1
        if count == 0:
            return 0.0
        return total_corr / count
