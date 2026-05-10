# region imports
from AlgorithmImports import *
# endregion

class Algo0087(QCAlgorithm):
    """
    Beta-scaled positioning strategy.
    - Uses SPY as low-beta asset and TQQQ (3x leveraged S&P 500) as high-beta asset.
    - Determines market regime (trending vs. choppy) using the spread between a 20-day
      and 50-day simple moving average of SPY.
    - In trending markets, allocate more to high-beta; in choppy markets, allocate more to low-beta.
    - Only uses allowed methods: SetStartDate, SetEndDate, SetCash, AddEquity, SetHoldings.
    """

    def Initialize(self):
        # Set the date range and initial cash
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 1, 1)
        self.SetCash(100000)

        # Add the securities
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol

        # Price history storage (manually maintained to avoid indicator/history methods)
        self.spy_prices = []

        # Parameters for trend detection
        self.short_period = 20
        self.long_period = 50
        self.trend_threshold = 0.02  # 2% difference between SMAs is considered trending

    def OnData(self, data):
        # Update price list for SPY
        if data.Bars.ContainsKey(self.spy):
            self.spy_prices.append(data.Bars[self.spy].Close)

        # Need enough data to compute long SMA
        if len(self.spy_prices) < self.long_period:
            return

        # Compute short and long simple moving averages
        short_sma = sum(self.spy_prices[-self.short_period:]) / self.short_period
        long_sma = sum(self.spy_prices[-self.long_period:]) / self.long_period
        current_price = self.spy_prices[-1]

        # Determine regime based on relative SMA spread
        diff = abs(short_sma - long_sma)
        if diff / current_price > self.trend_threshold:
            # Trending market -> overweight high-beta
            high_beta_weight = 0.8
            low_beta_weight = 0.2
        else:
            # Choppy market -> overweight low-beta
            high_beta_weight = 0.2
            low_beta_weight = 0.8

        # Set portfolio weights
        self.SetHoldings(self.tqqq, high_beta_weight)
        self.SetHoldings(self.spy, low_beta_weight)
