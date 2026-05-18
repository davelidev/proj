from AlgorithmImports import *

class RegimeGatedTOM(QCAlgorithm):
    """Turn-of-month TQQQ ONLY when QQQ > 200d Donchian midline; else BIL all month."""
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil  = self.AddEquity("BIL",  Resolution.Daily).Symbol
        self.hi200 = self.MAX(self.qqq, 200, Resolution.Daily)
        self.lo200 = self.MIN(self.qqq, 200, Resolution.Daily)
        self.SetWarmUp(220, Resolution.Daily)
        self.in_window = False
        self.Schedule.On(self.DateRules.MonthEnd(self.qqq, 2),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.WindowStart)
        self.Schedule.On(self.DateRules.MonthStart(self.qqq, 4),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.WindowEnd)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.DailyCheck)

    def _bull(self):
        if not (self.hi200.IsReady and self.lo200.IsReady): return False
        mid = (self.hi200.Current.Value + self.lo200.Current.Value) / 2.0
        return self.Securities[self.qqq].Price > mid

    def WindowStart(self):
        self.in_window = True
        if self.IsWarmingUp: return
        if self._bull():
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil)
                self.SetHoldings(self.tqqq, 1.0)

    def WindowEnd(self):
        self.in_window = False
        if self.Portfolio[self.tqqq].Invested:
            self.Liquidate(self.tqqq)
            self.SetHoldings(self.bil, 1.0)

    def DailyCheck(self):
        # Defensive: outside window we hold BIL; inside window we hold TQQQ but only if trend.
        if self.IsWarmingUp: return
        if self.in_window:
            if not self._bull() and self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)
            elif self._bull() and not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil)
                self.SetHoldings(self.tqqq, 1.0)
        else:
            if not self.Portfolio[self.bil].Invested:
                if self.Portfolio[self.tqqq].Invested: self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data): pass
