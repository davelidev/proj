# region imports
from AlgorithmImports import *
# endregion

class Algo099(QCAlgorithm):
    """
    QuantConnect Algorithm: Algo099
    Time Window Strategy: Trade only between 10:00 AM and 3:00 PM Eastern,
    avoiding the market open and close frenzy.
    Uses a simple 200-day simple moving average as a trend filter.
    Buys SPY when price > 200-day SMA at the start of the window,
    sells when price < 200-day SMA during the window.
    Designed for daily execution from 2014 to 2025, starting with $100k.
    """

    def Initialize(self):
        # Strategy timeframe
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 1, 1)
        self.SetCash(100000)

        # Add SPY with minute resolution for intraday time checks
        self.symbol = self.AddEquity("SPY", Resolution.Minute).Symbol

        # Create a 200-day SMA using daily consolidator
        self.sma = self.SMA(self.symbol, 200, Resolution.Daily, Field.Close)
        self.consolidator = TradeBarConsolidator(timedelta(days=1))
        self.SubscriptionManager.AddConsolidator(self.symbol, self.consolidator)
        self.sma.Attach(self.consolidator)

        # Set warm-up period to fill the SMA
        self.SetWarmUp(200, Resolution.Daily)

        # Define time window boundaries (Eastern Time)
        self.window_start = datetime(1, 1, 1, 10, 0, 0).time()   # 10:00 AM
        self.window_end   = datetime(1, 1, 1, 15, 0, 0).time()   # 3:00 PM

        # Schedule a daily trading routine
        self.Schedule.On(self.DateRules.EveryDay(self.symbol),
                         self.TimeRules.AfterMarketOpen(self.symbol, 30),   # 10:00 AM
                         self.MorningAction)
        self.Schedule.On(self.DateRules.EveryDay(self.symbol),
                         self.TimeRules.BeforeMarketClose(self.symbol, 60), # 2:00 PM
                         self.AfternoonCheck)

    def IsWithinWindow(self):
        """Check if current time is between 10:00 AM and 3:00 PM Eastern."""
        current_time = self.Time.time()
        return self.window_start <= current_time <= self.window_end

    def MorningAction(self):
        """Execute at the beginning of the window (10:00 AM).
        If price > 200-day SMA and not invested, buy."""
        if not self.IsWithinWindow():
            return
        if not self.sma.IsReady:
            return

        price = self.Securities[self.symbol].Price
        sma_value = self.sma.Current.Value

        if price > sma_value:
            if not self.Portfolio.Invested:
                self.SetHoldings(self.symbol, 0.5)   # 50% of capital
                self.Log(f"{self.Time}: BUY signal (Price={price:.2f}, SMA={sma_value:.2f})")

    def AfternoonCheck(self):
        """Check at 2:00 PM. If price < 200-day SMA while invested, sell."""
        if not self.IsWithinWindow():
            return
        if not self.sma.IsReady:
            return

        price = self.Securities[self.symbol].Price
        sma_value = self.sma.Current.Value

        if price < sma_value:
            if self.Portfolio.Invested:
                self.Liquidate(self.symbol)
                self.Log(f"{self.Time}: SELL signal (Price={price:.2f}, SMA={sma_value:.2f})")

    def OnData(self, data):
        """Optional: Placeholder for any other data processing."""
        pass
