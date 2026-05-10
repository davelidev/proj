from System import *
from QuantConnect import *
from QuantConnect.Algorithm import *
from QuantConnect.Indicators import *
from QuantConnect.Data.Market import TradeBar
from datetime import datetime, timedelta
import numpy as np

class Algo048(QCAlgorithm):
    """Advanced Quant Trading Algorithm using Seasonality, Correlation, Dispersion, and Regime Detection."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.AddEquity("TQQQ", Resolution.Daily)
        self.AddUniverse(self.CoarseSelectionFunction)

        self.basket = {}                         # dictionary mapping symbol -> data
        self.lookback = 30                       # lookback period for signals
        self.minHistory = 20                     # minimum bars needed for calculations

        # Seasonality biases for months 1-12 (Jan = 0.5, Oct = -0.4, Dec = 0.5)
        self.seasonality_bias = {
            1: 0.5,  2: -0.2, 3: 0.1,  4: -0.1,
            5: 0.0,  6: -0.3, 7: 0.2,  8: 0.1,
            9: -0.1, 10: -0.4, 11: 0.3, 12: 0.5
        }

        self.maxWeight = 0.9                     # maximum exposure to TQQQ

    def CoarseSelectionFunction(self, coarse):
        # Select top 10 mega-cap stocks by market cap
        filtered = [c for c in coarse if c.HasFundamentalData]
        sorted_by_mc = sorted(filtered, key=lambda c: c.MarketCap, reverse=True)
        top10 = sorted_by_mc[:10]

        universe_symbols = [c.Symbol for c in top10]

        # Ensure new symbols are added to basket
        for symbol in universe_symbols:
            if symbol not in self.basket:
                self.basket[symbol] = {"close": [], "return": []}

        # Remove symbols no longer in universe
        for symbol in list(self.basket.keys()):
            if symbol not in universe_symbols:
                del self.basket[symbol]

        return universe_symbols

    def OnData(self, data):
        # Wait for enough bars
        if self.Time < datetime(2014, 1, 30):
            return

        # 1. Update price history for TQQQ and basket members
        tqqq_symbol = self.Symbol("TQQQ")
        if tqqq_symbol not in data.Bars:
            return
        tqqq_close = self.History(tqqq_symbol, self.lookback, Resolution.Daily)["close"]
        if len(tqqq_close) < self.minHistory:
            return

        tqqq_returns = tqqq_close.pct_change().dropna().values

        # Ensure we have enough basket stocks with data
        valid_symbols = []
        basket_closes = {}
        for sym, info in self.basket.items():
            if sym in data.Bars:
                hist = self.History(sym, self.lookback, Resolution.Daily)["close"]
                if len(hist) >= self.minHistory:
                    basket_closes[sym] = hist
                    valid_symbols.append(sym)

        if len(valid_symbols) < 3:
            return  # too few universe members for meaningful signals

        # 2. Compute basket daily returns (current day)
        basket_returns_today = []
        for sym in valid_symbols:
            if sym in data.Bars:
                # need previous close to compute return
                prev_close = basket_closes[sym].iloc[-2] if len(basket_closes[sym]) >= 2 else None
                if prev_close is not None:
                    ret = (data.Bars[sym].Close - prev_close) / prev_close
                    basket_returns_today.append(ret)

        if len(basket_returns_today) < 3:
            return

        # 3. Calculate Signals

        # Seasonality score: map bias [-0.5,0.5] to [0,1]
        month = self.Time.month
        bias = self.seasonality_bias[month]
        seasonality_score = (bias + 0.5) / 1.0   # 0 -> -0.5, 1 -> 0.5

        # Correlation between TQQQ and each basket stock (rolling 20-day)
        corrs = []
        for sym in valid_symbols:
            sym_close = basket_closes[sym].values
            sym_returns = np.diff(sym_close) / sym_close[:-1]
            if len(sym_returns) >= self.minHistory:
                # align lengths
                n = min(len(tqqq_returns), len(sym_returns))
                if n < 10:
                    continue
                tqqq_ret = tqqq_returns[-n:]
                sym_ret = sym_returns[-n:]
                # Pearson correlation
                corr = np.corrcoef(tqqq_ret, sym_ret)[0, 1]
                if not np.isnan(corr):
                    corrs.append(corr)
        if len(corrs) == 0:
            correlation_score = 0.5
        else:
            avg_corr = np.mean(corrs)
            # Map correlation from [-1,1] to [0,1] (negative correlation still gives some signal >0)
            correlation_score = (avg_corr + 1.0) / 2.0

        # Dispersion: cross-sectional std of today's basket returns
        dispersion = np.std(basket_returns_today) if len(basket_returns_today) > 1 else 0.0
        # Normalize: typical daily dispersion ~0.01-0.02, cap at 0.1
        dispersion_score = min(dispersion / 0.03, 1.0)   # scale, high dispersion -> high risk

        # Regime detection: 20-day volatility of TQQQ
        vol = np.std(tqqq_returns[-20:]) * np.sqrt(252)  # annualized
        if vol > 0.5:          # high vol regime (50% annualized)
            regime_score = 0.2
        elif vol > 0.3:        # medium vol
            regime_score = 0.6
        else:                  # low vol
            regime_score = 1.0

        # 4. Composite signal (multiplicative blending)
        # Higher seasonality, higher correlation, lower dispersion, lower vol => higher weight
        composite = seasonality_score * correlation_score * (1 - dispersion_score) * regime_score

        # 5. Dynamic sizing
        weight = min(composite, 1.0) * self.maxWeight
        weight = max(weight, 0.0)   # no negative (no shorting)

        # 6. Rebalance
        self.SetHoldings("TQQQ", weight)

        # Optional: log scores for debugging
        self.Debug(f"Month: {month}, Seasonality: {seasonality_score:.2f}, "
                   f"Corr: {correlation_score:.2f}, Dispersion: {dispersion_score:.2f}, "
                   f"Regime: {regime_score:.2f}, Composite: {composite:.2f}, Weight: {weight:.2f}")
