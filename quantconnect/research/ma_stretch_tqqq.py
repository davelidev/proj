from datetime import datetime, timedelta
from AlgorithmImports import *


class TQQQMAStretch(QCAlgorithm):

    def Initialize(self):
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100_000)
        
        self.sym = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        
        # Indicators
        self.sma20 = self.SMA(self.sym, 20, Resolution.Daily)
        self.sma200 = self.SMA(self.sym, 200, Resolution.Daily)
        
        self.SetWarmUp(200, Resolution.Daily)
        
        self.Schedule.On(
            self.DateRules.EveryDay(self.sym),
            self.TimeRules.AfterMarketOpen(self.sym, 30),
            self.Rebalance,
        )

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma20.IsReady or not self.sma200.IsReady:
            return

        price = self.Securities[self.sym].Price
        ma20 = self.sma20.Current.Value
        ma200 = self.sma200.Current.Value

        if not self.Portfolio.Invested:
            # ENTRY: Bull market (Price > ma200) AND deep stretch below ma20
            # Stretch threshold: 5% below ma20
            if price > ma200 and price < (ma20 * 0.95):
                self.SetHoldings(self.sym, 1.0)
                self.Debug(f"ENTRY: ma20 Stretch at {price}")
        else:
            # EXIT: Revert to ma20 OR Trend breaks
            if price > ma20 or price < ma200:
                self.Liquidate(self.sym)
                self.Debug(f"EXIT: Reverted at {price}")
