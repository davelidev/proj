# Algo0090 - Momentum Consensus Strategy
# Hold S&P 500 only when at least 3 out of 5 momentum signals are positive.
# Momentum signals based on different lookback periods.
# Uses only SetStartDate, SetEndDate, SetCash, AddEquity, SetHoldings.
# No brokerage model.

from AlgorithmImports import *

class Algo090(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 1, 1)
        self.SetCash(100000)

        # Add SPY as the trading asset (daily data)
        self.symbol = self.AddEquity("SPY", Resolution.Daily).Symbol

        # Momentum lookback periods (in trading days)
        self.lookbacks = [21, 63, 126, 189, 252]
        self.max_lookback = max(self.lookbacks)

        # Rolling window to store historical close prices
        self.price_history = RollingWindow[float](self.max_lookback + 5)

        # Preload historical data before the start date
        history = self.History(self.symbol, self.max_lookback + 5, Resolution.Daily)
        if not history.empty:
            for time, row in history.loc[self.symbol].iterrows():
                self.price_history.Add(row["close"])

        # Flag to indicate enough history is available
        self.ready = self.price_history.Count >= self.max_lookback

    def OnData(self, data: Slice):
        # Add today's close price to the rolling window
        if data.ContainsKey(self.symbol):
            self.price_history.Add(self.Securities[self.symbol].Close)

        # Ensure we have enough history for all lookbacks
        if not self.ready:
            if self.price_history.Count >= self.max_lookback:
                self.ready = True
            else:
                return

        # Count how many momentum signals are positive
        positive_signals = 0
        today_price = self.price_history[0]

        for lookback in self.lookbacks:
            # Price lookback days ago (index = lookback in the rolling window)
            past_price = self.price_history[lookback]
            if past_price is None:
                continue

            # Momentum = (today / past - 1)
            if past_price != 0 and (today_price / past_price - 1) > 0:
                positive_signals += 1

        # Trade decision: hold 100% if at least 3/5 signals are up, otherwise 0%
        if positive_signals >= 3:
            self.SetHoldings(self.symbol, 1.0)
        else:
            self.SetHoldings(self.symbol, 0.0)
