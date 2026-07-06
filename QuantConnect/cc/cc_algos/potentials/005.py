# AntiMartingale — Anti-Martingale pyramid on TQQQ
from AlgorithmImports import *


class AntiMartingale(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.sym = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        self.entry_price = None
        self.cur_weight = 0.0
        self.SetWarmUp(210, Resolution.Daily)
        self.Schedule.On(
            self.DateRules.EveryDay(self.qqq),
            self.TimeRules.AfterMarketOpen(self.qqq, 35),
            self.Rebalance,
        )

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma.IsReady:
            return
        price = self.Securities[self.qqq].Price
        bull = price > self.sma.Current.Value
        if not bull:
            if self.Portfolio.Invested:
                self.Liquidate(self.sym)
                self.entry_price = None
                self.cur_weight = 0.0
            return
        if not self.Portfolio.Invested:
            self.SetHoldings(self.sym, 0.5)
            self.entry_price = price
            self.cur_weight = 0.5
            return
        # Pyramid: each 5.0% above entry, add another step until max_weight.
        steps = (price / self.entry_price - 1) / (5.0 / 100.0)
        target = min(1.0, 0.5 + max(0, int(steps)) * 0.15)
        if abs(target - self.cur_weight) > 0.05:
            self.SetHoldings(self.sym, target)
            self.cur_weight = target
