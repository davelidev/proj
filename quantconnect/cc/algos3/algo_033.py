from QuantConnect import *
from QuantConnect.Algorithm import QCAlgorithm
from QuantConnect.Data.UniverseSelection import *
from QuantConnect.Indicators import *
import pandas as pd
import numpy as np

class Algo033(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.AddEquity("TQQQ", Resolution.Daily)
        self.AddUniverse(self.CoarseSelectionFunction)

        self.basket = []                      # current universe symbols (list of Symbol)
        self.tqqq = self.Symbol("TQQQ")
        self.highest_equity = 100000

        # Parameters for vol-of-vol
        self.vol_lookback = 20
        self.vol_roc_period = 5
        self.base_weight = 1.0

        # For drawdown tracking
        self.drawdown_threshold = 0.20

    def CoarseSelectionFunction(self, coarse):
        # Filter stocks with fundamental data and positive market cap
        filtered = [x for x in coarse if x.HasFundamentalData and x.MarketCap > 0]
        # Sort by market cap descending and take top 10
        sorted_by_mcap = sorted(filtered, key=lambda x: x.MarketCap, reverse=True)
        top10 = sorted_by_mcap[:10]
        symbols = [x.Symbol for x in top10]
        self.basket = symbols
        return symbols

    def OnData(self, data):
        if not self.basket:
            return

        # ---- Compute TQQQ signals ----
        tqqq_history = self.History(["TQQQ"], 252, Resolution.Daily)
        if tqqq_history.empty:
            return

        tqqq_close = tqqq_history.loc["TQQQ"]["close"]
        tqqq_returns = tqqq_close.pct_change().dropna()

        # 20-day volatility (standard deviation of daily returns)
        if len(tqqq_returns) < self.vol_lookback:
            return
        vol_20d = tqqq_returns.rolling(self.vol_lookback).std()
        current_vol = vol_20d.iloc[-1]

        # Rate of change of volatility (vol-of-vol)
        if len(vol_20d) < self.vol_lookback + self.vol_roc_period:
            return
        vol_roc = (current_vol / vol_20d.iloc[-self.vol_roc_period] - 1)

        # Momentum (12-month return)
        if len(tqqq_close) < 252:
            return
        momentum_12m = tqqq_close.iloc[-1] / tqqq_close.iloc[-252] - 1

        # ---- Compute basket signals ----
        basket_history = self.History(self.basket, 200, Resolution.Daily)
        if basket_history.empty:
            return

        # Breadth: fraction of stocks above 200-day SMA
        sma200_cross = []
        for sym in self.basket:
            if sym in basket_history.index.levels[0]:
                close_series = basket_history.loc[sym]["close"]
                if len(close_series) >= 200:
                    sma200 = close_series.rolling(200).mean()
                    if not np.isnan(sma200.iloc[-1]):
                        sma200_cross.append(1 if close_series.iloc[-1] > sma200.iloc[-1] else 0)
        breadth = np.mean(sma200_cross) if sma200_cross else 0.5

        # Average 20-day volatility of basket stocks (simple mean)
        vol_basket_list = []
        for sym in self.basket:
            if sym in basket_history.index.levels[0]:
                close_series = basket_history.loc[sym]["close"]
                returns = close_series.pct_change().dropna()
                if len(returns) >= 20:
                    vol_basket_list.append(returns.rolling(20).std().iloc[-1])
        avg_basket_vol = np.mean(vol_basket_list) if vol_basket_list else 0

        # ---- Combine signals into position size ----
        # Base adjustment from vol-of-vol
        if vol_roc > 0:
            vol_mult = 0.8       # reduce size when vol rising
        else:
            vol_mult = 1.2       # increase size when vol falling

        # Momentum filter: only apply if momentum positive (simplistic)
        momentum_factor = 1.0 if momentum_12m > 0 else 0.5

        # Breadth factor: stronger if more stocks above SMA
        breadth_factor = 0.5 + 0.5 * breadth

        # Volatility regime: if current vol > historical median (1 year), reduce
        if len(vol_20d) >= 252:
            hist_vol_median = vol_20d.median()
            vol_regime_factor = 0.7 if current_vol > hist_vol_median else 1.0
        else:
            vol_regime_factor = 1.0

        # Initial weight (capped at 1)
        weight = self.base_weight * vol_mult * momentum_factor * breadth_factor * vol_regime_factor
        weight = min(weight, 1.0)

        # ---- Drawdown adjustment ----
        current_equity = self.Portfolio.TotalPortfolioValue
        self.highest_equity = max(self.highest_equity, current_equity)
        drawdown = (self.highest_equity - current_equity) / self.highest_equity
        if drawdown > self.drawdown_threshold:
            weight *= 0.5

        # Ensure non-negative and <= 1
        weight = max(0, min(weight, 1.0))

        # ---- Execute ----
        self.SetHoldings("TQQQ", weight)
