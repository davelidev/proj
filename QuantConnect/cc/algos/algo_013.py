from AlgorithmImports import *


class Algo013(QCAlgorithm):
    """#13 — Donchian 50-day breakout. Long TQQQ on 50d high, exit on 50d low."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.don  = self.DCH(self.qqq, 50, Resolution.Daily)
        self.SetWarmUp(60, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq),
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30),
                         self.Rebalance)

    def Rebalance(self):
        if self.IsWarmingUp or not self.don.IsReady: return
        px = self.Securities[self.qqq].Price
        invested = self.Portfolio[self.tqqq].Invested
        upper = self.don.UpperBand.Current.Value
        lower = self.don.LowerBand.Current.Value
        # Buy when price near new high; exit when near low
        if not invested and px >= upper * 0.999:
            self.SetHoldings(self.tqqq, 1.0)
        elif invested and px <= lower * 1.001:
            self.Liquidate(self.tqqq)
