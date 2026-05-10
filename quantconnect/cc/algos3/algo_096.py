from QuantConnect import *
from QuantConnect.Algorithm import *
from QuantConnect.Data.Market import TradeBar
from QuantConnect.Indicators import *
from QuantConnect.Securities import *
from System import *

class ResistanceHoldDaily(QCAlgorithm):
    """
    Strategy: Resistance Hold
    Maintain full position if current price > 10-day high.
    Otherwise, exit the position (remain in cash).
    """
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        # Add the asset (change symbol if desired)
        self.symbol = self.AddEquity("SPY", Resolution.Daily).Symbol

        # Rolling window to store the last 10 daily highs (excluding today)
        self.highs = RollingWindow[float](10)

        # Warm up the algorithm so we have 10 bars of history to start
        self.SetWarmUp(10, Resolution.Daily)

    def OnData(self, data: Slice):
        # Do not trade during warm-up
        if self.IsWarmingUp:
            if data.Bars.ContainsKey(self.symbol):
                # Populate the window during warm-up
                bar = data.Bars[self.symbol]
                self.highs.Add(bar.High)
            return

        # Ensure we have data for our symbol
        if not data.Bars.ContainsKey(self.symbol):
            return

        bar = data.Bars[self.symbol]
        current_close = bar.Close

        # The rolling window must be ready (10 entries) and we should have added today's data?
        # For the strategy, we compare current close to the max of the *previous* 10 highs.
        # So we first compute the max of the window, then update the window with today's high.
        if not self.highs.IsReady:
            # Not enough history; we only add today's high and skip trading
            self.highs.Add(bar.High)
            return

        # Max of the last 10 highs (excluding today)
        max_10d_high = max(self.highs)

        # Update the window with today's high for next day's calculation
        self.highs.Add(bar.High)

        # Strategy logic
        if current_close > max_10d_high:
            # Price breaks above the 10-day high -> go long (fully invested)
            if not self.Portfolio.Invested:
                self.SetHoldings(self.symbol, 1.0)
                self.Log(f"{self.Time}: BUY - Close {current_close} > 10d High {max_10d_high}")
        else:
            # Price fails to hold above the 10-day high -> exit position
            if self.Portfolio.Invested:
                self.Liquidate(self.symbol)
                self.Log(f"{self.Time}: SELL - Close {current_close} <= 10d High {max_10d_high}")
