from AlgorithmImports import *

class IntradayReversal(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        # Add SPY with minute resolution
        self.symbol = self.AddEquity("SPY", Resolution.Minute).Symbol

        # Daily consolidator to track previous day's close
        self.consolidator = TradeBarConsolidator(timedelta(days=1))
        self.consolidator.DataConsolidated += self.OnDailyConsolidated
        self.SubscriptionManager.AddConsolidator(self.symbol, self.consolidator)

        # Historical request for previous close on first day
        self.previous_close = None
        self.bought_today = False
        self.last_trade_date = None

        # Schedule selling at end of day (1 minute before market close)
        self.Schedule.On(
            self.DateRules.EveryDay(self.symbol),
            self.TimeRules.BeforeMarketClose(self.symbol, 1),
            self.SellAtEndOfDay
        )

    def OnDailyConsolidated(self, sender, bar):
        # Store previous close as the last daily close
        self.previous_close = bar.Close

    def OnData(self, data):
        # Only process if we have a previous close
        if self.previous_close is None:
            return

        # Check if we have a tradebar for our symbol
        if not data.Bars.ContainsKey(self.symbol):
            return

        # Get current bar
        bar = data.Bars[self.symbol]
        current_price = bar.Close

        # Avoid buying in the last 30 minutes of the trading day
        utc_time = self.UtcTime
        exchange = self.MarketHoursDatabase.GetExchangeHours(self.symbol.ID.Market, self.symbol, self.symbol.ID.SecurityType)
        local_time = exchange.UtcToLocal(utc_time)
        market_close = exchange.MarketClose(local_time)
        if market_close is not None:
            time_until_close = (market_close - local_time).total_seconds() / 60
            if time_until_close <= 30:
                return

        # Check for intraday drop of at least 1% from previous close
        if current_price <= self.previous_close * 0.99 and not self.bought_today:
            self.SetHoldings(self.symbol, 1.0)   # All in
            self.bought_today = True
            self.last_trade_date = self.Time.date()

    def SellAtEndOfDay(self):
        # Sell all holdings at end of day
        if self.Portfolio[self.symbol].Invested and self.bought_today:
            self.Liquidate(self.symbol)
            self.bought_today = False

    def OnEndOfDay(self):
        # Reset flag if we didn't trade today (for next day)
        if not self.bought_today:
            self.last_trade_date = self.Time.date()
