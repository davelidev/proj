from datetime import datetime, timedelta
from AlgorithmImports import *

class TQQQPullbackCross(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.SetBenchmark("QQQ")
        
        self.sym = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        
        self.sma5 = self.SMA(self.sym, 5, Resolution.Daily)
        self.sma10 = self.SMA(self.sym, 10, Resolution.Daily)
        self.sma200 = self.SMA(self.qqq, 200, Resolution.Daily)
        
        self.SetWarmUp(200, Resolution.Daily)
        
        self.Schedule.On(
            self.DateRules.EveryDay(self.sym),
            self.TimeRules.AfterMarketOpen(self.sym, 30),
            self.Rebalance,
        )

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma200.IsReady:
            return

        price = self.Securities[self.sym].Price
        qqq_price = self.Securities[self.qqq].Price
        s5 = self.sma5.Current.Value
        s10 = self.sma10.Current.Value
        s200 = self.sma200.Current.Value
        
        # We need the previous values to check for a cross
        # But we can also just use the current relationship
        
        # Bull Market Filter
        if qqq_price > s200:
            if not self.Portfolio.Invested:
                # ENTRY: Short MA is below Long MA (pullback) AND Price is below Short MA (deep pullback)
                if s5 < s10 and price < s5:
                    self.SetHoldings(self.sym, 1.0)
            else:
                # EXIT: Short MA crosses back above Long MA (trend resumed and exhausted)
                if s5 > s10:
                    self.Liquidate(self.sym)
        else:
            self.Liquidate(self.sym)
