# QuantConnect Algorithm: Algo081
# Strategy: Correlation Crash - Switch to defensive on correlation spike.
# Rules: weights <= 1.0, no leverage, no SetBrokerageModel
# Universe: SPY (equities) and TLT (long-term bonds)
# Logic: Compute 63-day rolling correlation of daily returns between SPY and TLT.
#   If correlation > 0.7 (spike), allocate 100% to TLT (defensive).
#   Otherwise, maintain equal weight (50/50) between SPY and TLT.

import numpy as np

class Algo081(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        # Add assets
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        self.tlt = self.AddEquity("TLT", Resolution.Daily).Symbol

        # Correlation parameters
        self.lookback = 63               # trading days (approx 3 months)
        self.threshold = 0.7             # correlation spike level

        # Store closing prices for correlation calculation
        self.spy_prices = RollingWindow[float](self.lookback + 1)
        self.tlt_prices = RollingWindow[float](self.lookback + 1)

        self.first = True

    def OnData(self, data):
        # Ensure we have data for both assets
        if not (data.ContainsKey(self.spy) and data.ContainsKey(self.tlt)):
            return

        spy_close = data[self.spy].Close
        tlt_close = data[self.tlt].Close
        self.spy_prices.Add(spy_close)
        self.tlt_prices.Add(tlt_close)

        # Not enough data for correlation yet -> use default 50/50 allocation
        if self.spy_prices.Count < self.lookback + 1:
            self.SetHoldings(self.spy, 0.5)
            self.SetHoldings(self.tlt, 0.5)
            return

        # Build return series from oldest to newest
        spy_list = list(self.spy_prices)[::-1]   # oldest first
        tlt_list = list(self.tlt_prices)[::-1]

        spy_returns = []
        tlt_returns = []
        for i in range(1, len(spy_list)):
            spy_ret = (spy_list[i] - spy_list[i-1]) / spy_list[i-1]
            tlt_ret = (tlt_list[i] - tlt_list[i-1]) / tlt_list[i-1]
            spy_returns.append(spy_ret)
            tlt_returns.append(tlt_ret)

        # Compute Pearson correlation coefficient
        corr = np.corrcoef(spy_returns, tlt_returns)[0, 1]

        # Decide allocation based on correlation spike
        if corr > self.threshold:
            # Correlation spike -> switch to defensive (100% TLT)
            self.SetHoldings(self.tlt, 1.0)
            self.SetHoldings(self.spy, 0.0)
        else:
            # Normal market -> maintain 50/50 balanced allocation
            self.SetHoldings(self.spy, 0.5)
            self.SetHoldings(self.tlt, 0.5)
