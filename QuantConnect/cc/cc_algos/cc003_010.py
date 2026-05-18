from AlgorithmImports import *
import math

class ChoppinessGatedROC(QCAlgorithm):
    """ROC(30) trend signal, but only acts when Choppiness Index says market is trending (< 50)."""
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil  = self.AddEquity("BIL",  Resolution.Daily).Symbol

        self.roc   = self.ROC(self.qqq, 30, Resolution.Daily)
        self.atr   = self.ATR(self.qqq, 14, MovingAverageType.Wilders, Resolution.Daily)
        self.hi14  = self.MAX(self.qqq, 14, Resolution.Daily)
        self.lo14  = self.MIN(self.qqq, 14, Resolution.Daily)

        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Rebalance)
        self.SetWarmUp(40, Resolution.Daily)

    def _choppiness(self):
        rng = self.hi14.Current.Value - self.lo14.Current.Value
        atr = self.atr.Current.Value
        if rng <= 0 or atr <= 0:
            return 100.0
        # CI = 100 * log10(sum(ATR_14) / (max14 - min14)) / log10(14).
        # Approx sum(ATR) ≈ 14 * ATR(14) (TR average × N).
        return 100.0 * math.log10((14 * atr) / rng) / math.log10(14)

    def Rebalance(self):
        if self.IsWarmingUp or not (self.roc.IsReady and self.atr.IsReady and self.hi14.IsReady and self.lo14.IsReady):
            return
        ci = self._choppiness()
        r  = self.roc.Current.Value

        trending = ci < 50.0  # CI < ~38 strong trend, > ~62 strong consolidation

        if trending and r > 0:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil)
                self.SetHoldings(self.tqqq, 1.0)
        elif (trending and r < 0) or not trending:
            if self.Portfolio[self.tqqq].Invested and not trending:
                # in chop, stay where we are to avoid whipsaw — only flip on clear bearish trend
                pass
            elif r < 0 and not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
