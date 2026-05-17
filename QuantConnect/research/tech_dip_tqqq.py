from datetime import datetime, timedelta
from AlgorithmImports import *


class TQQQTechDip(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.SetBenchmark("QQQ")
        
        self.sym = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        
        self.rsi = self.RSI(self.sym, 2)
        self.max = self.MAX(self.sym, 252)
        self.sma50 = self.SMA(self.sym, 50)
        
        self.SetWarmUp(252, Resolution.Daily)
        
        self.Schedule.On(
            self.DateRules.EveryDay(self.sym),
            self.TimeRules.AfterMarketOpen(self.sym, 30),
            self.Rebalance,
        )

    def Rebalance(self):
        if self.IsWarmingUp or not (self.max.IsReady and self.sma50.IsReady):
            return

        price = self.Securities[self.sym].Price
        rsi_val = self.rsi.Current.Value
        sma_val = self.sma50.Current.Value
        max_val = self.max.Current.Value

        if not self.Portfolio.Invested:
            # ENTRY: RSI(2) < 30 AND Price > SMA(50)
            if rsi_val < 30 and price > sma_val:
                self.SetHoldings(self.sym, 1.0)
                self.Debug(f"ENTRY TQQQ at {price}")
        else:
            # EXIT: 15% hard stop OR at 1yr-high
            avg_price = self.Portfolio[self.sym].AveragePrice
            if price <= avg_price * 0.85:
                self.Liquidate(self.sym)
                self.Debug(f"STOP LOSS EXIT at {price}")
            elif price >= max_val:
                self.Liquidate(self.sym)
                self.Debug(f"TAKE PROFIT (ATH) EXIT at {price}")
