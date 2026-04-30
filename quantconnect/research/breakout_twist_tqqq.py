from datetime import datetime, timedelta
from AlgorithmImports import *


class TQQQBreakoutTwist(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        
        self.sym = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        
        # Indicators
        self.adx = self.ADX(self.sym, 15, Resolution.Daily)
        self.high = self.MAX(self.sym, 10, Resolution.Daily)
        self.low = self.MIN(self.sym, 10, Resolution.Daily)
        self.sma200 = self.SMA(self.sym, 200, Resolution.Daily)
        
        self.SetWarmUp(200, Resolution.Daily)
        
        self.Schedule.On(
            self.DateRules.EveryDay(self.sym),
            self.TimeRules.AfterMarketOpen(self.sym, 30),
            self.Rebalance,
        )

    def Rebalance(self):
        if self.IsWarmingUp or not self.adx.IsReady or not self.high.IsReady:
            return

        price = self.Securities[self.sym].Price
        adx_val = self.adx.Current.Value
        high_val = self.high.Current.Value
        low_val = self.low.Current.Value
        sma_val = self.sma200.Current.Value

        if not self.Portfolio.Invested:
            # ENTRY: ADX < 20 (Congestion) AND Price hits 10-day high (Breakout)
            if adx_val < 20 and price >= high_val:
                self.SetHoldings(self.sym, 1.0)
                self.Debug(f"ENTRY: Breakout from Congestion at {price}")
        else:
            # EXIT: Hit 10-day low (Stop and Reverse concept) OR 200 SMA break
            if price <= low_val or price < sma_val:
                self.Liquidate(self.sym)
                self.Debug(f"EXIT: Stop Hit at {price}")
