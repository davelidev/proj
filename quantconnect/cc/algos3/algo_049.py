from System import *
from QuantConnect import *
from QuantConnect.Algorithm import *
from QuantConnect.Indicators import *
from QuantConnect.Data import *
from QuantConnect.Data.UniverseSelection import *
from datetime import timedelta
import numpy as np
import pandas as pd

class Algo049(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        # Add TQQQ as benchmark and for correlation
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol

        # Universe settings
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseFilter, self.FineFilter)

        # Basket for selected securities
        self.basket = {}

        # Regime detection using TQQQ volatility (ATR)
        self.regime = self.ATR(self.tqqq, 14, MovingAverageType.Simple, Resolution.Daily)

        # Rebalance daily
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.AfterMarketOpen("TQQQ", 30),
                         self.Rebalance)

        self.last_rebalance = None

    def CoarseFilter(self, coarse):
        # Basic liquidity filter
        filtered = [c for c in coarse if c.HasFundamentalData and c.Price > 5 and c.DollarVolume > 10000000]
        return filtered

    def FineFilter(self, fine):
        # Top 10 by market cap
        sorted_by_mcap = sorted(fine, key=lambda f: f.MarketCap, reverse=True)
        return [f.Symbol for f in sorted_by_mcap[:10]]

    def OnSecuritiesChanged(self, changes):
        # Update basket: add new symbols, remove old, initialize indicators
        for symbol in changes.AddedSecurities:
            symbol = symbol.Symbol
            if symbol not in self.basket:
                self.basket[symbol] = {
                    "roc": RateOfChange(21),
                    "std": StandardDeviation(21),
                    "corr": Correlation(f"{symbol}-TQQQ", 60),  # 60-day correlation
                    "seasonal_returns": None,  # cached seasonal data
                    "last_month": -1
                }
                # Register indicators with consolidator for daily updates
                self.RegisterIndicator(symbol, self.basket[symbol]["roc"], Resolution.Daily)
                self.RegisterIndicator(symbol, self.basket[symbol]["std"], Resolution.Daily)
                self.RegisterIndicator(symbol, self.basket[symbol]["corr"], Resolution.Daily)
                # For correlation, we need two inputs: symbol and TQQQ
                # We'll update manually in OnData to pass both.

        for symbol in changes.RemovedSecurities:
            symbol = symbol.Symbol
            if symbol in self.basket:
                del self.basket[symbol]

    def OnData(self, data):
        # Update indicators that need dual inputs (correlation)
        if data.ContainsKey(self.tqqq) and data[self.tqqq] is not None:
            tqqq_price = data[self.tqqq].Close
            for symbol in self.basket:
                if data.ContainsKey(symbol) and data[symbol] is not None:
                    price = data[symbol].Close
                    self.basket[symbol]["corr"].Update(self.Time, price, tqqq_price)

    def Rebalance(self):
        # Only rebalance once per day
        if self.Time.date() == self.last_rebalance:
            return
        self.last_rebalance = self.Time.date()

        # Compute scores and weights for all active basket symbols
        scores = {}
        total_score = 0.0

        # Gather returns for dispersion calculation
        returns_series = {}
        for symbol, indicators in self.basket.items():
            # Check if indicators are ready
            if not indicators["roc"].IsReady or not indicators["std"].IsReady or not indicators["corr"].IsReady:
                continue

            roc = indicators["roc"].Current.Value
            std = indicators["std"].Current.Value
            if std == 0:
                continue

            # Base Sharpe-like ratio
            sharpe = roc / std

            # Correlation signal: higher correlation with TQQQ -> overweight
            corr_val = indicators["corr"].Current.Value
            corr_signal = 0.5 + 0.5 * corr_val  # scale to [0,1]

            # Seasonality: compute average return in current month over last 5 years
            month = self.Time.month
            if indicators["last_month"] != month:
                indicators["last_month"] = month
                # Fetch historical data (5 years) for seasonal calculation
                hist = self.History(symbol, 5 * 365, Resolution.Daily)
                if not hist.empty and 'close' in hist.columns:
                    close = hist['close']
                    # Calculate daily returns and group by month
                    daily_ret = close.pct_change().dropna()
                    monthly_ret = daily_ret.groupby(daily_ret.index.month).mean()
                    indicators["seasonal_returns"] = monthly_ret  # dict month->mean return
                else:
                    indicators["seasonal_returns"] = None

            seasonal_mean = 0.0
            if indicators["seasonal_returns"] is not None and month in indicators["seasonal_returns"].index:
                seasonal_mean = indicators["seasonal_returns"].loc[month]
            # Normalize seasonal signal (z-score across securities? here use raw)
            seasonal_signal = np.clip(seasonal_mean * 100, -1, 1)  # simple scaling

            # Dispersion: cross-sectional std of recent returns across basket
            # We'll compute later after collecting returns
            returns_series[symbol] = roc  # using 21-day ROC as a return proxy

            # Regime signal: use TQQQ ATR relative to its SMA
            regime_val = self.regime.Current.Value
            # If regime (ATR) is high, reduce overall exposure; else increase.
            # Use a simple threshold based on historical median (not computed) -> default neutral
            regime_signal = 1.0  # placeholder, could be dynamically adjusted

            # Composite score (weights chosen arbitrarily for signal diversity)
            score = (0.4 * sharpe + 0.3 * corr_signal + 0.1 * seasonal_signal + 0.2 * regime_signal)
            scores[symbol] = max(score, 0)  # non-negative
            total_score += scores[symbol]

        # Compute dispersion signal: cross-sectional std of ROC values
        if len(returns_series) > 1:
            roc_array = np.array(list(returns_series.values()))
            cross_sectional_std = np.std(roc_array)
            # Use as a global multiplier: high dispersion -> more opportunity -> increase overall weight?
            # For simplicity, we adjust the total weight target
            disp_factor = 1.0 + 0.5 * cross_sectional_std  # boost up to 50%
        else:
            disp_factor = 1.0

        # Now compute target weights
        total_weight = 0.0
        weights = {}
        if total_score > 0:
            for symbol, score in scores.items():
                weight = score / total_score * disp_factor
                # Cap individual weight to 1 (no leverage)
                weight = min(weight, 1.0)
                # Also ensure total <= 1 (disp_factor might push over)
                weights[symbol] = weight
                total_weight += weight

            # Normalize if total>1 (due to disp_factor)
            if total_weight > 1.0:
                for symbol in weights:
                    weights[symbol] /= total_weight

            # Execute rebalance
            for symbol, weight in weights.items():
                self.SetHoldings(symbol, weight)

        # Liquidate symbols no longer in basket
        for symbol in self.Portfolio.Keys:
            if symbol not in self.basket and symbol != self.tqqq:
                self.Liquidate(symbol)

        # Also set a small position in TQQQ? Not required. Strategy uses only basket.
